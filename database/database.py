# Импортируем асинхронные компоненты SQLAlchemy
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from .models.base_model import Base # Импортируем нашу модель Base, от которой наследуются все модели
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
# Это безопасный способ хранения конфиденциальных данных (паролей, ключей и т.д.)
load_dotenv()

# Получаем URL БД из переменных окружения
# os.getenv() пытается получить значение переменной окружения
# Второй аргумент - значение по умолчанию, если переменная не найдена
# Формат URL: postgresql+asyncpg://user:password@host:port/database_name
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5435/fastapi_db")

# Создаём асинхронный движок для работы с базой данных
# create_async_engine создает пул соединений с базой данных
engine = create_async_engine(
    DATABASE_URL,
    pool_size=6,  # Максимальное количество соединений в пуле
    max_overflow=10,  # Дополнительные соединения, которые могут быть созданы при необходимости
    echo=True  # Логирует все SQL-запросы в консоль (удобно для отладки)
)

# Создаём фабрику асинхронных сессий
# async_sessionmaker - это асинхронный аналог sessionmaker
AsyncSessionLocal = async_sessionmaker(
    bind=engine,  # Привязываем к нашему движку
    expire_on_commit=False  # Объекты не будут терять атрибуты после коммита
    # autoflush=False,  # Можно добавить для отключения автоматического flush
    # autocommit=False  # Рекомендуется False для явного управления транзакциями
)


async def init_db():
    """
    Инициализирует базу данных, создает таблицы если они не существуют.
    Эта функция должна быть вызвана при старте приложения.

    Процесс:
    1. Устанавливает соединение с базой данных
    2. Для каждой таблицы в метаданных Base проверяет её существование
    3. Если таблица не существует - создаёт её
    """
    async with engine.begin() as conn:
        # Проверяем существование каждой таблицы перед созданием
        for table in Base.metadata.tables.values():
            # run_sync позволяет выполнять синхронные функции в асинхронном контексте
            if not await conn.run_sync(
                    lambda sync_conn: sync_conn.dialect.has_table(sync_conn, table.name)
            ):
                # Если таблицы нет - создаём её
                await conn.run_sync(table.create)
                print(f"Таблица {table.name} создана")
            else:
                print(f"Таблица {table.name} уже существует")


async def get_db() -> AsyncSession:
    """
    Генератор сессий для зависимостей FastAPI.
    Этот генератор будет использоваться в Depends() для внедрения сессии в роутеры.

    Принцип работы:
    1. Создаёт новую сессию
    2. Возвращает её (yield)
    3. После завершения работы:
       - Пытается сделать commit
       - В случае ошибки - rollback
       - В любом случае закрывает сессию

    Использование в FastAPI:
    @app.get("/")
    async def read_root(db: AsyncSession = Depends(get_db)):
        # работа с db
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session  # Отдаём сессию в роутер
            await session.commit()  # Если не было исключений - коммитим изменения
        except Exception as e:
            await session.rollback()  # При ошибке - откатываем транзакцию
            raise e  # Пробрасываем исключение дальше
        finally:
            await session.close()  # Всегда закрываем сессию
