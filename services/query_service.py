import logging

from core.database import db


class QueryService:
    """Выполнение SQL-запросов к базе данных."""

    async def execute_sql(self, sql: str) -> int:
        """Выполняет SQL-запрос и возвращает целочисленный результат."""
        logging.info(f"SQL: {sql}")
        try:
            result = await db.fetchval(sql)
            logging.info(f"Result: {result}")
            return int(result) if result is not None else 0
        except Exception as e:
            logging.error(f"SQL error: {e}")
            return 0
