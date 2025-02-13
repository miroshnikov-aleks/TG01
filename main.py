import logging
import requests
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
from config import API_TOKEN, WEATHER_API_KEY  # Импортируем токены из config.py

CITY_NAME = 'Moscow'

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()


# Команда /start
@router.message(Command(commands=['start']))
async def send_welcome(message: types.Message):
    await message.reply(
        "Привет! Я бот, который может предоставить прогноз погоды. Напишите команду /weather, чтобы получить прогноз."
    )


# Команда /help
@router.message(Command(commands=['help']))
async def send_help(message: types.Message):
    await message.reply(
        "Я могу помочь вам с прогнозом погоды.\n\nКоманды:\n/start - Начать работу с ботом\n/help - Получить справку\n/weather - Получить прогноз погоды"
    )


# Команда /weather
@router.message(Command(commands=['weather']))
async def get_weather(message: types.Message):
    try:
        # Запрос к API OpenWeatherMap
        response = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={CITY_NAME}&appid={WEATHER_API_KEY}&units=metric')

        if response.status_code != 200:
            await message.reply(f"Не удалось получить данные о погоде. Код ошибки: {response.status_code}.")
            return

        data = response.json()

        # Извлечение данных
        temperature = data['main']['temp']
        weather_description = data['weather'][0]['description']

        # Формирование ответа
        weather_info = f"Погода в {CITY_NAME}:\nТемпература: {temperature}°C\nОписание: {weather_description.capitalize()}"
        await message.reply(weather_info)

    except Exception as e:
        logging.exception("Произошла ошибка при получении данных о погоде:")
        await message.reply("Не удалось получить данные о погоде. Попробуйте позже.")


# Добавление маршрутизатора в диспетчер
dp.include_router(router)


# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())