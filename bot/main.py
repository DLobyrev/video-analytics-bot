import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from core.config import settings
from core.database import db
from bot.handlers import router


async def on_startup(bot: Bot):
    await db.connect()
    await bot.set_my_commands([BotCommand(command="start", description="Начать работу")])
    logging.info("Bot started")


async def on_shutdown(bot: Bot):
    await db.disconnect()
    logging.info("Bot stopped")


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=settings.telegram_bot_token)
    dp = Dispatcher()
    dp.include_router(router)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
