import logging
from aiogram import Bot, Dispatcher

from config import settings #подключаем класс с настройками бота
from router import router #подключаем роутеры 

# Для обратной совместимости экспортируем BOT_TOKEN
BOT_TOKEN = settings.BOT_TOKEN

#Конфигурированием логгирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#Инициализируем бота и диспатчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

#Инициализируем роутеры
dp.include_router(router)

async def start_bot():
    """Главная функция которая будет запускать нашего бота"""
    logger.info("Starting bot...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(start_bot())