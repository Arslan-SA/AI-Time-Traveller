"""Symmetric encryption helpers for secrets stored in the database."""

import base64
import hashlib
from functools import lru_cache

from cryptography.fernet import Fernet, InvalidToken

from app.core.config import get_settings


class TokenEncryptionError(RuntimeError):
    """Raised when a stored token cannot be decrypted."""


def derive_fernet_key(secret_key: str) -> bytes:
    """Derive a valid Fernet key from the application ``SECRET_KEY``.

    SHA-256 gives us the 32 bytes Fernet requires, and urlsafe base64 makes
    the result a valid Fernet key. The SECRET_KEY itself never touches the
    database.
    """
    if not secret_key:
        raise ValueError("SECRET_KEY must not be empty")
    digest = hashlib.sha256(secret_key.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest)


@lru_cache(maxsize=8)
def _fernet(secret_key: str) -> Fernet:
    return Fernet(derive_fernet_key(secret_key))


def get_fernet() -> Fernet:
    """Return the Fernet instance for the configured application secret."""
    return _fernet(get_settings().secret_key)


def encrypt_token(token: str, *, secret_key: str | None = None) -> str:
    """Encrypt a plaintext token for storage."""
    if not token:
        raise ValueError("token must not be empty")
    fernet = _fernet(secret_key) if secret_key is not None else get_fernet()
    return fernet.encrypt(token.encode("utf-8")).decode("ascii")


def decrypt_token(encrypted_token: str, *, secret_key: str | None = None) -> str:
    """Decrypt a token previously returned by :func:`encrypt_token`."""
    fernet = _fernet(secret_key) if secret_key is not None else get_fernet()
    try:
        return fernet.decrypt(encrypted_token.encode("ascii")).decode("utf-8")
    except (InvalidToken, ValueError) as exc:
        raise TokenEncryptionError(
            "Stored token could not be decrypted. Was SECRET_KEY changed?"
        ) from exc
