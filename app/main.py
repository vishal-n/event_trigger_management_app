import uvicorn
from fastapi import FastAPI
from app.routers import scheduled_triggers, api_triggers, logs
from app.database import setup_database
from app.tasks import handle_event_retention

import asyncio

app = FastAPI()

# Include routers
app.include_router(scheduled_triggers.router)
app.include_router(api_triggers.router)
app.include_router(logs.router)

@app.on_event("startup")
async def startup():
    setup_database()
    asyncio.create_task(handle_event_retention())

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
