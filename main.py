import asyncio
import os
from loguru import logger
from dotenv import load_dotenv, find_dotenv
from aiogram import Bot, Dispatcher, types
import requests
from bs4 import BeautifulSoup
from random import choice

load_dotenv(find_dotenv())
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")


async def main():
    logger.add("files.log",
               format="{time: YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
               rotation="3 days",
               backtrace=True,
               diagnose=True)
    
    bot = Bot(token=TOKEN)
    logger.info("сщздан бот")
    dp = Dispatcher()
    logger.info("создан диспетчер")

    async def send_random_joke():
        while True:
            try:
                response = requests.get("https://www.anekdot.ru/random/anekdot/")
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    jokes = soup.find_all('div', class_='text')
                    random_joke = choice(jokes).text.strip()
                    anekdot = random_joke
                else:
                    anekbot = 'Не удалось получить анекдот'
                    
                await bot.send_message(CHANNEL_ID, f"Анекдот: {anekdot}")
            except Exception as e:
                logger.error(f"Ошибка при отправке сообщения {e}")

if __name__ == '__main':
    asyncio.run(main())

