from aiogram import Router, types, F
from aiogram.filters import CommandStart
from sqlalchemy import select
from database import AsyncSessionLocal
from models import User
from texts import ALL as TEXTS
from keyboards.menus import main_menu

router = Router()

@router.message(CommandStart())
async def start_cmd(m: types.Message):
    lang_kb = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[[types.KeyboardButton(text="uz"), types.KeyboardButton(text="ru"), types.KeyboardButton(text="en")]]
    )
    await m.answer("Til / Язык / Language: uz | ru | en", reply_markup=lang_kb)

@router.message(F.text.in_({"uz", "ru", "en"}))
async def set_lang(m: types.Message):
    lang = m.text
    async with AsyncSessionLocal() as s:
        user = await s.scalar(select(User).where(User.tg_id == m.from_user.id))
        if not user:
            user = User(tg_id=m.from_user.id, lang=lang)
            s.add(user)
        else:
            user.lang = lang
        await s.commit()

    t = TEXTS[lang]
    await m.answer(t["hello"], reply_markup=main_menu(t))
    await m.answer(t["menu"])
