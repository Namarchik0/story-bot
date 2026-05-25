from aiogram.fsm.state import State, StatesGroup


class AddStory(StatesGroup):

    title = State()
    text = State()
    photo = State()


class EditStory(StatesGroup):

    text = State()