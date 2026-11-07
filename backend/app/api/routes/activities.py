"""Activity endpoints."""

from datetime import date
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.api.deps import CurrentUser, DbSession
from app.api.schemas.activity import ActivityCreate, ActivityPage, ActivityRead
from app.db.models import Activity, MetricDefinition

router = APIRouter(prefix="/activities")


def _resolve_metrics(
    db: Session,
    entries: list[ActivityCreate],
) -> dict[str, MetricDefinition]:
    """Return metrics keyed by name, rejecting unknown metric names."""
    names = {entry.metric for entry in entries}
    metrics = {
        metric.name: metric
        for metric in db.scalars(
            select(MetricDefinition).where(MetricDefinition.name.in_(names))
        )
    }

    missing = sorted(names - metrics.keys())
    if missing:
        raise HTTPException(
            status_code=422,
            detail=f"Unknown metric(s): {', '.join(missing)}",
        )

    return metrics


@router.post("", response_model=list[ActivityRead], status_code=status.HTTP_200_OK)
def upsert_activities(
    payload: ActivityCreate | list[ActivityCreate],
    current_user: CurrentUser,
    db: DbSession,
) -> list[Activity]:
    """Create or update one or many manual activity entries.

    Entries are keyed by the current user, metric and date. If the same key
    appears more than once in one request, the last entry wins.
    """
    entries = payload if isinstance(payload, list) else [payload]
    if not entries:
        raise HTTPException(
            status_code=422,
            detail="At least one activity entry is required",
        )

    metrics = _resolve_metrics(db, entries)
    deduped = {(entry.metric, entry.date): entry for entry in entries}

    metric_ids = {metrics[metric_name].id for metric_name, _ in deduped}
    dates = {activity_date for _, activity_date in deduped}
    existing = {
        (activity.metric_id, activity.date): activity
        for activity in db.scalars(
            select(Activity)
            .options(selectinload(Activity.metric))
            .where(
                Activity.user_id == current_user.id,
                Activity.metric_id.in_(metric_ids),
                Activity.date.in_(dates),
            )
        )
    }

    activities: list[Activity] = []
    for (metric_name, activity_date), entry in deduped.items():
        metric = metrics[metric_name]
        activity = existing.get((metric.id, activity_date))

        if activity is None:
            activity = Activity(
                user_id=current_user.id,
                metric=metric,
                date=activity_date,
                value=entry.value,
                source=entry.source,
            )
            db.add(activity)
            existing[(metric.id, activity_date)] = activity
        else:
            activity.value = entry.value
            activity.source = entry.source

        activities.append(activity)

    db.commit()

    # Reload with the metric relationship and server-generated timestamps
    # populated, preserving the request order in the response.
    activity_ids = [activity.id for activity in activities]
    refreshed = {
        activity.id: activity
        for activity in db.scalars(
            select(Activity)
            .options(selectinload(Activity.metric))
            .where(Activity.id.in_(activity_ids))
        )
    }
    return [refreshed[activity_id] for activity_id in activity_ids]


@router.get("", response_model=ActivityPage)
def list_activities(
    current_user: CurrentUser,
    db: DbSession,
    from_: Annotated[
        date | None,
        Query(alias="from", description="Inclusive start date (YYYY-MM-DD)"),
    ] = None,
    to: Annotated[
        date | None,
        Query(description="Inclusive end date (YYYY-MM-DD)"),
    ] = None,
    metric: Annotated[
        str | None,
        Query(min_length=1, max_length=64, description="Filter by metric name"),
    ] = None,
    limit: Annotated[int, Query(ge=1, le=500)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> ActivityPage:
    """List the current user's activities, newest first.

    ``from`` and ``to`` are inclusive date bounds. ``total`` counts every row
    matching the filters before ``limit`` and ``offset`` are applied.
    """
    if from_ is not None and to is not None and from_ > to:
        raise HTTPException(
            status_code=422,
            detail="'from' must be on or before 'to'",
        )

    filters = [Activity.user_id == current_user.id]
    if from_ is not None:
        filters.append(Activity.date >= from_)
    if to is not None:
        filters.append(Activity.date <= to)
    if metric is not None:
        filters.append(Activity.metric.has(MetricDefinition.name == metric))

    total = db.scalar(select(func.count()).select_from(Activity).where(*filters)) or 0
    items = db.scalars(
        select(Activity)
        .options(selectinload(Activity.metric))
        .where(*filters)
        .order_by(Activity.date.desc(), Activity.id.desc())
        .limit(limit)
        .offset(offset)
    ).all()

    return ActivityPage(items=items, total=total, limit=limit, offset=offset)
