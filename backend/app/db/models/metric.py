"""Metric definitions such as coding hours or GitHub commits."""

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String, false
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.db.models.activity import Activity


class MetricDefinition(TimestampMixin, Base):
    """A quantifiable productivity metric tracked over time."""

    __tablename__ = "metric_definitions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    unit: Mapped[str] = mapped_column(String(32))
    is_builtin: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default=false(),
        nullable=False,
    )

    activities: Mapped[list["Activity"]] = relationship(back_populates="metric")
