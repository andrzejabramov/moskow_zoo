from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, FSInputFile
from aiogram.filters import Command
from pathlib import Path

router = Router()

# Путь к логотипу относительно этого файла
LOGO_PATH = Path(__file__).parent.parent / "assets" / "logo.jpg"

@router.message(Command("start"))
@router.message(F.text == "Старт")  # ← обрабатываем нажатие кнопки
async def cmd_start(message: Message):
    if not LOGO_PATH.exists():
        await message.answer("❌ Ошибка: логотип не найден!")
        return

    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Старт")]],
        resize_keyboard=True
    )

    try:
        await message.answer_photo(
            photo=FSInputFile(LOGO_PATH),
            caption="Вас приветствует Московский Зоопарк",
            reply_markup=keyboard
        )
    except Exception as e:
        await message.answer(f"❌ Ошибка при отправке фото: {e}")