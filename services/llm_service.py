import re
import logging

import aiohttp
from core.config import settings


class LLMService:
    """Генерация SQL-запросов через LLM"""

    def __init__(self):
        self.base_url = "https://router.huggingface.co/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {settings.hf_token}",
            "Content-Type": "application/json"
        }

    async def generate_sql(self, query: str) -> str:
        """Преобразует русский запрос в SQL"""
        payload = {
            "model": "Qwen/Qwen2.5-Coder-32B-Instruct",
            "messages": [{
                "role": "user",
                "content": f"""videos(id TEXT, creator_id UUID, video_created_at TIMESTAMP, views_count INT)
video_snapshots(video_id TEXT, created_at TIMESTAMP, delta_views_count INT)

ПРАВИЛА:
- "сколько видео" -> COUNT(*), таблица videos
- "на сколько выросли" -> SUM(delta_views_count), таблица video_snapshots
- При фильтрации по времени: video_snapshots.created_at или videos.video_created_at
- "10 000" -> 10000, "100 000" -> 100000 (не путай!)
- Выводи ТОЛЬКО запрос без пояснений

Q: {query}
A:"""
            }],
            "max_tokens": 120,
            "temperature": 0.0
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                    self.base_url,
                    headers=self.headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
            ) as resp:
                if resp.status != 200:
                    logging.error(f"LLM HTTP {resp.status}: {await resp.text()}")
                    return "SELECT COUNT(*) FROM videos;"
                data = await resp.json()

        raw = data["choices"][0]["message"]["content"].strip()
        raw = raw.replace('```sql', '').replace('```', '').strip()
        logging.info(f"Raw model response: {raw}")
        sql = re.search(r'(SELECT\s+.*?)(?:;|$)', raw, re.IGNORECASE | re.DOTALL)
        return (sql.group(1).strip() + ';') if sql else "SELECT COUNT(*) FROM videos;"
