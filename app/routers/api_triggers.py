from fastapi import APIRouter
from app.models import APITrigger
from app.database import get_db_connection
from datetime import datetime

router = APIRouter(prefix="/triggers/api", tags=["API Triggers"])


@router.post("/")
async def create_api_trigger(trigger: APITrigger):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO api_triggers (name, endpoint, payload, created_at) VALUES (%s, %s, %s, %s) RETURNING id",
                (trigger.name, trigger.endpoint, trigger.payload, datetime.utcnow())
            )
            trigger_id = cur.fetchone()["id"]
            conn.commit()
    return {"message": "API trigger created", "id": trigger_id}
