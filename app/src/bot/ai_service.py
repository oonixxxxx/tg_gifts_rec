"""
Сервис для работы с ИИ для генерации рекомендаций подарков.
"""

import os
import asyncio
from typing import Dict, List, Optional
from openai import AsyncOpenAI
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()


class AIRecommendationService:
    """Сервис для генерации рекомендаций подарков с помощью ИИ."""
    
    def __init__(self):
        """Инициализация сервиса."""
        self.client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = "gpt-3.5-turbo"
        
        if not os.getenv('OPENAI_API_KEY'):
            raise ValueError("OPENAI_API_KEY environment variable is required!")
    
    async def get_gift_recommendations(
        self,
        gift_type: str,
        age_group: str,
        gender: str,
        occasion: str,
        budget: str,
        additional_info: Optional[str] = None
    ) -> List[str]:
        """
        Получить рекомендации подарков от ИИ.
        
        Args:
            gift_type: Тип подарка
            age_group: Возрастная группа
            gender: Пол получателя
            occasion: Повод для подарка
            budget: Бюджет
            additional_info: Дополнительная информация о получателе
            
        Returns:
            Список рекомендаций
        """
        try:
            prompt = self._build_prompt(
                gift_type, age_group, gender, occasion, budget, additional_info
            )
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Ты эксперт по подбору подарков. Твоя задача - дать 5 конкретных и полезных рекомендаций подарков на основе предоставленных параметров. Отвечай на русском языке."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            recommendations_text = response.choices[0].message.content
            return self._parse_recommendations(recommendations_text)
            
        except Exception as e:
            print(f"Ошибка при обращении к ИИ: {e}")
            return self._get_fallback_recommendations(gift_type, age_group)
    
    def _build_prompt(
        self,
        gift_type: str,
        age_group: str,
        gender: str,
        occasion: str,
        budget: str,
        additional_info: Optional[str] = None
    ) -> str:
        """Построить промпт для ИИ."""
        
        # Маппинг параметров на русский язык
        type_mapping = {
            "electronics": "электроника",
            "clothing": "одежда и аксессуары",
            "books": "книги",
            "toys": "игрушки",
            "cosmetics": "косметика и парфюмерия",
            "home": "товары для дома",
            "sports": "спорт и активность",
            "hobby": "хобби и творчество"
        }
        
        age_mapping = {
            "child": "ребенок (до 12 лет)",
            "teen": "подросток (13-17 лет)",
            "young_adult": "молодой взрослый (18-30 лет)",
            "adult": "взрослый (31-50 лет)",
            "senior": "пожилой человек (50+ лет)"
        }
        
        gender_mapping = {
            "male": "мужской",
            "female": "женский",
            "unisex": "унисекс"
        }
        
        occasion_mapping = {
            "birthday": "день рождения",
            "new_year": "новый год",
            "valentine": "день святого валентина",
            "graduation": "выпускной",
            "wedding": "свадьба",
            "anniversary": "годовщина",
            "christmas": "рождество",
            "other": "другой повод"
        }
        
        budget_mapping = {
            "low": "до 1000 рублей",
            "medium": "от 1000 до 5000 рублей",
            "high": "от 5000 до 15000 рублей",
            "premium": "от 15000 рублей"
        }
        
        prompt = f"""
Подбери 5 конкретных рекомендаций подарков со следующими параметрами:

Тип подарка: {type_mapping.get(gift_type, gift_type)}
Возраст получателя: {age_mapping.get(age_group, age_group)}
Пол получателя: {gender_mapping.get(gender, gender)}
Повод: {occasion_mapping.get(occasion, occasion)}
Бюджет: {budget_mapping.get(budget, budget)}
"""
        
        if additional_info:
            prompt += f"\nДополнительная информация: {additional_info}"
        
        prompt += """

Требования к ответу:
1. Дай ровно 5 конкретных рекомендаций
2. Каждая рекомендация должна быть конкретным товаром или услугой
3. Учитывай возраст, пол и повод
4. Предложения должны соответствовать бюджету
5. Формат: просто список из 5 пунктов, каждый с новой строки
6. Будь практичным и современным в рекомендациях

Пример формата:
1. Название подарка
2. Название подарка
3. Название подарка
4. Название подарка
5. Название подарка
"""
        
        return prompt
    
    def _parse_recommendations(self, text: str) -> List[str]:
        """Парсинг ответа от ИИ."""
        lines = text.strip().split('\n')
        recommendations = []
        
        for line in lines:
            line = line.strip()
            if line and (line.startswith(('1.', '2.', '3.', '4.', '5.')) or 
                        line.startswith(('1)', '2)', '3)', '4)', '5)')) or
                        line.startswith('-') or line.startswith('•')):
                # Убираем номера и маркеры
                clean_line = line
                for prefix in ['1.', '2.', '3.', '4.', '5.', '1)', '2)', '3)', '4)', '5)', '-', '•']:
                    if clean_line.startswith(prefix):
                        clean_line = clean_line[len(prefix):].strip()
                        break
                
                if clean_line:
                    recommendations.append(clean_line)
        
        # Если не удалось распарсить, возвращаем первые 5 строк
        if not recommendations:
            recommendations = [line.strip() for line in lines if line.strip()][:5]
        
        # Если все еще пусто, возвращаем резервные рекомендации
        if not recommendations:
            recommendations = self._get_fallback_recommendations("electronics", "adult")
        
        return recommendations[:5]  # Возвращаем максимум 5 рекомендаций
    
    def _get_fallback_recommendations(self, gift_type: str, age_group: str) -> List[str]:
        """Резервные рекомендации в случае ошибки ИИ."""
        fallback_recommendations = {
            "electronics": [
                "Беспроводные наушники",
                "Портативная колонка",
                "Умные часы",
                "Планшет",
                "Смартфон"
            ],
            "clothing": [
                "Стильная футболка",
                "Джинсы",
                "Кроссовки",
                "Свитер",
                "Куртка"
            ],
            "books": [
                "Художественная литература",
                "Научно-популярная книга",
                "Энциклопедия",
                "Детектив",
                "Фантастика"
            ],
            "toys": [
                "Настольная игра",
                "Конструктор",
                "Кукла",
                "Машинка",
                "Пазл"
            ],
            "cosmetics": [
                "Парфюм",
                "Косметический набор",
                "Крем для лица",
                "Помада",
                "Тушь для ресниц"
            ],
            "home": [
                "Ваза для цветов",
                "Ароматические свечи",
                "Картина",
                "Комнатное растение",
                "Плед"
            ],
            "sports": [
                "Спортивная форма",
                "Мяч",
                "Гантели",
                "Коврик для йоги",
                "Бутылка для воды"
            ],
            "hobby": [
                "Набор для рисования",
                "Музыкальный инструмент",
                "Набор для рукоделия",
                "Фотоаппарат",
                "Набор инструментов"
            ]
        }
        
        return fallback_recommendations.get(gift_type, [
            "Универсальный подарок",
            "Подарочная карта",
            "Книга",
            "Косметический набор",
            "Аксессуар"
        ])


# Создаем экземпляр сервиса
ai_service = AIRecommendationService()
