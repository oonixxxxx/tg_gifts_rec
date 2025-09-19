import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

class Settings:
    """Класс настроек для бота"""
    
    def __init__(self):
        self.BOT_TOKEN = os.getenv('BOT_TOKEN')
        
        if not self.BOT_TOKEN:
            raise ValueError("BOT_TOKEN environment variable is required!")

# Создаем экземпляр настроек
settings = Settings()