from fastapi import APIRouter
from app.database import get_db_connection
from datetime import datetime, timedelta

router = APIRouter(prefix="/logs", tags=["Event Logs"])


@router.get("/")
async def get_logs(archived: bool = False):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            if archived:
                cur.execute("SELECT * FROM executions WHERE is_archived = TRUE ORDER BY executed_at DESC")
            else:
                cur.execute("SELECT * FROM executions WHERE executed_at >= %s AND is_archived = FALSE ORDER BY executed_at DESC",
                            (datetime.utcnow() - timedelta(hours=2),))
            logs = cur.fetchall()
    return {"logs": logs}
