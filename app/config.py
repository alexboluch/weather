import os
from pathlib import Path
from dotenv import load_dotenv


env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    PROJECT_NAME: str = "Weather Monitoring Service"
    STATIC_TOKEN: str = os.getenv("STATIC_TOKEN")
    WEATHER_API_KEY: str = os.getenv("WEATHER_API_KEY")
    LATITUDE: float = float(os.getenv("LATITUDE"))
    LONGITUDE: float = float(os.getenv("LONGITUDE"))

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@db:5432/{os.getenv('DB_NAME')}"

settings = Settings()