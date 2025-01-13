import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.types import BotCommand

from config import TOKEN, WEATHER_API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def start_handler(message: Message):
    await message.answer("Привет, я бот-синоптик! Используй команду /koh, чтобы узнать погоду на острове Панган")


async def help_handler(message: Message):
    await message.answer("Этот бот умеет выполнять команды:\n/start\n/help\n/koh")


async def koh_weather_handler(message: Message):
    try:
        async with aiohttp.ClientSession() as session:
            url = f"https://api.openweathermap.org/data/2.5/weather?q=Ko+Pha+Ngan,TH&appid={WEATHER_API_KEY}&units=metric"
            async with session.get(url) as response:
                response_text = await response.text()
                if response.status == 200:
                    data = await response.json()
                    weather_description = data['weather'][0]['description']
                    temperature = data['main']['temp']
                    feels_like = data['main']['feels_like']
                    humidity = data['main']['humidity']

                    weather_message = (
                        f"Погода на острове Панган:\n"
                        f"Описание: {weather_description.capitalize()}\n"
                        f"Температура: {temperature}°C\n"
                        f"Ощущается как: {feels_like}°C\n"
                        f"Влажность: {humidity}%"
                    )

                    # Отправка сообщения с погодой пользователю
                    await message.answer(weather_message)
                else:
                    await message.answer(f"Ошибка запроса: {response.status} - {response_text}")

                # Вывод для отладки
                print(f"URL: {url}")
                print(f"Response status: {response.status}")
                print(f"Response text: {response_text}")
    except Exception as e:
        await message.answer("Произошла ошибка при получении данных о погоде. Попробуйте позже.")
        print(f"Ошибка: {e}")


async def main():
    # Регистрация команд
    dp.message.register(start_handler, CommandStart())
    dp.message.register(help_handler, Command("help"))
    dp.message.register(koh_weather_handler, Command("koh"))

    # Установка списка команд для бота
    await bot.set_my_commands([
        BotCommand(command="start", description="Начало работы"),
        BotCommand(command="help", description="Справка"),
        BotCommand(command="koh", description="Узнать погоду на острове Панган")
    ])

    # Запуск бота
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
