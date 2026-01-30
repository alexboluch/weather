# Weather Monitoring Service

Асинхронний сервіс на FastAPI для збору даних про погоду (OpenWeather API) та збереження їх у PostgreSQL.

## Стек
- **Backend:** Python 3.11, FastAPI, APScheduler
- **DB:** PostgreSQL, SQLAlchemy (asyncpg)
- **Infrastructure:** Docker, Docker Compose

## Налаштування (.env)
Створіть файл `.env` у корені проекту та заповніть його(як приклад):

```env
# База даних
DB_USER=user
DB_PASSWORD=password
DB_NAME=weather_db

# Ключі
WEATHER_API_KEY=4376be898bcbc641a67ce16a7d88b00c # ваш_ключ_openweathermap
STATIC_TOKEN=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6 # ваш_токен_авторизації

# Координати
LATITUDE=46.4716
LONGITUDE=30.7059
```
## Запуск
docker-compose up --build -d

## Ендпоінти
GET /weather/history — історія погоди.

GET /weather/logs — логи планувальника.

## Для дебагу
DEBUG_MODE=true у docker-compose.yml
