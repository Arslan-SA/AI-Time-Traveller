"""Tests for the persistence layer."""

from datetime import date, datetime

import pytest
from sqlalchemy import func, inspect, select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.crypto import TokenEncryptionError, decrypt_token, encrypt_token
from app.db.models import (
    Activity,
    GithubConnection,
    MetricDefinition,
    SavedScenario,
    User,
)
from app.db.seed import BUILTIN_METRICS, seed_builtin_metrics
from app.db.session import normalize_database_url


def make_user(session: Session, email: str = "user@example.com") -> User:
    user = User(email=email, display_name="Test User")
    session.add(user)
    session.flush()
    return user


def test_tables_are_created(db_engine) -> None:
    assert set(inspect(db_engine).get_table_names()) == {
        "activities",
        "github_connections",
        "metric_definitions",
        "saved_scenarios",
        "users",
    }


def test_builtin_metrics_seed_is_idempotent(db_session: Session) -> None:
    assert seed_builtin_metrics(db_session) == 4
    assert seed_builtin_metrics(db_session) == 0
    db_session.commit()

    metrics = db_session.scalars(
        select(MetricDefinition).order_by(MetricDefinition.name)
    ).all()

    assert {metric.name for metric in metrics} == {
        definition["name"] for definition in BUILTIN_METRICS
    }
    assert all(metric.is_builtin for metric in metrics)
    assert {metric.name: metric.unit for metric in metrics}["leetcode"] == "problems"


def test_activity_is_unique_per_user_metric_and_date(
    db_session: Session, seeded_metrics: Session
) -> None:
    user = make_user(db_session)
    metric = db_session.scalar(
        select(MetricDefinition).where(MetricDefinition.name == "coding_hours")
    )
    assert metric is not None

    activity = Activity(
        user=user,
        metric=metric,
        date=date(2026, 1, 1),
        value=2.5,
    )
    db_session.add(activity)
    db_session.commit()
    assert activity.source == "manual"

    db_session.add(
        Activity(
            user_id=user.id,
            metric_id=metric.id,
            date=date(2026, 1, 1),
            value=4.0,
        )
    )
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()

    assert db_session.scalar(select(func.count()).select_from(Activity)) == 1


def test_sqlite_foreign_keys_are_enforced(db_session: Session) -> None:
    db_session.add(
        Activity(
            user_id=999,
            metric_id=999,
            date=date(2026, 1, 1),
            value=1.0,
        )
    )
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_github_token_is_encrypted_at_rest(db_session: Session) -> None:
    user = make_user(db_session)
    connection = GithubConnection(user=user, github_username="arslansa")
    connection.access_token = "ghp_super_secret"
    connection.last_synced_at = datetime(2026, 1, 2, 12, 0)
    db_session.add(connection)
    db_session.commit()
    db_session.expire_all()

    stored = db_session.get(GithubConnection, connection.id)
    assert stored is not None
    assert stored.encrypted_access_token != "ghp_super_secret"
    assert "ghp_super_secret" not in stored.encrypted_access_token
    assert stored.access_token == "ghp_super_secret"
    assert stored.last_synced_at is not None
    assert stored.last_synced_at.date() == date(2026, 1, 2)

    raw_token = db_session.execute(
        text("SELECT encrypted_access_token FROM github_connections")
    ).scalar_one()
    assert "ghp_super_secret" not in raw_token


def test_encryption_requires_the_same_secret_key() -> None:
    encrypted = encrypt_token("ghp_test_token")

    assert encrypted != "ghp_test_token"
    assert decrypt_token(encrypted) == "ghp_test_token"
    with pytest.raises(TokenEncryptionError):
        decrypt_token(encrypted, secret_key="a-different-key")


def test_saved_scenario_round_trips_json_overrides(
    db_session: Session,
) -> None:
    user = make_user(db_session)
    overrides = {
        "coding_hours_per_day": 4,
        "study_pause": {"start_day": 10, "duration_days": 10},
    }
    scenario = SavedScenario(
        user=user,
        name="Level up",
        horizon_days=90,
        overrides=overrides,
    )
    db_session.add(scenario)
    db_session.commit()
    db_session.expire_all()

    stored = db_session.get(SavedScenario, scenario.id)
    assert stored is not None
    assert stored.name == "Level up"
    assert stored.horizon_days == 90
    assert stored.overrides == overrides


def test_saved_scenario_rejects_non_positive_horizon(
    db_session: Session,
) -> None:
    user = make_user(db_session)
    db_session.add(
        SavedScenario(
            user=user,
            name="Invalid",
            horizon_days=0,
            overrides={},
        )
    )

    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_deleting_user_cascades_to_owned_rows(
    db_session: Session, seeded_metrics: Session
) -> None:
    user = make_user(db_session)
    metric = db_session.scalar(
        select(MetricDefinition).where(MetricDefinition.name == "coding_hours")
    )
    assert metric is not None

    connection = GithubConnection(user=user, github_username="arslansa")
    connection.access_token = "ghp_token"
    scenario = SavedScenario(
        user=user,
        name="Sprint",
        horizon_days=30,
        overrides={"coding_hours_per_day": 3},
    )
    activity = Activity(
        user=user,
        metric=metric,
        date=date(2026, 1, 3),
        value=3.0,
    )
    db_session.add_all([connection, scenario, activity])
    db_session.commit()

    db_session.delete(user)
    db_session.commit()

    for model in (Activity, GithubConnection, SavedScenario):
        assert db_session.scalar(select(func.count()).select_from(model)) == 0
    assert db_session.get(MetricDefinition, metric.id) is not None


def test_postgres_urls_use_the_psycopg_driver() -> None:
    assert (
        normalize_database_url("postgresql://user:pass@localhost/db")
        == "postgresql+psycopg://user:pass@localhost/db"
    )
    assert (
        normalize_database_url("postgres://user:pass@localhost/db")
        == "postgresql+psycopg://user:pass@localhost/db"
    )
    assert (
        normalize_database_url("sqlite:///./time_traveler.db")
        == "sqlite:///./time_traveler.db"
    )


def test_client_fixture_uses_the_in_memory_database(client) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
