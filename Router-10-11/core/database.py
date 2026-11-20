
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

from core.config import settings


# 1. Engine: conecta con la base de datos
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True
)


# 2. Sesion de la base de datos
SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


# 3. Base: clase padre de los modelos
Base = declarative_base()


# 4. Dependencia para FastAPI
async def obtener_bd():

    db = SessionLocal()

    try:
        yield db

    finally:
        await db.close()
