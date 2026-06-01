from aiogram.fsm.state import State, StatesGroup


class AddStory(StatesGroup):
    title = State()
    content = State()


class EditStory(StatesGroup):
    content = State()