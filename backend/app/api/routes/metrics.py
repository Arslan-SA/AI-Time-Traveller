"""Metric definition endpoints."""

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.api.deps import CurrentUser, DbSession
from app.api.schemas.metric import MetricCreate, MetricRead
from app.db.models import MetricDefinition

router = APIRouter(prefix="/metrics")


@router.get("", response_model=list[MetricRead])
def list_metrics(
    _current_user: CurrentUser,
    db: DbSession,
) -> list[MetricDefinition]:
    """List every built-in and custom metric definition."""
    return list(
        db.scalars(
            select(MetricDefinition).order_by(
                MetricDefinition.is_builtin.desc(),
                MetricDefinition.name,
            )
        ).all()
    )


@router.post(
    "",
    response_model=MetricRead,
    status_code=status.HTTP_201_CREATED,
)
def create_metric(
    payload: MetricCreate,
    _current_user: CurrentUser,
    db: DbSession,
) -> MetricDefinition:
    """Create a custom metric definition."""
    existing = db.scalar(
        select(MetricDefinition).where(MetricDefinition.name == payload.name)
    )
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Metric '{payload.name}' already exists",
        )

    metric = MetricDefinition(
        name=payload.name,
        unit=payload.unit,
        is_builtin=False,
    )
    db.add(metric)
    try:
        db.commit()
    except IntegrityError:
        # The unique name check can still race with another request.
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Metric '{payload.name}' already exists",
        ) from None

    db.refresh(metric)
    return metric
