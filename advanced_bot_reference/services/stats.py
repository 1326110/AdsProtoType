from __future__ import annotations

from database import get_db
from database.models import StatsModel


class StatsService:
    @staticmethod
    async def get_stats_text() -> str:
        db = get_db()
        stats = await db.get_stats()
        top_cmds = await db.get_top_commands(5)

        parts = [
            "System Statistics",
            "",
            f"Users: {stats.total_users}",
            f"  Active today: {stats.active_today}",
            f"  New today: {stats.new_today}",
            f"Groups: {stats.total_groups}",
            f"Total commands: {stats.total_commands}",
            "",
            "Top commands:",
        ]

        for cmd in top_cmds:
            parts.append(f"  /{cmd['command']}: {cmd['count']}x")

        return "\n".join(parts)
