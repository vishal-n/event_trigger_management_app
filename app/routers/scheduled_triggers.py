from fastapi import APIRouter, BackgroundTasks
from app.models import ScheduledTrigger
from app.database import get_db_connection
from datetime import datetime


router = APIRouter(prefix="/triggers/scheduled", tags=["Scheduled Triggers"])


@router.post("/")
async def create_scheduled_trigger(trigger: ScheduledTrigger, background_tasks: BackgroundTasks):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO scheduled_triggers (name, interval_minutes, fire_in_minutes, recurring, created_at) 
                   VALUES (%s, %s, %s, %s, %s) RETURNING id""",
                (trigger.name, trigger.interval_minutes, trigger.fire_in_minutes, trigger.recurring, datetime.utcnow())
            )
            trigger_id = cur.fetchone()["id"]
            conn.commit()

    if trigger.recurring:
        # Add recurring logic
        background_tasks.add_task(handle_recurring_task, trigger_id, trigger.interval_minutes)
    return {"message": "Scheduled trigger created", "id": trigger_id}
