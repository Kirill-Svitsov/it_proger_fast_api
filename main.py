from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from logger import logger

app = FastAPI(
    title="Магазин электроники API",
    description="API для интернет-магазина электроники",
    version="1.0.0",
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up...")
    # Инициализация БД
    from database.database import init_db
    await init_db()
    logger.info("Database initialized")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down...")


# Подключаем роутеры
from routers import users

app.include_router(users.router, prefix="/users", tags=["Пользователи"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8190, reload=True)
