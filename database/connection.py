# ==============================================
# CONEXÃO COM O BANCO DE DADOS (SQLAlchemy Async)
# ==============================================

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.orm import DeclarativeBase

from config import DATABASE_URL

# Engine assíncrono para PostgreSQL
engine = create_async_engine(
    DATABASE_URL,
    echo=False,          # Define como True para logar SQL (apenas debug)
    pool_size=20,        # Tamanho do pool de conexões
    max_overflow=0,      # Conexões extras além do pool_size
    future=True,
)

# Fábrica de sessões assíncronas
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Evita expirar objetos após commit
)

# Base declarativa para os modelos
class Base(DeclarativeBase):
    """Classe base para todos os modelos ORM."""
    pass


async def get_session() -> AsyncSession:
    """
    Dependência para obter uma sessão assíncrona.
    Uso em handlers do Aiogram com injeção manual:
        async with async_session() as session:
            ...
    """
    async with async_session() as session:
        yield session


async def init_db() -> None:
    """
    Cria as tabelas no banco de dados (para desenvolvimento inicial).
    Em produção, utilize Alembic para migrações.
    """
    # Importa os modelos para registrá-los na Base
    from database import models  # noqa: F401
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()
