import asyncio
import os
import asyncpg
from aiogram.types import Message
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from dotenv import load_dotenv
from aiogram import Router

from service import (get_weather, get_joke, get_currency_rates, movies, chat_with_ai)
import keyboards as kb

load_dotenv()

TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()

user_surveys = {}

questions = [
    "Как вас зовут?",
    "Сколько вам лет?",
    "Какой ваш любимый школьный предмет?",
    "Какой ваш любимый цвет?",
    "Какой ваш любимый фильм?",
    "Какое ваше хобби?",
    "Какое ваше любимое животное?",
    "Какое ваше любимое время года?"
]


async def create_pool():
    return await asyncpg.create_pool(
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        host=os.getenv('DB_HOST')
    )


@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(f"Привет {message.from_user.first_name or message.from_user.username}, выберите из меню",
                         reply_markup=kb.reply_menu)


@dp.message()
async def text_handler(message: Message):
    chat_id = message.chat.id


    if chat_id in user_surveys:
        await survey_handler(message)
        return


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
        await start_survey(message)
    elif message.text == '💡 Чат с ИИ':
        await message.answer('Задавайте любой вопрос, на который вам ответит ИИ.')
    else:
        await chat_with_ai(message)


async def start_survey(message: types.Message):
    chat_id = message.chat.id
    user_surveys[chat_id] = {'answers': []}
    await message.answer(questions[0])


async def survey_handler(message: types.Message):
    chat_id = message.chat.id

    if chat_id in user_surveys:
        user_surveys[chat_id]['answers'].append(message.text)
        q_index = len(user_surveys[chat_id]['answers'])

        if q_index < len(questions):
            await message.answer(questions[q_index])
        else:
            pool = dp['db']
            async with pool.acquire() as conn:
                await conn.execute(
                    'INSERT INTO surveys (user_id, answers) VALUES ($1, $2)',
                    message.from_user.id,
                    user_surveys[chat_id]['answers']
                )
            await message.answer("Спасибо за участие в опросе!")
            del user_surveys[chat_id]

@dp.callback_query()
async def callback_query_handler(call: types.CallbackQuery):
    if call.data == "boxing":
        await call.message.answer_photo('https://avatars.mds.yandex.net/i?id=4ec58c567c030197f345986850e2dee9_l-10805535-images-thumbs&n=13')
    elif call.data == 'football':
        await call.message.answer_photo('https://i.cdn.newsbytesapp.com/images/l3420250312041648.jpeg')
    elif call.data == 'basketball':
        await call.message.answer_photo('https://avatars.mds.yandex.net/i?id=35c3668628f22806c28c3d7785ebaa14_l-8770658-images-thumbs&n=13')

async def main():
    pool = await create_pool()
    dp['db'] = pool
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        await pool.close()

if __name__ == '__main__':
    print("Starting bot...")
    asyncio.run(main())
