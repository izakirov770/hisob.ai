from aiogram import Router, types, F
from sqlalchemy import select, func
from datetime import datetime, timedelta
from database import AsyncSessionLocal
from models import User, Transaction, TxType
from texts import ALL as TEXTS

router = Router()

@router.message(F.text.in_({"📊 Hisobot", "📊 Отчет", "📊 Report", "Hisobot", "Отчет", "Report"}))
async def report_menu(m: types.Message):
    now = datetime.now()
    periods = {
        "today": (now.replace(hour=0, minute=0, second=0, microsecond=0), now),
        "week": (now - timedelta(days=7), now),
        "month": (now - timedelta(days=30), now),
    }
    async with AsyncSessionLocal() as s:
        user = await s.scalar(select(User).where(User.tg_id == m.from_user.id))
        if not user:
            await m.answer("/start")
            return
        t = TEXTS[user.lang]
        text_lines = [t["report_title"]]
        for key, (a, b) in periods.items():
            inc = await s.scalar(
                select(func.coalesce(func.sum(Transaction.amount), 0)).where(
                    Transaction.user_id==user.id,
                    Transaction.type==TxType.income,
                    Transaction.created_at.between(a,b)
                )
            )
            exp = await s.scalar(
                select(func.coalesce(func.sum(Transaction.amount), 0)).where(
                    Transaction.user_id==user.id,
                    Transaction.type==TxType.expense,
                    Transaction.created_at.between(a,b)
                )
            )
            text_lines.append(f"{key}: +{inc} / -{exp}")
        await m.answer("\n".join(text_lines))
