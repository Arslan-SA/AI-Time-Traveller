"""Tests for the manual activity API."""

from datetime import date, timedelta

import pytest
from sqlalchemy import func, select

from app.api.deps import DEV_USER_EMAIL
from app.db.models import Activity, MetricDefinition, User


def days_ago(days: int) -> date:
    return date.today() - timedelta(days=days)


def activity_payload(
    metric: str = "coding_hours",
    *,
    days: int = 1,
    value: float = 1.0,
    **extra: object,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "metric": metric,
        "date": days_ago(days).isoformat(),
        "value": value,
    }
    payload.update(extra)
    return payload


def seed_activities(client) -> None:
    response = client.post(
        "/api/activities",
        json=[
            activity_payload("coding_hours", days=5, value=1.0),
            activity_payload("coding_hours", days=3, value=2.0),
            activity_payload("study_hours", days=3, value=3.0),
            activity_payload("study_hours", days=1, value=4.0),
        ],
    )
    assert response.status_code == 200


def test_post_single_activity(client, seeded_metrics) -> None:
    response = client.post(
        "/api/activities",
        json=activity_payload(value=2.5),
    )

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1

    activity = body[0]
    assert activity["metric"]["name"] == "coding_hours"
    assert activity["metric"]["unit"] == "hours"
    assert activity["metric"]["is_builtin"] is True
    assert activity["date"] == days_ago(1).isoformat()
    assert activity["value"] == 2.5
    assert activity["source"] == "manual"
    assert activity["created_at"]


def test_post_bulk_activities(client, seeded_metrics) -> None:
    response = client.post(
        "/api/activities",
        json=[
            activity_payload("coding_hours", days=2, value=1.5),
            activity_payload("study_hours", days=2, value=3.0),
        ],
    )

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2
    assert {item["metric"]["name"] for item in body} == {
        "coding_hours",
        "study_hours",
    }
    assert {item["value"] for item in body} == {1.5, 3.0}


def test_post_upserts_on_user_metric_date(
    client,
    seeded_metrics,
    db_session,
) -> None:
    first = client.post(
        "/api/activities",
        json=activity_payload(value=1.0),
    ).json()[0]

    second = client.post(
        "/api/activities",
        json=activity_payload(value=6.5),
    ).json()[0]

    assert second["id"] == first["id"]
    assert second["value"] == 6.5
    assert db_session.scalar(select(func.count()).select_from(Activity)) == 1

    listed = client.get("/api/activities").json()
    assert listed["total"] == 1
    assert listed["items"][0]["value"] == 6.5


def test_duplicate_entries_in_one_request_keep_last_value(
    client,
    seeded_metrics,
) -> None:
    response = client.post(
        "/api/activities",
        json=[
            activity_payload(value=1.0),
            activity_payload(value=9.0),
        ],
    )

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["value"] == 9.0


@pytest.mark.parametrize(
    "body",
    [
        {"metric": "coding_hours", "date": days_ago(1).isoformat(), "value": -0.1},
        {"date": days_ago(1).isoformat(), "value": 1.0},
        {"metric": "coding_hours", "date": "not-a-date", "value": 1.0},
        [],
    ],
)
def test_post_activity_validation_errors(
    client,
    seeded_metrics,
    body,
) -> None:
    response = client.post("/api/activities", json=body)

    assert response.status_code == 422


def test_future_date_is_rejected(client, seeded_metrics) -> None:
    response = client.post(
        "/api/activities",
        json=activity_payload(days=-1),
    )

    assert response.status_code == 422
    assert "future" in response.text


def test_unknown_metric_is_rejected(client, seeded_metrics) -> None:
    response = client.post(
        "/api/activities",
        json=activity_payload("not_a_metric"),
    )

    assert response.status_code == 422
    assert "Unknown metric" in response.text


def test_get_activities_filters_by_date_and_metric(
    client,
    seeded_metrics,
) -> None:
    seed_activities(client)

    all_activities = client.get("/api/activities").json()
    assert all_activities["total"] == 4
    assert all_activities["limit"] == 100
    assert all_activities["offset"] == 0
    dates = [item["date"] for item in all_activities["items"]]
    assert dates == sorted(dates, reverse=True)

    coding = client.get(
        "/api/activities",
        params={"metric": "coding_hours"},
    ).json()
    assert coding["total"] == 2
    assert {item["metric"]["name"] for item in coding["items"]} == {"coding_hours"}

    day = days_ago(3).isoformat()
    date_range = client.get(
        "/api/activities",
        params={"from": day, "to": day},
    ).json()
    assert date_range["total"] == 2
    assert {item["date"] for item in date_range["items"]} == {day}

    combined = client.get(
        "/api/activities",
        params={"metric": "study_hours", "from": day, "to": day},
    ).json()
    assert combined["total"] == 1
    assert combined["items"][0]["value"] == 3.0

    unknown = client.get(
        "/api/activities",
        params={"metric": "not_a_metric"},
    ).json()
    assert unknown["total"] == 0
    assert unknown["items"] == []


def test_get_activities_paginates(client, seeded_metrics) -> None:
    seed_activities(client)

    first_page = client.get(
        "/api/activities",
        params={"limit": 2, "offset": 0},
    ).json()
    second_page = client.get(
        "/api/activities",
        params={"limit": 2, "offset": 2},
    ).json()

    assert first_page["total"] == 4
    assert second_page["total"] == 4
    assert len(first_page["items"]) == 2
    assert len(second_page["items"]) == 2

    first_ids = {item["id"] for item in first_page["items"]}
    second_ids = {item["id"] for item in second_page["items"]}
    assert first_ids.isdisjoint(second_ids)
    assert len(first_ids | second_ids) == 4


@pytest.mark.parametrize(
    "params",
    [
        {"limit": 0},
        {"limit": 501},
        {"offset": -1},
        {"from": days_ago(1).isoformat(), "to": days_ago(3).isoformat()},
    ],
)
def test_get_activity_query_validation(
    client,
    seeded_metrics,
    params,
) -> None:
    response = client.get("/api/activities", params=params)

    assert response.status_code == 422


def test_get_activities_only_returns_current_user_rows(
    client,
    seeded_metrics,
    db_session,
) -> None:
    client.post(
        "/api/activities",
        json=activity_payload(value=2.0),
    )

    metric = db_session.scalar(
        select(MetricDefinition).where(MetricDefinition.name == "coding_hours")
    )
    assert metric is not None

    other_user = User(email="other@example.com")
    db_session.add(other_user)
    db_session.flush()
    db_session.add(
        Activity(
            user=other_user,
            metric=metric,
            date=days_ago(2),
            value=99.0,
        )
    )
    db_session.commit()

    listed = client.get("/api/activities").json()

    assert listed["total"] == 1
    assert listed["items"][0]["value"] == 2.0


def test_current_user_dependency_uses_one_dev_user(
    client,
    seeded_metrics,
    db_session,
) -> None:
    client.get("/api/activities")
    client.get("/api/activities")

    users = db_session.scalars(select(User)).all()

    assert [user.email for user in users] == [DEV_USER_EMAIL]
