# keyboards/quiz_kb.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

attitude_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="❤️ Люблю", callback_data="attitude:love"),
        InlineKeyboardButton(text="😐 Равнодушен", callback_data="attitude:neutral"),
        InlineKeyboardButton(text="❌ Не люблю", callback_data="attitude:hate")
    ]
])