"""Daily activity values recorded for a user and metric."""

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, Float, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.db.models.metric import MetricDefinition
    from app.db.models.user import User


class Activity(TimestampMixin, Base):
    """One metric value for one user on one calendar day."""

    __tablename__ = "activities"
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "metric_id",
            "date",
            name="uq_activities_user_metric_date",
        ),
        Index("ix_activities_user_id_date", "user_id", "date"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    metric_id: Mapped[int] = mapped_column(
        ForeignKey("metric_definitions.id", ondelete="RESTRICT"),
        nullable=False,
    )
    date: Mapped[date] = mapped_column(Date, nullable=False)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    source: Mapped[str] = mapped_column(
        String(32),
        default="manual",
        server_default="manual",
        nullable=False,
    )

    user: Mapped["User"] = relationship(back_populates="activities")
    metric: Mapped["MetricDefinition"] = relationship(back_populates="activities")
