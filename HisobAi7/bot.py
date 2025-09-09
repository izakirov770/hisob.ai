import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import settings
from database import init_db
from handlers.start import router as start_router
from handlers.transactions import router as tx_router
from handlers.debts import router as debts_router
from handlers.reports import router as reports_router
from handlers.reminders import setup_reminders

async def main():
    logging.basicConfig(level=logging.INFO)

    await init_db()

    bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(start_router)
    dp.include_router(tx_router)
    dp.include_router(debts_router)
    dp.include_router(reports_router)

    await setup_reminders(dp, bot)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
