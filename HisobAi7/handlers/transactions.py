from aiogram import Router, types, F
from sqlalchemy import select
from database import AsyncSessionLocal
from models import User, Transaction, TxType
from texts import ALL as TEXTS
from services.categorizer import guess_category

router = Router()

# Format: "+12000 coffee" or "-50000 taxi"
@router.message(F.text.regexp(r"^[\+\-]\s*\d+"))
async def parse_text_tx(m: types.Message):
    text = m.text.strip()
    sign = 1 if text.startswith("+") else -1
    body = text[1:].strip()
    parts = body.split(maxsplit=1)
    amount = int(parts[0])
    note = parts[1] if len(parts) > 1 else ""

    async with AsyncSessionLocal() as s:
        user = await s.scalar(select(User).where(User.tg_id == m.from_user.id))
        if not user:
            await m.answer("/start")
            return
        category = guess_category(note, default="other")
        tx = Transaction(
            user_id=user.id,
            type=TxType.income if sign == 1 else TxType.expense,
            amount=abs(amount),
            category=category,
            note=note,
        )
        s.add(tx)
        await s.commit()
        t = TEXTS[user.lang]
        await m.answer(t["saved"])

@router.message(F.voice)
async def handle_voice(m: types.Message):
    async with AsyncSessionLocal() as s:
        user = await s.scalar(select(User).where(User.tg_id == m.from_user.id))
        lang = user.lang if user else "uz"
    t = TEXTS[lang]
    await m.answer(t["ask_text_tx"] + "\n\n(🎙️ Ovozdan matn: STT hozircha o‘chirilgan — keyinchalik yoqamiz)")

@router.message(F.photo)
async def handle_receipt(m: types.Message):
    async with AsyncSessionLocal() as s:
        user = await s.scalar(select(User).where(User.tg_id == m.from_user.id))
        lang = user.lang if user else "uz"
    t = TEXTS[lang]
    await m.answer(t["ask_text_tx"] + "\n\n(🧾 Chek OCR: hozircha o‘chirilgan — keyinchalik yoqamiz)")
