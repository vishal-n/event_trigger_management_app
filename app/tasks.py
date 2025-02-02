import asyncio
from typing import Optional
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


async def handle_recurring_task(trigger_id: int, interval_minutes: int):
    """
    Handle recurring scheduled tasks.
    
    Args:
        trigger_id (int): ID of the trigger in the database.
        interval_minutes (int): Interval in minutes between executions.
    """
    while True:
        # Wait for the interval
        await asyncio.sleep(interval_minutes * 60)
        
        # Log the execution in the database
        executed_at = datetime.utcnow()
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO executions (trigger_id, executed_at, is_test, trigger_type) VALUES (%s, %s, %s, %s)",
                    (trigger_id, executed_at, False, "scheduled")
                )
                conn.commit()
        
        print(f"Recurring task triggered for Trigger ID {trigger_id} at {executed_at}")


async def handle_scheduled_trigger(trigger_id: int, interval: Optional[int], is_recurring: bool):
    """
    Handles scheduled triggers.
    
    - If one-time (`is_recurring=False`), it fires after the delay.
    - If recurring (`is_recurring=True`), it keeps firing at set intervals.
    """
    while True:
        await asyncio.sleep(interval * 60 if interval else 0)  # Convert minutes to seconds
        
        # Log the execution in the database
        executed_at = datetime.utcnow()
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO executions (trigger_id, executed_at, is_test, trigger_type) VALUES (%s, %s, %s, %s)",
                    (trigger_id, executed_at, False, "scheduled")
                )
                conn.commit()
        
        print(f"Trigger ID {trigger_id} executed at {executed_at}")

        if not is_recurring:
            break
