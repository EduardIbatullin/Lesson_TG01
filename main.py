import asyncio
import random
import aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import TOKEN, WEATHER_API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Функция для получения прогноза погоды с обработкой ошибок и попыткой повторного запроса
async def get_weather(city: str, retries: int = 3):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
    print(url)
    for attempt in range(retries):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        weather = data['weather'][0]['description']
                        temp = data['main']['temp']
                        feels_like = data['main']['feels_like']
                        return f"Погода в {city}:\nСостояние: {weather}\nТемпература: {temp}°C\nОщущается как: {feels_like}°C"
                    else:
                        return f"Не удалось получить данные о погоде. Проверьте название города. (Код ошибки: {response.status})"
        except aiohttp.ClientOSError as e:
            if attempt < retries - 1:
                await asyncio.sleep(2)  # Задержка перед повторной попыткой
            else:
                return f"Ошибка сети: {str(e)}. Повторите попытку позже."

# Команда /start
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет. Я Бот! Я могу показать прогноз погоды. Используй команду /weather <город>.")

# Команда /help
@dp.message(Command("help"))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды: \n /start - запуск бота \n /photo - случайное фото \n /weather <город> - прогноз погоды \n /help - помощь")

# Команда /photo
@dp.message(Command("photo"))
async def photo(message: Message):
    photos = [
        "https://sofmix-shop.ru/upload/iblock/ef2/rk3qb096rwe8256x0b9i2iubqlh2rly1.jpg",
        "https://baldezh.top/uploads/posts/2022-08/1660006712_32-funart-pro-p-iskusstvennii-intellekt-art-krasivo-35.jpg",
        "https://trashbox.ru/ifiles/1407921_55b940_logo/prodvinutyj-ii-openai-obmanuli-pri-pomoschi-ruchki-i-bumagi-1.jpeg"
    ]
    rand_photo = random.choice(photos)
    await message.answer_photo(photo=rand_photo, caption="Это случайное фото с ИИ!")

# Обработка команды /weather
@dp.message(Command("weather"))
async def weather(message: Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Пожалуйста, укажите город. Пример: /weather Москва")
    else:
        city = parts[1]
        weather_info = await get_weather(city)
        await message.answer(weather_info)

# Обработка текста "Что такое ИИ?"
@dp.message(F.text == "Что такое ИИ?")
async def aitext(message: Message):
    await message.answer("Искусственный интеллект – раздел информатики, который занимается решением когнитивных задач, обычно отведенных человеку. К таким задачам относятся обучение, создание и распознавание образов.")

# Реакция на фото
@dp.message(F.photo)
async def react_photo(message: Message):
    await message.answer("Ого, какое фото!")

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
