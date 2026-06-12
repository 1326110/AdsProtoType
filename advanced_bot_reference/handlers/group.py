from __future__ import annotations

import logging

from aiogram import F, Router
from aiogram.filters import Command, ChatMemberUpdatedFilter, KICKED, MEMBER
from aiogram.types import ChatMemberUpdated, Message

from database import get_db

logger = logging.getLogger(__name__)

group_router = Router()
group_router.message.filter(F.chat.type.in_({"group", "supergroup"}))


@group_router.message(Command("start"))
async def group_start(message: Message) -> None:
    db = get_db()
    await db.register_group(
        telegram_id=message.chat.id,
        title=message.chat.title,
        username=message.chat.username,
    )
    await message.answer(
        "Hello! I'm active in this group. "
        "Use /help to see available commands."
    )


@group_router.my_chat_member(ChatMemberUpdatedFilter(KICKED))
async def on_group_kick(event: ChatMemberUpdated) -> None:
    db = get_db()
    await db.update_group(
        telegram_id=event.chat.id,
        is_active=False,
    )
    logger.info(f"Bot removed from group {event.chat.id}")


@group_router.my_chat_member(ChatMemberUpdatedFilter(MEMBER))
async def on_group_join(event: ChatMemberUpdated) -> None:
    db = get_db()
    await db.register_group(
        telegram_id=event.chat.id,
        title=event.chat.title,
        username=event.chat.username,
    )
    logger.info(f"Bot added to group {event.chat.id} ({event.chat.title})")
