from __future__ import annotations

import asyncio
import logging
from datetime import datetime
from typing import List

from aiogram import Bot
from aiogram.exceptions import (
    TelegramForbiddenError,
    TelegramRetryAfter,
    TelegramBadRequest,
)

from database import get_db

logger = logging.getLogger(__name__)


class BroadcastService:
    def __init__(self, bot: Bot):
        self.bot = bot
        self._is_running = False

    async def send_to_user(
        self, user_id: int, text: str, keyboard=None
    ) -> bool:
        try:
            await self.bot.send_message(
                chat_id=user_id,
                text=text,
                reply_markup=keyboard,
            )
            return True
        except TelegramForbiddenError:
            db = get_db()
            await db.update_user(user_id, is_banned=True)
            return False
        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after)
            return await self.send_to_user(user_id, text, keyboard)
        except TelegramBadRequest:
            return False
        except Exception as e:
            logger.error(f"Broadcast send error to {user_id}: {e}")
            return False

    async def broadcast(
        self,
        text: str,
        admin_id: int,
        target_ids: List[int] = None,
    ) -> int:
        self._is_running = True
        db = get_db()

        if target_ids is None:
            users = await db.get_all_users(only_active=True)
            target_ids = [u.telegram_id for u in users]

        broadcast_id = await db.create_broadcast(admin_id, text, len(target_ids))

        sent = 0
        failed = 0

        for i, user_id in enumerate(target_ids):
            if not self._is_running:
                break
            success = await self.send_to_user(user_id, text)
            if success:
                sent += 1
            else:
                failed += 1

            if i > 0 and i % 10 == 0:
                await db.update_broadcast(
                    broadcast_id,
                    sent_count=sent,
                    failed_count=failed,
                )

            await asyncio.sleep(0.05)

        await db.update_broadcast(
            broadcast_id,
            sent_count=sent,
            failed_count=failed,
            status="completed",
            completed_at=datetime.now().isoformat(),
        )

        self._is_running = False
        return sent

    def cancel(self) -> None:
        self._is_running = False
