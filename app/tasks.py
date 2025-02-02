import asyncio
from datetime import datetime, timedelta
from app.database import get_db_connection


async def handle_event_retention():
    while True:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE executions SET is_archived = TRUE WHERE executed_at < %s AND is_archived = FALSE", (datetime.utcnow() - timedelta(hours=2),))
                cur.execute("DELETE FROM executions WHERE executed_at < %s", (datetime.utcnow() - timedelta(hours=48),))
                conn.commit()
        await asyncio.sleep(3600)
