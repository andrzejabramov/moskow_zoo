# handlers/animal_quiz.py
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from pathlib import Path

from src.states.quiz import AnimalQuiz
from src.keyboards.quiz import attitude_kb

router = Router()

ASSETS = Path(__file__).parent.parent / "assets"

# Inline-клавиатура для вопроса
# attitude_kb = InlineKeyboardMarkup(inline_keyboard=[
#     [
#         InlineKeyboardButton(text="❤️ Люблю", callback_data="attitude:love"),
#         InlineKeyboardButton(text="😐 Равнодушен", callback_data="attitude:neutral"),
#         InlineKeyboardButton(text="❌ Не люблю", callback_data="attitude:hate")
#     ]
# ])

@router.message(F.text == "Старт")
@router.message(F.text == "/start")
async def handle_start(message: Message, state: FSMContext, bot: Bot):
    # 1. Отправляем приветствие с логотипом (как раньше)
    logo_path = ASSETS / "logo.jpg"
    if not logo_path.exists():
        await message.answer("❌ Логотип не найден!")
        return

    await message.answer_photo(
        photo=FSInputFile(logo_path),
        caption="Вас приветствует Московский Зоопарк"
    )

    # 2. Сразу задаём игровой вопрос
    await message.answer(
        "🐾 Ты любишь животных?",
        reply_markup=attitude_kb
    )

    # 3. Устанавливаем состояние FSM
    await state.set_state(AnimalQuiz.waiting_for_attitude)

# Обработка выбора
@router.callback_query(F.data.startswith("attitude:"), AnimalQuiz.waiting_for_attitude)
async def handle_attitude(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.answer()
    attitude = callback.data.split(":")[1]

    if attitude == "love":
        await bot.send_photo(
            chat_id=callback.message.chat.id,
            photo=FSInputFile(ASSETS / "fireworks.jpg"),
            caption="🎉 Ура! Ты настоящий друг животных!\nВ подарок — виртуальный фейерверк! 🎆\n(Бонус будет доступен позже!)"
        )

    elif attitude == "neutral":
        await bot.send_photo(
            chat_id=callback.message.chat.id,
            photo=FSInputFile(ASSETS / "cute_pet.jpg"),
            caption="🥺 Разве можно быть равнодушным к таким созданиям?"
        )

    elif attitude == "hate":
        await callback.message.edit_text(
            "🤔 Ты не любишь **всех** животных? Или есть какие-то, которых особенно не переносишь?",
            reply_markup=None
        )
        await state.set_state(AnimalQuiz.waiting_for_dislike_reason)
        return  # не очищаем состояние

    # Завершаем диалог (кроме ветки "не люблю")
    await state.clear()

# Обработка уточнения
@router.message(AnimalQuiz.waiting_for_dislike_reason)
async def handle_dislike_reason(message: Message, state: FSMContext):
    await message.answer(
        f"А, понятно! Значит, ты просто не встречал *настоящих* друзей-животных. 😼\n"
        f"Может, в Московском зоопарке ты найдёшь того, кто изменит твоё мнение?"
    )
    await state.clear()