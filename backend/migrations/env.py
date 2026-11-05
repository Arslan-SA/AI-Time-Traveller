"""Alembic environment for the AI Time Traveler database."""

from logging.config import fileConfig

from alembic import context

# Importing the models package registers every table on Base.metadata.
import app.db.models  # noqa: F401
from app.core.config import get_settings
from app.db.base import Base
from app.db.session import create_db_engine, normalize_database_url

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def database_url() -> str:
    """Prefer sqlalchemy.url from the ini file, then the app settings."""
    configured_url = config.get_main_option("sqlalchemy.url")
    return normalize_database_url(configured_url or get_settings().database_url)


def run_migrations_offline() -> None:
    """Emit SQL to stdout without connecting to a database."""
    url = database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        render_as_batch=url.startswith("sqlite"),
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations against the configured database."""
    connectable = create_db_engine(database_url(), echo=False)

    try:
        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
                compare_type=True,
                render_as_batch=connection.dialect.name == "sqlite",
            )

            with context.begin_transaction():
                context.run_migrations()
    finally:
        connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
