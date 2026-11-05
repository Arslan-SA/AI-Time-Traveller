"""GitHub OAuth connection for a user."""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.crypto import decrypt_token, encrypt_token
from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.db.models.user import User


class GithubConnection(TimestampMixin, Base):
    """A user's GitHub link, with the access token encrypted at rest."""

    __tablename__ = "github_connections"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    github_username: Mapped[str | None] = mapped_column(String(100))
    encrypted_access_token: Mapped[str] = mapped_column(Text, nullable=False)
    last_synced_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    user: Mapped["User"] = relationship(back_populates="github_connection")

    @property
    def access_token(self) -> str:
        """Return the decrypted OAuth token."""
        return decrypt_token(self.encrypted_access_token)

    @access_token.setter
    def access_token(self, token: str) -> None:
        """Encrypt and store the OAuth token.

        Assign through this property (``connection.access_token = token``)
        rather than writing ``encrypted_access_token`` directly.
        """
        self.encrypted_access_token = encrypt_token(token)
