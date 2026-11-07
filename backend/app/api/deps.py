"""Shared FastAPI dependencies."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.models import User
from app.db.session import get_db

DEV_USER_EMAIL = "dev@time-traveler.local"
DEV_USER_DISPLAY_NAME = "Development User"

DbSession = Annotated[Session, Depends(get_db)]


def get_current_user(db: DbSession) -> User:
    """Return the fixed development user until real authentication exists.

    Routes depend on :data:`CurrentUser` rather than this function directly,
    so replacing it with a JWT or session lookup does not touch any route.
    """
    user = db.scalar(select(User).where(User.email == DEV_USER_EMAIL))
    if user is not None:
        return user

    user = User(email=DEV_USER_EMAIL, display_name=DEV_USER_DISPLAY_NAME)
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        # A concurrent first request created the same user; fetch it instead.
        db.rollback()
        user = db.scalar(select(User).where(User.email == DEV_USER_EMAIL))
        if user is None:
            raise
        return user

    db.refresh(user)
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
