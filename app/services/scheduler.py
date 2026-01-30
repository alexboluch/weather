from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.database import SessionLocal
from app.services.logic import fetch_and_save_weather, cleanup_old_logs

def start_scheduler():
    scheduler = AsyncIOScheduler()

    async def weather_job():
        async with SessionLocal() as db:
            await fetch_and_save_weather(db)

    async def cleanup_job():
        async with SessionLocal() as db:
            await cleanup_old_logs(db)

    scheduler.add_job(weather_job, 'cron', minute=0, id='weather_fetch')
    scheduler.add_job(cleanup_job, 'cron', hour=3, minute=0, id='logs_cleanup')

    scheduler.start()
    return scheduler
