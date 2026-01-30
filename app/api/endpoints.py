from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from datetime import date, datetime, time
from typing import List, Any

from app.database import get_db
from app.models import Weather, TaskLog
from app.api.deps import validate_token


router = APIRouter(
    prefix="/weather",
    tags=["Weather & Logs"],
    dependencies=[Depends(validate_token)]
)


async def get_records_by_day(model: Any, day: date, db: AsyncSession):
    """Універсальна функція для фільтрації записів за день"""
    start = datetime.combine(day, time.min)
    end = datetime.combine(day, time.max)

    query = (
        select(model)
        .where(and_(model.created_at >= start, model.created_at <= end))
        .order_by(model.created_at.asc())
    )
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/history", response_model=None)
async def get_weather_history(
    day: date = Query(..., description="YYYY-MM-DD"),
    db: AsyncSession = Depends(get_db)
):
    records = await get_records_by_day(Weather, day, db)
    return {
        "status": "success",
        "requested_day": day,
        "count": len(records),
        "data": records
    }


@router.get("/logs", response_model=None)
async def get_scheduler_logs(
    day: date = Query(..., description="YYYY-MM-DD"),
    db: AsyncSession = Depends(get_db)
):
    logs = await get_records_by_day(TaskLog, day, db)
    return {
        "status": "success",
        "requested_day": day,
        "count": len(logs),
        "data": logs
    }
