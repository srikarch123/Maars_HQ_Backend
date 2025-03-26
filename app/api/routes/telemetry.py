from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import async_session
from app.core.redis_client import get_redis
from app.schemas.telemetry import TelemetryOut
from app.models.telemetry import Telemetry
import json

router = APIRouter()

async def get_db():
    async with async_session() as session:
        yield session

@router.get("/telemetry/{robot_id}", response_model=TelemetryOut)
async def get_latest_telemetry(robot_id: str):
    redis = await get_redis()
    data = await redis.get(f"telemetry:{robot_id}")
    if not data:
        raise HTTPException(status_code=404, detail="No telemetry found")
    return json.loads(data)

@router.get("/telemetry/{robot_id}/history", response_model=list[TelemetryOut])
async def get_telemetry_history(robot_id: str, limit: int = 10, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Telemetry)
        .where(Telemetry.robot_id == robot_id)
        .order_by(Telemetry.timestamp.desc())
        .limit(limit)
    )
    return result.scalars().all()
