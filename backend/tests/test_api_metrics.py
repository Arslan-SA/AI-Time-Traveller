"""Tests for metric definition endpoints."""

from datetime import date, timedelta

import pytest
from sqlalchemy import select

from app.api.deps import DEV_USER_EMAIL
from app.db.models import User


def test_list_metrics_returns_builtins(client, seeded_metrics) -> None:
    response = client.get("/api/metrics")

    assert response.status_code == 200
    body = response.json()
    assert {metric["name"] for metric in body} == {
        "coding_hours",
        "study_hours",
        "leetcode",
        "github_commits",
    }
    assert all(metric["is_builtin"] for metric in body)


def test_create_custom_metric(client, seeded_metrics) -> None:
    response = client.post(
        "/api/metrics",
        json={"name": "reading", "unit": "pages"},
    )

    assert response.status_code == 201
    metric = response.json()
    assert metric["name"] == "reading"
    assert metric["unit"] == "pages"
    assert metric["is_builtin"] is False
    assert metric["id"]

    listed = client.get("/api/metrics").json()
    assert "reading" in {item["name"] for item in listed}


def test_create_duplicate_metric_returns_conflict(client) -> None:
    payload = {"name": "reading", "unit": "pages"}
    first = client.post("/api/metrics", json=payload)
    second = client.post("/api/metrics", json=payload)

    assert first.status_code == 201
    assert second.status_code == 409
    assert "already exists" in second.json()["detail"]


@pytest.mark.parametrize(
    "body",
    [
        {},
        {"name": "", "unit": "pages"},
        {"name": "reading", "unit": ""},
        {"name": "reading", "unit": "pages", "is_builtin": True},
        {"name": "x" * 65, "unit": "pages"},
    ],
)
def test_create_metric_validation(client, body) -> None:
    response = client.post("/api/metrics", json=body)

    assert response.status_code == 422


def test_custom_metric_can_be_used_for_activity(client) -> None:
    created = client.post(
        "/api/metrics",
        json={"name": "reading", "unit": "pages"},
    )
    assert created.status_code == 201

    posted = client.post(
        "/api/activities",
        json={
            "metric": "reading",
            "date": (date.today() - timedelta(days=1)).isoformat(),
            "value": 12,
        },
    )
    assert posted.status_code == 200

    listed = client.get(
        "/api/activities",
        params={"metric": "reading"},
    ).json()
    assert listed["total"] == 1
    assert listed["items"][0]["metric"]["unit"] == "pages"


def test_metric_endpoints_use_the_fixed_dev_user(client, db_session) -> None:
    client.get("/api/metrics")
    client.get("/api/metrics")

    users = db_session.scalars(select(User)).all()

    assert [user.email for user in users] == [DEV_USER_EMAIL]
