# Настройка подключения к базе данных
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, \
    async_sessionmaker
from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base, declared_attr

from config import DATABASE_URL

if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgresql://", "postgresql+asyncpg://", 1)

# Создание асинхронного движка SQLAlchemy
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Вывод SQL-запросов в консоль (удобно для отладки)
)


# Создание фабрики сессий с использованием современного синтаксиса
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    # Использование expire_on_commit=False позволяет избежать дополнительных
    # запросов и связанных с этим проблем в асинхронном коде
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)


class PreBase:

    @declared_attr
    def __tablename__(cls):

        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


# Сделана настройка чтоб название таблицы совпадала с названием модели
Base = declarative_base(cls=PreBase)


# Асинхронная функция для получения сессии базы данных
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
