from __future__ import annotations

import logging
import traceback

from aiogram import F, Router
from aiogram.exceptions import (
    TelegramBadRequest,
    TelegramForbiddenError,
    TelegramNetworkError,
    TelegramRetryAfter,
    TelegramUnauthorizedError,
)
from aiogram.types import CallbackQuery, ErrorEvent, Message

from bot import bot
from config import cfg

logger = logging.getLogger(__name__)

error_router = Router(name="errors")


@error_router.errors()
async def global_error_handler(event: ErrorEvent) -> None:
    exc = event.exception
    update = event.update

    logger.error(
        "Global error: %s\n%s",
        exc,
        "".join(traceback.format_exception(type(exc), exc, exc.__traceback__)),
    )

    user_id = None
    if update.message:
        user_id = update.message.from_user.id
    elif update.callback_query:
        user_id = update.callback_query.from_user.id

    error_text = (
        "An unexpected error occurred. Please try again later."
    )

    if user_id:
        try:
            await bot.send_message(user_id, error_text)
        except Exception:
            pass

    for admin_id in cfg.ADMIN_IDS:
        try:
            await bot.send_message(
                admin_id,
                f"Error:\n"
                f"  Type: {type(exc).__name__}\n"
                f"  Detail: {exc}\n"
                f"  User: {user_id}",
            )
        except Exception:
            pass


@error_router.message(F.text)
async def unhandled_message(message: Message) -> None:
    if message.text and not message.text.startswith("/"):
        return
    await message.answer(
        "Unknown command. Use /help to see available commands."
    )
