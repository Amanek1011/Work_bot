from aiogram.fsm.state import State, StatesGroup

class Questions(StatesGroup):
    name = State()
    age = State()
    favorite_subject = State()
    favorite_color = State()
    favorite_movie = State()
    hobby = State()
    favorite_animal = State()
    favorite_season = State()