"""Shared pytest fixtures backed by an in-memory SQLite database."""

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.db import models  # noqa: F401  registers every table on Base.metadata
from app.db.base import Base
from app.db.seed import seed_builtin_metrics
from app.db.session import create_db_engine, get_db
from app.main import app


@pytest.fixture()
def db_engine() -> Iterator[Engine]:
    """Create a fresh in-memory database for a single test."""
    engine = create_db_engine("sqlite+pysqlite://")
    Base.metadata.create_all(engine)

    try:
        yield engine
    finally:
        Base.metadata.drop_all(engine)
        engine.dispose()


@pytest.fixture()
def db_session(db_engine: Engine) -> Iterator[Session]:
    """Yield a session bound to the test's in-memory database."""
    session_factory = sessionmaker(
        bind=db_engine,
        class_=Session,
        autoflush=False,
        expire_on_commit=False,
    )
    with session_factory() as session:
        yield session


@pytest.fixture()
def seeded_metrics(db_session: Session) -> Session:
    """Return a session that already contains the built-in metrics."""
    seed_builtin_metrics(db_session)
    db_session.commit()
    return db_session


@pytest.fixture()
def client(db_session: Session) -> Iterator[TestClient]:
    """FastAPI test client whose requests share the in-memory session."""

    def override_get_db() -> Iterator[Session]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.pop(get_db, None)
