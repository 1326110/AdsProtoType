from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class UserModel:
    id: int
    telegram_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    language: str = "en"
    is_premium: bool = False
    is_banned: bool = False
    is_admin: bool = False
    total_commands: int = 0
    last_activity: Optional[str] = None
    created_at: Optional[str] = None


@dataclass
class GroupModel:
    id: int
    telegram_id: int
    title: Optional[str] = None
    username: Optional[str] = None
    member_count: int = 0
    is_active: bool = True
    welcome_enabled: bool = False
    welcome_message: Optional[str] = None
    created_at: Optional[str] = None


@dataclass
class BroadcastModel:
    id: int
    admin_id: int
    message_text: str
    sent_count: int = 0
    total_count: int = 0
    failed_count: int = 0
    status: str = "pending"
    created_at: Optional[str] = None
    completed_at: Optional[str] = None


@dataclass
class StatsModel:
    total_users: int = 0
    total_groups: int = 0
    total_commands: int = 0
    active_today: int = 0
    new_today: int = 0
