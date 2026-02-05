import asyncio
import asyncpg
import os


async def main():
    """Создаёт таблицы в БД из файла миграции."""
    host = 'postgres' if os.path.exists('/.dockerenv') else 'localhost'
    conn = await asyncpg.connect(
        user='postgres',
        password='postgres',
        database='analytics',
        host=host
    )
    with open('/app/migrations/001_init_tables.sql', 'r', encoding='utf-8') as f:
        await conn.execute(f.read())
    await conn.close()
    print("Database initialized")


if __name__ == "__main__":
    asyncio.run(main())
