import asyncio
from fastapi import APIRouter, BackgroundTasks
from app.models import ScheduledTrigger
from app.database import get_db_connection
from app.tasks import handle_recurring_task, handle_scheduled_trigger
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

    if trigger.recurring and trigger.interval_minutes:
        # Start recurring task
        background_tasks.add_task(handle_recurring_task, trigger_id, trigger.interval_minutes)
    elif trigger.fire_in_minutes:
        # Handle one-time scheduled task
        background_tasks.add_task(handle_scheduled_trigger, trigger_id, trigger.fire_in_minutes, False)

    return {"message": "Scheduled trigger created", "id": trigger_id}


@router.get("/")
async def get_all_scheduled_triggers():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM scheduled_triggers")
            scheduled_triggers = cur.fetchall()
    return {"scheduled_triggers": scheduled_triggers}


@router.put("/{trigger_id}")
async def update_scheduled_trigger(trigger_id: int, trigger: ScheduledTrigger):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE scheduled_triggers SET name = %s, interval_minutes = %s, fire_in_minutes = %s, recurring = %s WHERE id = %s", (trigger.name, trigger.interval_minutes, trigger.fire_in_minutes, trigger.recurring, trigger_id))
            conn.commit()
    return {"message": "Scheduled trigger updated"}


@router.delete("/{trigger_id}")
async def delete_scheduled_trigger(trigger_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM scheduled_triggers WHERE id = %s", (trigger_id,))
            conn.commit()
    return {"message": "Scheduled trigger deleted"}


@router.post("/test/")
async def test_scheduled_trigger(fire_in_minutes: int, background_tasks: BackgroundTasks):
    async def test_task():
        await asyncio.sleep(fire_in_minutes * 60)
        print(f"Test scheduled trigger fired at {datetime.utcnow()}")
    background_tasks.add_task(test_task)
    return {"message": f"Test scheduled trigger will fire in {fire_in_minutes} minutes."}
