from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from dotenv import load_dotenv

load_dotenv()


class ConfigError(Exception):
    pass


@dataclass(frozen=True, slots=True)
class Config:
    BOT_TOKEN: str
    ADMIN_IDS: List[int] = field(default_factory=list)
    BOT_MODE: str = "polling"
    WEBHOOK_URL: str = ""
    WEBHOOK_PORT: int = 8443
    DB_PATH: Path = Path(__file__).parent / "data" / "bot.db"
    LOG_LEVEL: str = "INFO"
    SKIP_UPDATES: bool = True
    THROTTLE_RATE: float = 0.5
    DEFAULT_LANGUAGE: str = "en"

    @classmethod
    def from_env(cls) -> Config:
        token = os.getenv("BOT_TOKEN", "")
        if not token:
            raise ConfigError(
                "BOT_TOKEN is required! "
                "Create a .env file or set the environment variable."
            )

        raw_admins = os.getenv("ADMIN_IDS", "")
        admin_ids: List[int] = []
        for part in raw_admins.split(","):
            part = part.strip()
            if part:
                try:
                    admin_ids.append(int(part))
                except ValueError:
                    print(f"[WARN] Invalid ADMIN_ID: {part}")

        return cls(
            BOT_TOKEN=token,
            ADMIN_IDS=admin_ids,
            BOT_MODE=os.getenv("BOT_MODE", "polling").strip().lower(),
            WEBHOOK_URL=os.getenv("WEBHOOK_URL", "").strip(),
            WEBHOOK_PORT=int(os.getenv("WEBHOOK_PORT", "8443")),
            LOG_LEVEL=os.getenv("LOG_LEVEL", "INFO").upper(),
            SKIP_UPDATES=os.getenv("SKIP_UPDATES", "true").lower() == "true",
            THROTTLE_RATE=float(os.getenv("THROTTLE_RATE", "0.5")),
            DEFAULT_LANGUAGE=os.getenv("DEFAULT_LANGUAGE", "en"),
        )

    @property
    def is_webhook(self) -> bool:
        return self.BOT_MODE == "webhook" and bool(self.WEBHOOK_URL)


cfg = Config.from_env()
