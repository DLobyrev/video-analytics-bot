import asyncpg
from core.config import settings


class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(settings.database_url, min_size=1, max_size=10)

    async def disconnect(self):
        if self.pool:
            await self.pool.close()
            self.pool = None

    async def fetchval(self, query: str, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetchval(query, *args)


db = Database()
