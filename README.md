# Telegram Bot для аналитики видео-статистики

Асинхронный Telegram-бот, который обрабатывает естественные запросы на русском языке и возвращает числовые ответы на
основе анализа видео-статистики из PostgreSQL.


## Запуск с Docker

```bash

# Клонирование
git clone https://github.com/DLobyrev/video-analytics-bot.git
cd video-analytics-bot

# Настройка окружения
cp .env.example .env 
# заполните .env
1. TELEGRAM_BOT_TOKEN=ваш_токен_из_@BotFather
2. HF_TOKEN=ваш_API_ключ_LLM_HuggingFace
- Остальные параметры по умолчанию

# Запуск
docker compose up -d --build
sleep 30  # ожидание готовности БД

# Инициализация БД и загрузка данных
docker compose exec bot python -m scripts.init_db
docker compose exec bot python -m scripts.load_data

# Проверка логов
docker compose logs -f bot
```




### Архитектура и подход к преобразованию запросов в SQL

```
Запрос пользователя в Telegram (русский текст)
         ↓
[LLM(32B)] — генерация готового SQL на основе промпта со схемой БД
         ↓
[QueryService] — выполнение параметризованного SQL через asyncpg
         ↓
PostgreSQL → число → ответ пользователю в Telegram
```
Модель **генерирует готовый SQL** напрямую (без промежуточной параметризации), потому что:
- Модель Qwen2.5-Coder-32B обучена на коде и корректно генерирует SQL при наличии детального контекста схемы
- Промпт содержит полную схему БД и правила преобразования запросов
  - Структуру таблиц videos и video_snapshots с типами полей
  - Примеры преобразования чисел (10 000 → 10000)
  - Запрет на вывод пояснений — только чистый SQL



### Промпт для описания схемы БД (фрагмент)
```
videos(id TEXT, creator_id UUID, video_created_at TIMESTAMP, views_count INT)
video_snapshots(video_id TEXT, created_at TIMESTAMP, delta_views_count INT)

ПРАВИЛА:
- "сколько видео" -> COUNT(*), таблица videos
- "на сколько выросли" -> SUM(delta_views_count), таблица video_snapshots
- При фильтрации по времени: video_snapshots.created_at или videos.video_created_at
- "10 000" -> 10000, "100 000" -> 100000 (не путай!)
- Выводи ТОЛЬКО запрос без пояснений

Q: {запрос пользователя}
A:
```
### Технический стек (полностью асинхронный)
| Компонент       | Технология                                    |
|-----------------|-----------------------------------------------|
| Язык            | Python 3.11                                   |
| Telegram-бот    | aiogram 3.x (асинхронный)                     |
| База данных     | PostgreSQL 15                                 |
| LLM             | Qwen2.5-Coder-32B-Instruct через Hugging Face |
| HTTP-клиент     | aiohttp                                       |
| Запросы к БД    | asyncpg                                       |
| Сборка          | Docker + docker-compose                       |