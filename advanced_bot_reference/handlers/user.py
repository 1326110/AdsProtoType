from __future__ import annotations

import logging

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from database import get_db
from filters import NotBannedFilter
from keyboards import KeyboardBuilder, main_menu_kb, cancel_kb, settings_kb

logger = logging.getLogger(__name__)

user_router = Router()
user_router.message.filter(NotBannedFilter())
user_router.callback_query.filter(NotBannedFilter())


class FeedbackForm(StatesGroup):
    waiting_for_message = State()


class SettingsForm(StatesGroup):
    waiting_for_language = State()


# ── Start ──────────────────────────────────────────────────────────

@user_router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    text = (
        "Welcome! I'm an advanced modular bot built with aiogram 3.\n\n"
        "Features:\n"
        "  Modular plugin-style architecture\n"
        "  SQLite database with proper ORM\n"
        "  Admin panel & user management\n"
        "  Middlewares (throttling, logging, auth)\n"
        "  Broadcast system\n"
        "  Custom filters\n"
        "  FSM workflows\n\n"
        "Use the menu below or type /help."
    )
    await message.answer(text, reply_markup=main_menu_kb())


@user_router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    text = (
        "Available commands:\n"
        "/start - Main menu\n"
        "/help - This message\n"
        "/profile - View your profile\n"
        "/stats - System statistics\n"
        "/settings - Change preferences\n"
        "/feedback - Send feedback\n"
        "/about - About this bot\n"
        "/cancel - Cancel current operation"
    )
    await message.answer(text)


@user_router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext) -> None:
    current = await state.get_state()
    if current is None:
        await message.answer("Nothing to cancel.")
        return
    await state.clear()
    await message.answer("Operation cancelled.", reply_markup=main_menu_kb())


@user_router.message(Command("profile"))
async def cmd_profile(message: Message) -> None:
    db = get_db()
    user = await db.get_user(message.from_user.id)
    if user is None:
        await message.answer("User not found. Use /start to register.")
        return

    text = (
        f"Your Profile\n\n"
        f"ID: {user.telegram_id}\n"
        f"Username: @{user.username or 'N/A'}\n"
        f"Language: {user.language}\n"
        f"Premium: {'Yes' if user.is_premium else 'No'}\n"
        f"Commands used: {user.total_commands}\n"
        f"Last activity: {user.last_activity or 'N/A'}"
    )
    await message.answer(text)


@user_router.message(Command("stats"))
async def cmd_stats(message: Message) -> None:
    from services import StatsService
    text = await StatsService.get_stats_text()
    await message.answer(text)


@user_router.message(Command("about"))
async def cmd_about(message: Message) -> None:
    text = (
        "Advanced Modular Bot v1.0\n\n"
        "Built with:\n"
        "  aiogram 3.x\n"
        "  aiosqlite\n"
        "  python-dotenv\n\n"
        "Architecture highlights:\n"
        "  Layered (handlers/services/db/keyboards)\n"
        "  Middleware pipeline\n"
        "  Custom filters\n"
        "  FSM workflows\n"
        "  Webhook/polling auto-switch\n"
        "  Rate limiting\n"
        "  Broadcast system\n"
        "  Usage analytics"
    )
    await message.answer(text)


# ── Settings ───────────────────────────────────────────────────────

@user_router.message(Command("settings"))
async def cmd_settings(message: Message) -> None:
    await message.answer("Settings:", reply_markup=settings_kb())


@user_router.callback_query(F.data == "set_language")
async def set_language_start(query: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(SettingsForm.waiting_for_language)
    kb = KeyboardBuilder.reply([
        ["en", "ru", "hi", "zh", "ja"],
        ["Cancel"],
    ])
    await query.message.edit_text(
        "Select your language:",
        reply_markup=None,
    )
    await query.message.answer(
        "Available: en, ru, hi, zh, ja",
        reply_markup=kb,
    )


@user_router.message(SettingsForm.waiting_for_language, F.text)
async def set_language_done(message: Message, state: FSMContext) -> None:
    lang = message.text.strip().lower()
    valid = {"en", "ru", "hi", "zh", "ja"}
    if lang not in valid:
        await message.answer("Invalid language. Choose from: en, ru, hi, zh, ja")
        return
    db = get_db()
    await db.update_user(message.from_user.id, language=lang)
    await state.clear()
    await message.answer(
        f"Language set to {lang}.",
        reply_markup=main_menu_kb(),
    )


# ── Feedback ──────────────────────────────────────────────────────

@user_router.message(Command("feedback"))
async def feedback_start(message: Message, state: FSMContext) -> None:
    await state.set_state(FeedbackForm.waiting_for_message)
    await message.answer(
        "Send me your feedback or suggestions:",
        reply_markup=cancel_kb(),
    )


@user_router.message(FeedbackForm.waiting_for_message, F.text)
async def feedback_done(message: Message, state: FSMContext) -> None:
    text = message.text
    db = get_db()
    user = await db.get_user(message.from_user.id)
    name = user.first_name or user.username or str(user.telegram_id)

    from config import cfg
    from bot import bot

    for admin_id in cfg.ADMIN_IDS:
        try:
            await bot.send_message(
                admin_id,
                f"Feedback from {name} ({message.from_user.id}):\n\n{text}",
            )
        except Exception:
            pass

    await state.clear()
    await message.answer(
        "Thanks for your feedback!",
        reply_markup=main_menu_kb(),
    )


@user_router.message(FeedbackForm.waiting_for_message)
async def feedback_invalid(message: Message) -> None:
    await message.answer("Please send text feedback, or /cancel to exit.")


# ── Callback menu handlers ────────────────────────────────────────

@user_router.callback_query(F.data == "profile")
async def cb_profile(query: CallbackQuery) -> None:
    db = get_db()
    user = await db.get_user(query.from_user.id)
    if user is None:
        await query.message.edit_text("User not found.")
        return
    text = (
        f"Your Profile\n\n"
        f"ID: {user.telegram_id}\n"
        f"Username: @{user.username or 'N/A'}\n"
        f"Language: {user.language}\n"
        f"Premium: {'Yes' if user.is_premium else 'No'}\n"
        f"Commands: {user.total_commands}"
    )
    await query.message.edit_text(text, reply_markup=main_menu_kb())


@user_router.callback_query(F.data == "stats")
async def cb_stats(query: CallbackQuery) -> None:
    from services import StatsService
    text = await StatsService.get_stats_text()
    await query.message.edit_text(text, reply_markup=main_menu_kb())


@user_router.callback_query(F.data == "settings")
async def cb_settings(query: CallbackQuery) -> None:
    await query.message.edit_text("Settings:", reply_markup=settings_kb())


@user_router.callback_query(F.data == "help")
async def cb_help(query: CallbackQuery) -> None:
    text = (
        "Commands:\n"
        "/start - Main menu\n"
        "/help - This message\n"
        "/profile - Your profile\n"
        "/stats - Statistics\n"
        "/settings - Preferences\n"
        "/feedback - Send feedback\n"
        "/about - About bot\n"
        "/cancel - Cancel operation"
    )
    await query.message.edit_text(text, reply_markup=main_menu_kb())


@user_router.callback_query(F.data == "about")
async def cb_about(query: CallbackQuery) -> None:
    text = (
        "Advanced Modular Bot v1.0\n\n"
        "Layered architecture with aiogram 3.\n"
        "Middleware pipeline, custom filters,"
        " FSM workflows, broadcast system,"
        " usage analytics."
    )
    await query.message.edit_text(text, reply_markup=main_menu_kb())


@user_router.callback_query(F.data == "back_main")
async def cb_back_main(query: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await query.message.edit_text("Main Menu:", reply_markup=main_menu_kb())
