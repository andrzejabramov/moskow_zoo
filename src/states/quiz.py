from aiogram.fsm.state import State, StatesGroup

class AnimalQuiz( StatesGroup ):
    waiting_for_attitude = State()  # состояние: ждём ответ на "любишь животных?"
    waiting_for_dislike_reason = State()  # если выбрал "не люблю" — уточняем