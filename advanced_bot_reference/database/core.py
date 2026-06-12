from __future__ import annotations

import logging
import sqlite3
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import AsyncGenerator, AsyncIterator, Dict, List, Optional, Tuple

import aiosqlite

from config import cfg
from database.models import BroadcastModel, GroupModel, StatsModel, UserModel

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    async def connect(self) -> aiosqlite.Connection:
        conn = await aiosqlite.connect(str(self.db_path))
        conn.row_factory = aiosqlite.Row
        await conn.execute("PRAGMA journal_mode=WAL")
        await conn.execute("PRAGMA foreign_keys=ON")
        return conn

    async def setup(self) -> None:
        async with self.conn() as conn:
            await conn.executescript("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_id INTEGER UNIQUE NOT NULL,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    language TEXT DEFAULT 'en',
                    is_premium INTEGER DEFAULT 0,
                    is_banned INTEGER DEFAULT 0,
                    is_admin INTEGER DEFAULT 0,
                    total_commands INTEGER DEFAULT 0,
                    last_activity TEXT,
                    created_at TEXT DEFAULT (datetime('now'))
                );

                CREATE TABLE IF NOT EXISTS groups (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_id INTEGER UNIQUE NOT NULL,
                    title TEXT,
                    username TEXT,
                    member_count INTEGER DEFAULT 0,
                    is_active INTEGER DEFAULT 1,
                    welcome_enabled INTEGER DEFAULT 0,
                    welcome_message TEXT,
                    created_at TEXT DEFAULT (datetime('now'))
                );

                CREATE TABLE IF NOT EXISTS broadcasts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    admin_id INTEGER NOT NULL,
                    message_text TEXT NOT NULL,
                    sent_count INTEGER DEFAULT 0,
                    total_count INTEGER DEFAULT 0,
                    failed_count INTEGER DEFAULT 0,
                    status TEXT DEFAULT 'pending',
                    created_at TEXT DEFAULT (datetime('now')),
                    completed_at TEXT
                );

                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_id INTEGER,
                    command TEXT,
                    args TEXT,
                    timestamp TEXT DEFAULT (datetime('now'))
                );

                CREATE INDEX IF NOT EXISTS idx_users_telegram_id ON users(telegram_id);
                CREATE INDEX IF NOT EXISTS idx_groups_telegram_id ON groups(telegram_id);
                CREATE INDEX IF NOT EXISTS idx_logs_timestamp ON logs(timestamp);
            """)
            await conn.commit()
        logger.info("Database setup complete")

    @asynccontextmanager
    async def conn(self) -> AsyncGenerator[aiosqlite.Connection, None]:
        conn = await self.connect()
        try:
            yield conn
        finally:
            await conn.close()

    # ── User operations ────────────────────────────────────────────

    async def register_user(self, telegram_id: int, **kwargs) -> UserModel:
        async with self.conn() as conn:
            now = datetime.now().isoformat()
            await conn.execute(
                """INSERT INTO users (telegram_id, username, first_name, last_name, last_activity)
                   VALUES (?, ?, ?, ?, ?)
                   ON CONFLICT(telegram_id) DO UPDATE SET
                       username = COALESCE(excluded.username, users.username),
                       first_name = COALESCE(excluded.first_name, users.first_name),
                       last_name = COALESCE(excluded.last_name, users.last_name),
                       last_activity = ?""",
                (
                    telegram_id,
                    kwargs.get("username"),
                    kwargs.get("first_name"),
                    kwargs.get("last_name"),
                    now,
                    now,
                ),
            )
            await conn.commit()
            return await self.get_user(telegram_id)

    async def get_user(self, telegram_id: int) -> Optional[UserModel]:
        async with self.conn() as conn:
            cursor = await conn.execute(
                "SELECT * FROM users WHERE telegram_id = ?", (telegram_id,)
            )
            row = await cursor.fetchone()
            if row is None:
                return None
            return UserModel(**dict(row))

    async def update_user(self, telegram_id: int, **kwargs) -> None:
        allowed = {
            "username", "first_name", "last_name", "language",
            "is_premium", "is_banned", "is_admin", "total_commands", "last_activity",
        }
        updates = {k: v for k, v in kwargs.items() if k in allowed}
        if not updates:
            return
        set_clause = ", ".join(f"{k} = ?" for k in updates)
        values = list(updates.values()) + [telegram_id]
        async with self.conn() as conn:
            await conn.execute(
                f"UPDATE users SET {set_clause} WHERE telegram_id = ?", values
            )
            await conn.commit()

    async def increment_commands(self, telegram_id: int) -> None:
        async with self.conn() as conn:
            await conn.execute(
                """UPDATE users SET total_commands = total_commands + 1,
                   last_activity = datetime('now') WHERE telegram_id = ?""",
                (telegram_id,),
            )
            await conn.commit()

    async def get_all_users(self, only_active: bool = False) -> List[UserModel]:
        async with self.conn() as conn:
            query = "SELECT * FROM users"
            params: Tuple = ()
            if only_active:
                query += " WHERE is_banned = 0"
            cursor = await conn.execute(query, params)
            rows = await cursor.fetchall()
            return [UserModel(**dict(r)) for r in rows]

    async def get_user_count(self) -> int:
        async with self.conn() as conn:
            cursor = await conn.execute("SELECT COUNT(*) FROM users")
            return (await cursor.fetchone())[0]

    async def get_active_today_count(self) -> int:
        async with self.conn() as conn:
            cursor = await conn.execute(
                "SELECT COUNT(*) FROM users WHERE last_activity >= datetime('now', '-1 day')"
            )
            return (await cursor.fetchone())[0]

    async def get_new_today_count(self) -> int:
        async with self.conn() as conn:
            cursor = await conn.execute(
                "SELECT COUNT(*) FROM users WHERE created_at >= datetime('now', '-1 day')"
            )
            return (await cursor.fetchone())[0]

    # ── Group operations ───────────────────────────────────────────

    async def register_group(self, telegram_id: int, **kwargs) -> GroupModel:
        async with self.conn() as conn:
            await conn.execute(
                """INSERT INTO groups (telegram_id, title, username, member_count)
                   VALUES (?, ?, ?, ?)
                   ON CONFLICT(telegram_id) DO UPDATE SET
                       title = COALESCE(excluded.title, groups.title),
                       username = COALESCE(excluded.username, groups.username),
                       is_active = 1""",
                (
                    telegram_id,
                    kwargs.get("title"),
                    kwargs.get("username"),
                    kwargs.get("member_count", 0),
                ),
            )
            await conn.commit()
            return await self.get_group(telegram_id)

    async def get_group(self, telegram_id: int) -> Optional[GroupModel]:
        async with self.conn() as conn:
            cursor = await conn.execute(
                "SELECT * FROM groups WHERE telegram_id = ?", (telegram_id,)
            )
            row = await cursor.fetchone()
            if row is None:
                return None
            return GroupModel(**dict(row))

    async def update_group(self, telegram_id: int, **kwargs) -> None:
        allowed = {
            "title", "username", "member_count", "is_active",
            "welcome_enabled", "welcome_message",
        }
        updates = {k: v for k, v in kwargs.items() if k in allowed}
        if not updates:
            return
        set_clause = ", ".join(f"{k} = ?" for k in updates)
        values = list(updates.values()) + [telegram_id]
        async with self.conn() as conn:
            await conn.execute(
                f"UPDATE groups SET {set_clause} WHERE telegram_id = ?", values
            )
            await conn.commit()

    async def get_all_groups(self) -> List[GroupModel]:
        async with self.conn() as conn:
            cursor = await conn.execute("SELECT * FROM groups WHERE is_active = 1")
            rows = await cursor.fetchall()
            return [GroupModel(**dict(r)) for r in rows]

    async def get_group_count(self) -> int:
        async with self.conn() as conn:
            cursor = await conn.execute(
                "SELECT COUNT(*) FROM groups WHERE is_active = 1"
            )
            return (await cursor.fetchone())[0]

    # ── Broadcast operations ───────────────────────────────────────

    async def create_broadcast(
        self, admin_id: int, text: str, total: int
    ) -> int:
        async with self.conn() as conn:
            cursor = await conn.execute(
                """INSERT INTO broadcasts (admin_id, message_text, total_count)
                   VALUES (?, ?, ?)""",
                (admin_id, text, total),
            )
            await conn.commit()
            return cursor.lastrowid

    async def update_broadcast(
        self, broadcast_id: int, **kwargs
    ) -> None:
        allowed = {"sent_count", "failed_count", "status", "completed_at"}
        updates = {k: v for k, v in kwargs.items() if k in allowed}
        if not updates:
            return
        set_clause = ", ".join(f"{k} = ?" for k in updates)
        values = list(updates.values()) + [broadcast_id]
        async with self.conn() as conn:
            await conn.execute(
                f"UPDATE broadcasts SET {set_clause} WHERE id = ?", values
            )
            await conn.commit()

    async def get_broadcasts(
        self, limit: int = 10
    ) -> List[BroadcastModel]:
        async with self.conn() as conn:
            cursor = await conn.execute(
                "SELECT * FROM broadcasts ORDER BY created_at DESC LIMIT ?",
                (limit,),
            )
            rows = await cursor.fetchall()
            return [BroadcastModel(**dict(r)) for r in rows]

    # ── Log operations ─────────────────────────────────────────────

    async def log_command(
        self, telegram_id: int, command: str, args: str = ""
    ) -> None:
        async with self.conn() as conn:
            await conn.execute(
                "INSERT INTO logs (telegram_id, command, args) VALUES (?, ?, ?)",
                (telegram_id, command, args),
            )
            await conn.commit()

    async def get_top_commands(self, limit: int = 10) -> List[Dict]:
        async with self.conn() as conn:
            cursor = await conn.execute(
                """SELECT command, COUNT(*) as count
                   FROM logs
                   GROUP BY command
                   ORDER BY count DESC
                   LIMIT ?""",
                (limit,),
            )
            rows = await cursor.fetchall()
            return [dict(r) for r in rows]

    async def get_command_count(self) -> int:
        async with self.conn() as conn:
            cursor = await conn.execute("SELECT COUNT(*) FROM logs")
            return (await cursor.fetchone())[0]

    # ── Stats ──────────────────────────────────────────────────────

    async def get_stats(self) -> StatsModel:
        total_users = await self.get_user_count()
        total_groups = await self.get_group_count()
        total_commands = await self.get_command_count()
        active_today = await self.get_active_today_count()
        new_today = await self.get_new_today_count()
        return StatsModel(
            total_users=total_users,
            total_groups=total_groups,
            total_commands=total_commands,
            active_today=active_today,
            new_today=new_today,
        )


_db: Optional[Database] = None


def get_db() -> Database:
    global _db
    if _db is None:
        _db = Database(cfg.DB_PATH)
    return _db
