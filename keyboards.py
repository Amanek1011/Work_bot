from aiogram.types import InlineKeyboardButton
from aiogram import types

reply_menu = types.ReplyKeyboardMarkup(
    keyboard=[
            [
                types.KeyboardButton(text='💡 Картинка'),
                types.KeyboardButton(text='🏞 Погода'),
            ],
            [
                types.KeyboardButton(text='💡 Курс валют'),
                types.KeyboardButton(text='🏞 Список фильмов'),
            ],
            [
                types.KeyboardButton(text='💡 Шутка'),
                types.KeyboardButton(text='🏞 Пройти опрос'),
            ],
            [
                types.KeyboardButton(text='💡 Чат с ИИ')
            ]
        ],
        resize_keyboard=True,
)


inline_image = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Бокс🥊', callback_data='boxing')],
        [InlineKeyboardButton(text='Футбол⚽', callback_data='football')],
        [InlineKeyboardButton(text='Баскетболл🏀', callback_data='basketball')]

    ]
)

inline_AI = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Старт', callback_data='start_Ai')]
    ]
)