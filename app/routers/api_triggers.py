import asyncio
from fastapi import APIRouter, HTTPException
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


@router.get("/")
async def get_all_api_triggers():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM api_triggers")
            api_triggers = cur.fetchall()
    return {"api_triggers": api_triggers}


@router.post("/{trigger_id}/execute")
async def execute_api_trigger(trigger_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT endpoint, payload FROM api_triggers WHERE id = %s", (trigger_id,))
            trigger = cur.fetchone()
            if not trigger:
                raise HTTPException(status_code=404, detail="Trigger not found")
    
    # Simulate API request
    await asyncio.sleep(1)
    executed_at = datetime.utcnow()
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO executions (trigger_id, executed_at, is_test, trigger_type) VALUES (%s, %s, %s, %s)", (trigger_id, executed_at, False, "api"))
            conn.commit()
    return {"message": "API trigger executed", "executed_at": executed_at}


@router.put("/{trigger_id}")
async def update_api_trigger(trigger_id: int, trigger: APITrigger):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE api_triggers SET name = %s, endpoint = %s, payload = %s WHERE id = %s", (trigger.name, trigger.endpoint, trigger.payload, trigger_id))
            conn.commit()
    return {"message": "API trigger updated"}


@router.delete("/{trigger_id}")
async def delete_api_trigger(trigger_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM api_triggers WHERE id = %s", (trigger_id,))
            conn.commit()
    return {"message": "API trigger deleted"}


@router.post("/test/")
async def test_api_trigger(trigger: APITrigger):
    # Simulate API request
    await asyncio.sleep(1)
    print(f"Test API trigger executed with payload: {trigger.payload} at {datetime.utcnow()}")
    return {"message": "Test API trigger executed successfully"}
