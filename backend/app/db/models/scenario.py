"""Saved What-If scenarios."""

from typing import TYPE_CHECKING, Any

from sqlalchemy import JSON, CheckConstraint, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.db.models.user import User


class SavedScenario(TimestampMixin, Base):
    """A named simulation configuration a user can revisit."""

    __tablename__ = "saved_scenarios"
    __table_args__ = (
        CheckConstraint("horizon_days > 0", name="horizon_days_positive"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    horizon_days: Mapped[int] = mapped_column(Integer, nullable=False)
    overrides: Mapped[dict[str, Any]] = mapped_column(
        JSON,
        default=dict,
        nullable=False,
    )

    user: Mapped["User"] = relationship(back_populates="saved_scenarios")
