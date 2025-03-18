import os

from aiogram.client.session import aiohttp
from aiogram.types import Message
from dotenv import load_dotenv
from deep_translator import GoogleTranslator
from openai import OpenAI

import aiohttp
import xml.etree.ElementTree as ET
load_dotenv()

WEATHER_API_KEY=os.getenv('WEATHER_API_KEY')

OPEN_AI_CHAT_KEY = os.getenv('OPEN_AI_CHAT_KEY')


#🏞 Погода
async def get_weather():
    url = f"https://api.openweathermap.org/data/2.5/weather?q=Бишкек&appid={WEATHER_API_KEY}&units=metric"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                type_ = data["weather"][0]["main"]
                temp_c = data["main"]["temp"]
                feels_like = data["main"]["feels_like"]
                city = data["name"]
                return f"Погода в городе {city}:{type_}\n Температура:{temp_c}\n Чувствуется как:{feels_like}"
            else:
                return f"Произошла ошибка"


#💡 Курс валют

async def get_currency_rates():
    url = "https://www.nbkr.kg/XML/daily.xml"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                xml_data = await response.text()
                root = ET.fromstring(xml_data)

                rates = {}

                for currency in root.findall('Currency'):
                    iso_code = currency.get('ISOCode')
                    value_element = currency.find('Value')


                    if iso_code and value_element is not None:
                        rate = value_element.text
                        rates[iso_code] = rate


                usd = rates.get("USD", "Нет данных")
                eur = rates.get("EUR", "Нет данных")
                rub = rates.get("RUB", "Нет данных")
                kzt = rates.get("KZT", "Нет данных")
                cny = rates.get("CNY", "Нет данных")

                return (f"💰 Официальные курсы валют в Кыргызстане:\n"
                        f"🇺🇸 USD: {usd} KGS\n"
                        f"🇪🇺 EUR: {eur} KGS\n"
                        f"🇷🇺 RUB: {rub} KGS\n"
                        f"🇰🇿 KZT: {kzt} KGS\n"
                        f"🇨🇳 CNY: {cny} KGS")
            else:
                return f"Ошибка при запросе данных: {response.status}"


#🏞 Список фильмов
movies = """1. Побег из Шоушенка (1994)
2. Крестный отец (1972)
3. Крестный отец 2 (1974)
4. Темный рыцарь (2008)
5. Криминальное чтиво (1994)
6. Бойцовский клуб (1999)
7. Форрест Гамп (1994)
8. Начало (2010)
9. Матрица (1999)
10. Зеленая миля (1999)
11. Интерстеллар (2014)
12. Список Шиндлера (1993)
13. Парк юрского периода (1993)
14. Гладиатор (2000)
15. Властелин колец: Братство кольца (2001)
16. Властелин колец: Две крепости (2002)
17. Властелин колец: Возвращение короля (2003)
18. Звездные войны: Империя наносит ответный удар (1980)
19. Однажды в Голливуде (2019)
20. Достучаться до небес (1997)
21. Джанго освобожденный (2012)
22. Великий Гэтсби (2013)
23. Операция «Ы» и другие приключения Шурика (1965)
24. Брат (1997)
25. Брат 2 (2000)
26. Джентльмены (2019)
27. Карты, деньги, два ствола (1998)
28. Большой куш (2000)
29. Леон (1994)
30. Реквием по мечте (2000)
31. Таксист (1976)
32. Остров проклятых (2010)
33. Храброе сердце (1995)
34. Пираты Карибского моря: Проклятие Черной жемчужины (2003)
35. Искупление (2007)
36. Шестое чувство (1999)
37. Однажды в Америке (1984)
38. Достать ножи (2019)
39. Оно (2017)
40. Титаник (1997)"""

#💡 Шутка
async def get_joke():
    url = "https://v2.jokeapi.dev/joke/Any"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                if data["type"] == "single":
                    joke = data["joke"]
                else:
                    joke = f"{data['setup']}\n{data['delivery']}"

                translated_joke = GoogleTranslator(source="auto", target="ru").translate(joke)
                return translated_joke
            else:
                return "Ошибка при получении шутки 😢"

#OpenAi
async def chat_with_ai(message: Message):
    try:
        print("Старт")
        client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=f"{OPEN_AI_CHAT_KEY}",
        )

        completion = client.chat.completions.create(
        model="open-r1/olympiccoder-32b:free",
        messages=[
            {
            "role": "user",
            "content": message.text
            }
        ]
        )
        r = completion.choices[0].message.content
        await message.answer(r)
    except Exception as e:
        print(e)