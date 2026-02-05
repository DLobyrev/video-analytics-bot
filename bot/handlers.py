import logging

from aiogram import Router, F
from aiogram.types import Message

from services.llm_service import LLMService
from services.query_service import QueryService


router = Router()
llm_service = LLMService()
query_service = QueryService()


@router.message(F.text)
async def handle_query(message: Message):
    """Обрабатывает текстовый запрос пользователя и возвращает числовой ответ."""
    try:
        sql = await llm_service.generate_sql(message.text)
        result = await query_service.execute_sql(sql)
        await message.answer(str(result))
    except Exception as e:
        logging.error(f"Handler error: {e}")
        await message.answer("0")