from aiogram import Dispatcher, Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy import select
from datetime import datetime, timedelta
import pytz

from config import settings
from database import AsyncSessionLocal
from models import User, Debt
from texts import ALL as TEXTS

_scheduler: AsyncIOScheduler | None = None

async def setup_reminders(dp: Dispatcher, bot: Bot):
    global _scheduler
    if _scheduler:
        return _scheduler

    _scheduler = AsyncIOScheduler(timezone=settings.TIMEZONE)

    # Daily 20:00 reminder
    _scheduler.add_job(lambda: daily_ping(bot), CronTrigger(hour=20, minute=0))

    # Debt reminders — every 60 minutes
    _scheduler.add_job(lambda: debt_ping(bot), CronTrigger(minute=0))

    _scheduler.start()

async def daily_ping(bot: Bot):
    async with AsyncSessionLocal() as s:
        users = (await s.execute(select(User))).scalars().all()
        for u in users:
            t = TEXTS[u.lang]
            try:
                await bot.send_message(chat_id=u.tg_id, text=t["daily_reminder"])
            except Exception:
                pass

async def debt_ping(bot: Bot):
    tz = pytz.timezone(settings.TIMEZONE)
    now = datetime.now(tz)
    soon = now + timedelta(days=1)
    async with AsyncSessionLocal() as s:
        debts = (await s.execute(select(Debt).where(Debt.is_closed == False))).scalars().all()
        for d in debts:
            due = d.due_date
            if due.tzinfo is None:
                due = tz.localize(due)
            else:
                due = due.astimezone(tz)
            if now <= due <= soon:
                u = await s.get(User, d.user_id)
                if u is None:
                    continue
                msg = f"⏰ Qarz eslatmasi: {d.person} — {d.amount} — {due.strftime('%Y-%m-%d %H:%M')}"
                if u.lang == "ru":
                    msg = f"⏰ Напоминание о долге: {d.person} — {d.amount} — {due.strftime('%Y-%m-%d %H:%M')}"
                if u.lang == "en":
                    msg = f"⏰ Debt reminder: {d.person} — {d.amount} — {due.strftime('%Y-%m-%d %H:%M')}"
                try:
                    await bot.send_message(u.tg_id, msg)
                except Exception:
                    pass
