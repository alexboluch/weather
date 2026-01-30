import httpx
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from app.models import Weather, TaskLog
from app.config import settings


API_URL = "https://api.openweathermap.org/data/2.5/weather"


async def fetch_and_save_weather(db: AsyncSession):
    async with httpx.AsyncClient() as client:
        try:
            params = {
                'lat': settings.LATITUDE,
                'lon': settings.LONGITUDE,
                "appid": settings.WEATHER_API_KEY,
                "units": "metric",
                "lang": "ua"
            }
            response = await client.get(API_URL, params=params, timeout=10.0)
            response.raise_for_status()
            data = response.json()

            new_weather = Weather(
                main=data["weather"][0]["main"],
                description=data["weather"][0]["description"],
                temp=data["main"]["temp"],
                feels_like=data["main"]["feels_like"]
            )

            db.add(new_weather)
            log = TaskLog(
                status="success",
                detail=f"Weather updated for {data.get('name')}"
            )
            db.add(log)
            await db.commit()
            print(f"[{datetime.now()}] Дані успішно збережено")

        except httpx.HTTPStatusError as e:
            await db.rollback()
            error_msg = f"API Error: {e.response.status_code}"
            db.add(TaskLog(status="error", detail=error_msg))
            await db.commit()
            print(error_msg)

        except Exception as e:
            await db.rollback()
            error_msg = f"Unexpected Error: {str(e)}"
            db.add(TaskLog(status="error", detail=error_msg))
            await db.commit()
            print(error_msg)


async def cleanup_old_logs(db: AsyncSession):
    try:
        threshold = datetime.utcnow() - timedelta(days=7)
        query = delete(TaskLog).where(TaskLog.created_at < threshold)

        result = await db.execute(query)
        await db.commit()

        print(f"Cleanup complete. Removed rows: {result.rowcount}")

    except Exception as e:
        await db.rollback()
        print(f"Error during logs cleanup: {e}")