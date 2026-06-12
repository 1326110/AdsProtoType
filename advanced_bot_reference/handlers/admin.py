from __future__ import annotations

import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from bot import bot
from database import get_db
from filters import AdminFilter
from keyboards import (
    KeyboardBuilder,
    admin_menu_kb,
    confirm_kb,
    main_menu_kb,
)
from services import BroadcastService, StatsService

logger = logging.getLogger(__name__)

admin_router = Router()
admin_router.message.filter(AdminFilter())
admin_router.callback_query.filter(AdminFilter())


class BroadcastForm(StatesGroup):
    waiting_for_text = State()
    waiting_for_confirm = State()


# ── Admin panel ────────────────────────────────────────────────────

@admin_router.message(Command("admin"))
async def cmd_admin(message: Message) -> None:
    text = (
        "Admin Panel\n\n"
        "Use the menu below or:\n"
        "/admin - Open this panel\n"
        "/broadcast - Send broadcast\n"
        "/stats - View statistics\n"
        "/users - List users\n"
        "/ban <id> - Ban user\n"
        "/unban <id> - Unban user"
    )
    await message.answer(text, reply_markup=admin_menu_kb())


# ── Dashboard ──────────────────────────────────────────────────────

@admin_router.callback_query(F.data == "admin_dashboard")
async def admin_dashboard(query: CallbackQuery) -> None:
    from services import StatsService
    text = await StatsService.get_stats_text()
    await query.message.edit_text(text, reply_markup=admin_menu_kb())


# ── Broadcast ──────────────────────────────────────────────────────

@admin_router.callback_query(F.data == "admin_broadcast")
async def admin_broadcast_start(query: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(BroadcastForm.waiting_for_text)
    await query.message.edit_text(
        "Send the message to broadcast to all users:",
    )


@admin_router.message(BroadcastForm.waiting_for_text, F.text)
async def admin_broadcast_preview(message: Message, state: FSMContext) -> None:
    await state.update_data(text=message.text)
    await state.set_state(BroadcastForm.waiting_for_confirm)

    db = get_db()
    count = await db.get_user_count()

    await message.answer(
        f"Preview:\n\n{message.text}\n\n"
        f"Will be sent to {count} users. Confirm?",
        reply_markup=confirm_kb("broadcast_confirm", "broadcast_cancel"),
    )


@admin_router.message(BroadcastForm.waiting_for_text)
async def admin_broadcast_invalid(message: Message) -> None:
    await message.answer("Please send text, or /cancel to exit.")


@admin_router.callback_query(F.data == "broadcast_confirm")
async def admin_broadcast_execute(query: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    text = data.get("text", "")
    await state.clear()

    await query.message.edit_text("Broadcasting... This may take a while.")

    service = BroadcastService(bot)
    sent = await service.broadcast(text, query.from_user.id)

    await query.message.edit_text(
        f"Broadcast complete!\nSent to {sent} users.",
        reply_markup=admin_menu_kb(),
    )


@admin_router.callback_query(F.data == "broadcast_cancel")
async def admin_broadcast_cancel(query: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await query.message.edit_text(
        "Broadcast cancelled.",
        reply_markup=admin_menu_kb(),
    )


# ── Users ──────────────────────────────────────────────────────────

@admin_router.callback_query(F.data == "admin_users")
async def admin_users_list(query: CallbackQuery) -> None:
    db = get_db()
    users = await db.get_all_users()
    total = len(users)
    banned = sum(1 for u in users if u.is_banned)
    admins = sum(1 for u in users if u.is_admin)
    premium = sum(1 for u in users if u.is_premium)

    text = (
        f"Users: {total}\n"
        f"Admins: {admins}\n"
        f"Premium: {premium}\n"
        f"Banned: {banned}\n\n"
        "Use /ban <id>, /unban <id>, /premium <id>"
    )
    await query.message.edit_text(text, reply_markup=admin_menu_kb())


@admin_router.message(Command("ban"))
async def admin_ban(message: Message) -> None:
    args = message.text.split()
    if len(args) < 2:
        await message.answer("Usage: /ban <user_id>")
        return
    try:
        user_id = int(args[1])
    except ValueError:
        await message.answer("Invalid user ID.")
        return

    db = get_db()
    await db.update_user(user_id, is_banned=True)
    await message.answer(f"User {user_id} has been banned.")


@admin_router.message(Command("unban"))
async def admin_unban(message: Message) -> None:
    args = message.text.split()
    if len(args) < 2:
        await message.answer("Usage: /unban <user_id>")
        return
    try:
        user_id = int(args[1])
    except ValueError:
        await message.answer("Invalid user ID.")
        return

    db = get_db()
    await db.update_user(user_id, is_banned=False)
    await message.answer(f"User {user_id} has been unbanned.")


@admin_router.message(Command("premium"))
async def admin_premium(message: Message) -> None:
    args = message.text.split()
    if len(args) < 2:
        await message.answer("Usage: /premium <user_id>")
        return
    try:
        user_id = int(args[1])
    except ValueError:
        await message.answer("Invalid user ID.")
        return

    db = get_db()
    user = await db.get_user(user_id)
    if user is None:
        await message.answer("User not found.")
        return

    await db.update_user(user_id, is_premium=not user.is_premium)
    status = "promoted" if not user.is_premium else "demoted"
    await message.answer(f"User {user_id} {status} {'to' if not user.is_premium else 'from'} premium.")


# ── Groups ─────────────────────────────────────────────────────────

@admin_router.callback_query(F.data == "admin_groups")
async def admin_groups_list(query: CallbackQuery) -> None:
    db = get_db()
    groups = await db.get_all_groups()
    text = (
        f"Active groups: {len(groups)}\n\n"
        + "\n".join(
            f"  {g.title or 'N/A'} (ID: {g.telegram_id})"
            for g in groups[:20]
        )
    )
    if len(groups) > 20:
        text += f"\n... and {len(groups) - 20} more"
    await query.message.edit_text(text, reply_markup=admin_menu_kb())


# ── Logs ───────────────────────────────────────────────────────────

@admin_router.callback_query(F.data == "admin_logs")
async def admin_logs(query: CallbackQuery) -> None:
    db = get_db()
    top = await db.get_top_commands(10)
    text = "Top commands:\n\n" + "\n".join(
        f"  /{c['command']}: {c['count']}x" for c in top
    )
    await query.message.edit_text(text, reply_markup=admin_menu_kb())
