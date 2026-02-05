import asyncio
import json
import os
from datetime import datetime

from core.database import db


def parse_datetime(value: str) -> datetime:
    """Преобразует ISO-дату с временной зоной в naive datetime для PostgreSQL TIMESTAMP."""
    dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
    return dt.replace(tzinfo=None) if dt.tzinfo else dt


async def main():
    """Загружает видео и снапшоты из JSON в таблицы БД."""
    await db.connect()

    json_path = os.environ.get('JSON_DATA_PATH', '/app/data/videos.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
        videos = raw_data['videos']

    video_count = 0
    snapshot_count = 0

    for video in videos:
        # Вставляем видео
        await db.fetchval(
            """
            INSERT INTO videos (id, creator_id, video_created_at, views_count, likes_count,
                                comments_count, reports_count, created_at, updated_at)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9) ON CONFLICT (id) DO NOTHING
            """,
            video['id'],
            video['creator_id'],
            parse_datetime(video['video_created_at']),
            video['views_count'],
            video['likes_count'],
            video['comments_count'],
            video['reports_count'],
            parse_datetime(video['created_at']) if video.get('created_at') else None,
            parse_datetime(video['updated_at']) if video.get('updated_at') else None
        )
        video_count += 1

        # Вставляем снапшоты
        for snapshot in video.get('snapshots', []):
            await db.fetchval(
                """
                INSERT INTO video_snapshots (video_id, created_at, views_count, likes_count,
                                             comments_count, reports_count,
                                             delta_views_count, delta_likes_count, delta_comments_count,
                                             delta_reports_count, updated_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
                """,
                video['id'],
                parse_datetime(snapshot['created_at']),
                snapshot['views_count'],
                snapshot['likes_count'],
                snapshot['comments_count'],
                snapshot['reports_count'],
                snapshot['delta_views_count'],
                snapshot['delta_likes_count'],
                snapshot['delta_comments_count'],
                snapshot['delta_reports_count'],
                parse_datetime(snapshot['updated_at']) if snapshot.get('updated_at') else None
            )
            snapshot_count += 1

    await db.disconnect()
    print(f"Loaded {video_count} videos and {snapshot_count} snapshots")


if __name__ == "__main__":
    asyncio.run(main())
