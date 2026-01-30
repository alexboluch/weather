from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List


class WeatherSchema(BaseModel):
    id: int
    main: str
    description: str
    temp: float
    feels_like: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TaskLogSchema(BaseModel):
    id: int
    status: str
    detail: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DaySummaryResponse(BaseModel):
    status: str
    requested_day: str
    count: int
    data: List[dict]
