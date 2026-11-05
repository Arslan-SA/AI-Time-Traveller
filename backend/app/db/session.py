"""Database engine, session factory, and FastAPI session dependency."""

from collections.abc import Iterator
from typing import Any

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine, make_url
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import get_settings


def normalize_database_url(database_url: str) -> str:
    """Make common PostgreSQL URLs use the installed psycopg 3 driver."""
    if database_url.startswith("postgres://"):
        return "postgresql+psycopg://" + database_url.removeprefix("postgres://")
    if database_url.startswith("postgresql://"):
        return "postgresql+psycopg://" + database_url.removeprefix("postgresql://")
    return database_url


def _enable_sqlite_foreign_keys(
    dbapi_connection: Any,
    _connection_record: Any,
) -> None:
    """Enforce foreign keys, which SQLite disables by default."""
    cursor = dbapi_connection.cursor()
    try:
        cursor.execute("PRAGMA foreign_keys=ON")
    finally:
        cursor.close()


def create_db_engine(
    database_url: str | None = None,
    *,
    echo: bool | None = None,
) -> Engine:
    """Create an engine for SQLite (dev/tests) or PostgreSQL (production).

    In-memory SQLite is pinned to a single connection with ``StaticPool`` so
    every session in a test sees the same database.
    """
    settings = get_settings()
    url = make_url(normalize_database_url(database_url or settings.database_url))

    engine_options: dict[str, Any] = {
        "echo": settings.sql_echo if echo is None else echo,
        "pool_pre_ping": True,
        "future": True,
    }

    if url.get_backend_name() == "sqlite":
        # FastAPI runs sync endpoints in worker threads, so connections may be
        # used from a different thread than the one that opened them.
        engine_options["connect_args"] = {"check_same_thread": False}
        if url.database in (None, "", ":memory:"):
            engine_options["poolclass"] = StaticPool

    engine = create_engine(url, **engine_options)

    if engine.dialect.name == "sqlite":
        event.listen(engine, "connect", _enable_sqlite_foreign_keys)

    return engine


engine = create_db_engine()

SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    autoflush=False,
    expire_on_commit=False,
)


def get_db() -> Iterator[Session]:
    """Yield a request-scoped session and always close it afterwards."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
