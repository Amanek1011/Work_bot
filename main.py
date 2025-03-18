import asyncio


import os

from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from dotenv import load_dotenv
from aiogram import Router
from service import (get_weather, get_joke,get_currency_rates, movies, start_survey)
import keyboards as kb
from States import Questions

load_dotenv()

TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(f"Привет {message.from_user.first_name or message.from_user.username}, выберите из меню",
                         reply_markup= kb.reply_menu)
@dp.message()
async def text_handler(message: Message, state: FSMContext):
    if message.text == "💡 Картинка":
        await message.answer('Какую картинку вы хотите?', reply_markup=kb.inline_image)
    elif message.text == "🏞 Погода":
        weather = await get_weather()
        await message.answer(weather)
    elif message.text == '💡 Курс валют':
        course = await get_currency_rates()
        await message.answer(course)
    elif message.text == '🏞 Список фильмов':
        await message.answer(movies)
    elif message.text == '💡 Шутка':
        joke = await get_joke()
        await message.answer(joke)
    elif message.text == '🏞 Пройти опрос':
        await start_survey(message, state)


@dp.message(Questions.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько вам лет?")
    await state.set_state(Questions.age)

@dp.message(Questions.age)
async def process_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("Какой ваш любимый школьный предмет?")
    await state.set_state(Questions.favorite_subject)

@dp.message(Questions.favorite_subject)
async def process_favorite_subject(message: Message, state: FSMContext):
    await state.update_data(favorite_subject=message.text)
    await message.answer("Какой ваш любимый цвет?")
    await state.set_state(Questions.favorite_color)

@dp.message(Questions.favorite_color)
async def process_favorite_color(message: Message, state: FSMContext):
    await state.update_data(favorite_color=message.text)
    await message.answer("Какой ваш любимый фильм?")
    await state.set_state(Questions.favorite_movie)

@dp.message(Questions.favorite_movie)
async def process_favorite_movie(message: Message, state: FSMContext):
    await state.update_data(favorite_movie=message.text)
    await message.answer("Какое ваше хобби?")
    await state.set_state(Questions.hobby)

@dp.message(Questions.hobby)
async def process_hobby(message: Message, state: FSMContext):
    await state.update_data(hobby=message.text)
    await message.answer("Какое ваше любимое животное?")
    await state.set_state(Questions.favorite_animal)

@dp.message(Questions.favorite_animal)
async def process_favorite_animal(message: Message, state: FSMContext):
    await state.update_data(favorite_animal=message.text)
    await message.answer("Ваше любимое время года?")
    await state.set_state(Questions.favorite_season)

@dp.message(Questions.favorite_season)
async def process_favorite_season(message: Message, state: FSMContext):
    data = await state.get_data()
    summary = (f"Спасибо за участие в опросе!\n"
               f"Имя: {data['name']}\n"
               f"Возраст: {data['age']}\n"
               f"Любимый предмет: {data['favorite_subject']}\n"
               f"Любимый цвет: {data['favorite_color']}\n"
               f"Любимый фильм: {data['favorite_movie']}\n"
               f"Хобби: {data['hobby']}\n"
               f"Любимое животное: {data['favorite_animal']}\n"
               f"Любимое время года: {data['favorite_season']}")

    await message.answer(summary)
    await state.clear()


@dp.callback_query()
async def callback_query_handler(call: types.CallbackQuery):
    if call.data == "boxing":
        await call.message.answer_photo('https://avatars.mds.yandex.net/i?id=4ec58c567c030197f345986850e2dee9_l-10805535-images-thumbs&n=13')
    elif call.data == 'football':
        await call.message.answer_photo('https://i.cdn.newsbytesapp.com/images/l3420250312041648.jpeg')
    elif call.data == 'basketball':
        await call.message.answer_photo('https://avatars.mds.yandex.net/i?id=35c3668628f22806c28c3d7785ebaa14_l-8770658-images-thumbs&n=13')


async def main():
    print("Bot started...")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())