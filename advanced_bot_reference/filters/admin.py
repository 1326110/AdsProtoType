from __future__ import annotations

from typing import Union

from aiogram.filters import Filter
from aiogram.types import CallbackQuery, Message, User

from config import cfg
from database import get_db


class AdminFilter(Filter):
    key = "is_admin"

    async def __call__(
        self, event: Union[Message, CallbackQuery], user: User | None = None
    ) -> bool:
        if user is None:
            event_user = getattr(event, "from_user", None)
            if event_user is None:
                return False
            user = event_user
        if user.id in cfg.ADMIN_IDS:
            return True
        db = get_db()
        db_user = await db.get_user(user.id)
        return db_user is not None and db_user.is_admin


class PremiumFilter(Filter):
    key = "is_premium"

    async def __call__(
        self, event: Union[Message, CallbackQuery], user: User | None = None
    ) -> bool:
        if user is None:
            event_user = getattr(event, "from_user", None)
            if event_user is None:
                return False
            user = event_user
        db = get_db()
        db_user = await db.get_user(user.id)
        return db_user is not None and db_user.is_premium


class NotBannedFilter(Filter):
    key = "not_banned"

    async def __call__(
        self, event: Union[Message, CallbackQuery], user: User | None = None
    ) -> bool:
        if user is None:
            event_user = getattr(event, "from_user", None)
            if event_user is None:
                return False
            user = event_user
        db = get_db()
        db_user = await db.get_user(user.id)
        if db_user is None:
            return True
        return not db_user.is_banned
