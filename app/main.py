import logging, os, debugpy
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database import engine, Base
from app.services.scheduler import start_scheduler
from app.api.endpoints import router as weather_router
from app.config import settings


if os.getenv("DEBUG_MODE") == "true":
    debugpy.listen(("0.0.0.0", 5678))
    # debugpy.wait_for_client()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    scheduler = start_scheduler()

    yield # Додаток працює

    try:
        scheduler.shutdown(wait=False)
    except Exception as e:
        logger.error(f"Error during scheduler shutdown: {e}")


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)
app.include_router(weather_router)
