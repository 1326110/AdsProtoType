from __future__ import annotations

import asyncio
import logging
import sys

from aiogram.enums import ChatAction
from aiogram.types import BotCommand, BotCommandScopeDefault

from bot import bot, dp
from bot.middlewares import (
    ChatActionMiddleware,
    CommandLoggingMiddleware,
    ThrottlingMiddleware,
    UserRegistrationMiddleware,
)
from config import cfg
from database import get_db
from handlers import register_all_routers


def setup_logging() -> None:
    logging.basicConfig(
        level=getattr(logging, cfg.LOG_LEVEL, logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
    )


async def setup_bot_commands() -> None:
    commands = [
        BotCommand(command="start", description="Main menu"),
        BotCommand(command="help", description="Show help"),
        BotCommand(command="profile", description="Your profile"),
        BotCommand(command="stats", description="System stats"),
        BotCommand(command="settings", description="Change settings"),
        BotCommand(command="feedback", description="Send feedback"),
        BotCommand(command="about", description="About this bot"),
        BotCommand(command="cancel", description="Cancel operation"),
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())


def register_middlewares() -> None:
    dp.message.middleware(ThrottlingMiddleware(rate=cfg.THROTTLE_RATE))
    dp.callback_query.middleware(ThrottlingMiddleware(rate=cfg.THROTTLE_RATE))
    dp.message.middleware(UserRegistrationMiddleware())
    dp.callback_query.middleware(UserRegistrationMiddleware())
    dp.message.middleware(CommandLoggingMiddleware())
    dp.callback_query.middleware(ChatActionMiddleware())


async def on_startup() -> None:
    db = get_db()
    await db.setup()
    await setup_bot_commands()
    register_middlewares()
    register_all_routers(dp)
    logging.info("Bot started successfully")


async def on_shutdown() -> None:
    logging.info("Bot shutting down...")
    await bot.session.close()


async def main() -> None:
    setup_logging()

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    logging.info(
        "Starting bot in %s mode...",
        "webhook" if cfg.is_webhook else "polling",
    )

    if cfg.SKIP_UPDATES:
        await bot.delete_webhook(drop_pending_updates=True)

    if cfg.is_webhook:
        await bot.set_webhook(
            url=cfg.WEBHOOK_URL,
            drop_pending_updates=cfg.SKIP_UPDATES,
        )
        await dp.start_webhook(
            dispatcher=dp,
            bot=bot,
            webhook_path="/webhook",
            host="0.0.0.0",
            port=cfg.WEBHOOK_PORT,
        )
    else:
        await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
