"""
Роутер для обработки команд бота.
"""

from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from .states import GiftSelectionStates, GiftParameters
from .ai_service import ai_service

# Создаем роутер для обработки команд
router = Router()


@router.message(Command("start"))
async def start_handler(message: Message) -> None:
    """
    Обработчик команды /start.
    
    Args:
        message: Объект сообщения от пользователя
    """
    welcome_text = """
        🤖 **Добро пожаловать в ИИ-бота рекомендаций подарков!**

        Я использую искусственный интеллект для подбора идеальных подарков!

        **Что я умею:**
        • 🧠 Использую ИИ для персональных рекомендаций
        • 🎯 Учитываю возраст, пол и предпочтения получателя
        • 💰 Предлагаю варианты в рамках вашего бюджета
        • 🎉 Помогаю с выбором для разных поводов

        **Начните с команды `/reco` для получения ИИ-рекомендаций!**

        Используйте `/help` для получения подробной информации.
    """
    
    await message.answer(welcome_text, parse_mode="Markdown")


@router.message(Command("shop"))
async def shop_handler(message: Message) -> None:
    """
    Обработчик команды /shop.
    
    Команда должна вызывать страницу магазина где можно приобрести подарки.
    
    Args:
        message: Объект сообщения от пользователя
    """
    await message.answer("It's shop command")


@router.message(Command("reco"))
async def reco_handler(message: Message, state: FSMContext) -> None:
    """
    Обработчик команды /reco.
    
    Команда запускает процесс выбора параметров для ИИ-рекомендаций.
    
    Args:
        message: Объект сообщения от пользователя
        state: Состояние FSM
    """
    await state.set_state(GiftSelectionStates.selecting_gift_type)
    
    # Создаем клавиатуру для выбора типа подарка
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=name, callback_data=f"gift_type_{key}")]
        for key, name in GiftParameters.GIFT_TYPES.items()
    ])
    
    await message.answer(
        "🧠 **ИИ-подбор подарков**\n\n"
        "Я использую искусственный интеллект для создания персональных рекомендаций!\n\n"
        "Сначала выберите тип подарка:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    
@router.message(Command("help"))
async def help_handler(message: Message):
    """
    Обработчик команды /help
    
    Команда должна вызывать сообщение которое должно помочь пользователям разобраться в том как устроен бот
    
    Args:
        message: Сообщение от пользователя
    """
    
    help_text = """
            🤖 **ИИ-бот рекомендаций телеграм подарков**

            **Доступные команды:**

            🧠 `/reco` - Получить ИИ-рекомендации подарков
            • Выберите тип подарка (электроника, одежда, книги и т.д.)
            • Укажите возраст получателя
            • Выберите пол получателя
            • Определите повод для подарка
            • Установите бюджет
            • Получите персональные ИИ-рекомендации!

            🛍️ `/shop` - Перейти в магазин подарков

            ℹ️ `/help` - Показать это сообщение

            **Как работает ИИ:**
            1. Используйте команду `/reco`
            2. Следуйте инструкциям и выбирайте параметры
            3. ИИ анализирует ваши предпочтения
            4. Получите уникальные персональные рекомендации
            5. При необходимости можете начать выбор заново

            **Особенности ИИ-системы:**
            • 🧠 Использует современные алгоритмы машинного обучения
            • 🎯 Учитывает все ваши предпочтения и ограничения
            • 💡 Предлагает креативные и актуальные варианты
            • 🔄 Адаптируется под разные ситуации и поводы

            Начните с команды `/reco` для получения ИИ-рекомендаций! 🚀
    """
    
    await message.answer(help_text, parse_mode="Markdown")


