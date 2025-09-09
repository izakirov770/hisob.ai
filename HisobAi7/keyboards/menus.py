from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu(t: dict) -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text=t["btn_add_income"]), KeyboardButton(text=t["btn_add_expense"])],
        [KeyboardButton(text=t["btn_report"]), KeyboardButton(text=t["btn_debt"])],
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
