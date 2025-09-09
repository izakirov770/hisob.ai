from aiogram import Router, types, F
from sqlalchemy import select
from datetime import datetime
from database import AsyncSessionLocal
from models import User, Debt, DebtDir
from texts import ALL as TEXTS

router = Router()

KEYWORDS_TAKE = {"olgan", "vzyal", "take"}
KEYWORDS_GIVE = {"bergen", "dal", "give"}

@router.message(F.text)
async def add_debt(m: types.Message):
    text = (m.text or "").strip()
    lowered = text.lower()
    words = lowered.split()

    # Expect patterns like:
    #   "olgan 500000 Ali 2025-09-20"
    #   "bergen 300000 Vali 2025-09-25"
    if len(words) >= 4 and (words[0] in KEYWORDS_TAKE or words[0] in KEYWORDS_GIVE):
        try:
            direction = DebtDir.take if words[0] in KEYWORDS_TAKE else DebtDir.give
            amount = int(words[1])
            person = words[2]
            due_date = datetime.fromisoformat(words[3])
        except Exception:
            # Not a debt command, skip to next handlers
            return

        async with AsyncSessionLocal() as s:
            user = await s.scalar(select(User).where(User.tg_id == m.from_user.id))
            if not user:
                await m.answer("/start")
                return
            d = Debt(user_id=user.id, direction=direction, person=person, amount=amount, due_date=due_date)
            s.add(d)
            await s.commit()
            t = TEXTS[user.lang]
            await m.answer(t["debt_added"])
