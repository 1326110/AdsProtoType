from __future__ import annotations

from typing import List, Optional, Tuple

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)


class KeyboardBuilder:
    @staticmethod
    def inline(
        buttons: List[List[Tuple[str, str]]],
        resize: bool = True,
    ) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=text, callback_data=data)
                    for text, data in row
                ]
                for row in buttons
            ]
        )

    @staticmethod
    def url_inline(
        buttons: List[List[Tuple[str, str]]],
    ) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=text, url=url)
                    for text, url in row
                ]
                for row in buttons
            ]
        )

    @staticmethod
    def reply(
        buttons: List[List[str]],
        resize: bool = True,
        one_time: bool = False,
        selective: bool = False,
    ) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=text) for text in row]
                for row in buttons
            ],
            resize_keyboard=resize,
            one_time_keyboard=one_time,
            selective=selective,
        )

    @staticmethod
    def remove() -> ReplyKeyboardRemove:
        return ReplyKeyboardRemove()


def main_menu_kb() -> InlineKeyboardMarkup:
    return KeyboardBuilder.inline([
        [("Profile", "profile"), ("Stats", "stats")],
        [("Settings", "settings"), ("Help", "help")],
        [("About", "about")],
    ])


def admin_menu_kb() -> InlineKeyboardMarkup:
    return KeyboardBuilder.inline([
        [("Dashboard", "admin_dashboard"), ("Broadcast", "admin_broadcast")],
        [("Users", "admin_users"), ("Groups", "admin_groups")],
        [("Logs", "admin_logs"), ("Back to Menu", "back_main")],
    ])


def cancel_kb() -> ReplyKeyboardMarkup:
    return KeyboardBuilder.reply([["Cancel"]])


def confirm_kb(data_yes: str, data_no: str) -> InlineKeyboardMarkup:
    return KeyboardBuilder.inline([
        [("Yes", data_yes), ("No", data_no)],
    ])


def settings_kb() -> InlineKeyboardMarkup:
    return KeyboardBuilder.inline([
        [("Language", "set_language")],
        [("Back", "back_main")],
    ])
