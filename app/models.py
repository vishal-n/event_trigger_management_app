### Database schemas for all the tables

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ScheduledTrigger(BaseModel):
    name: str
    interval_minutes: Optional[int] = None
    fire_in_minutes: Optional[int] = None
    recurring: bool


class APITrigger(BaseModel):
    name: str
    endpoint: str
    payload: dict


class TriggerExecution(BaseModel):
    trigger_id: int
    executed_at: datetime
    is_test: bool
    trigger_type: str
