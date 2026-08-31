# ==============================================
# ALAMBIĆ - CONFIGURAÇÃO DO AMBIENTE DE MIGRAÇÃO
# ==============================================

import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# Importa a Base e a URL do banco
from database.connection import Base, DATABASE_URL
from database import models  # noqa: F401  (garante que os modelos sejam registrados)

# Carrega configuração do arquivo alembic.ini
config = context.config

# Define a URL do banco a partir do config.py
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Configura logging se houver arquivo de config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadados dos modelos para autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Executa migrações em modo offline (sem conexão com banco).
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """
    Executa migrações com conexão ativa.
    """
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """
    Cria engine assíncrono e executa migrações.
    """
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """
    Executa migrações em modo online (com conexão assíncrona).
    """
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
