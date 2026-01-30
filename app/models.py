from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, DateTime, func
from datetime import datetime

from .database import Base


class Weather(Base):
    __tablename__ = "weather_data"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    main: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(255))
    temp: Mapped[float] = mapped_column(Float)
    feels_like: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, server_default=func.now())


class TaskLog(Base):
    __tablename__ = "task_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(default="pending")
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    detail: Mapped[str] = mapped_column(nullable=True)