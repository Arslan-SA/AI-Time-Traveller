"""Activity request and response schemas."""

from datetime import date, datetime
from typing import Annotated

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    field_validator,
)

from app.api.schemas.metric import MetricName, MetricRead

ActivitySource = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=32),
]


class ActivityCreate(BaseModel):
    """One manual activity entry.

    Metric existence is checked against the database in the route because
    custom metrics are user-defined. Value and date rules are enforced here so
    malformed payloads fail before reaching the database.
    """

    model_config = ConfigDict(extra="forbid")

    metric: MetricName
    date: date
    value: float = Field(ge=0, allow_inf_nan=False)
    source: ActivitySource = "manual"

    @field_validator("date")
    @classmethod
    def reject_future_date(cls, value: date) -> date:
        """Activities describe the past; future dates are forecasts."""
        if value > date.today():
            raise ValueError("activity date cannot be in the future")
        return value


class ActivityRead(BaseModel):
    """A stored activity, with its metric expanded for clients."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    metric: MetricRead
    date: date
    value: float
    source: str
    created_at: datetime


class ActivityPage(BaseModel):
    """A page of activities plus the total matching count."""

    items: list[ActivityRead]
    total: int
    limit: int
    offset: int
