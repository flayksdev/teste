from __future__ import annotations

import time

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError

from .config import get_settings

_hasher = PasswordHasher()
# Hash descartável: usado para gastar o mesmo tempo quando o e-mail não existe.
_DUMMY_HASH = _hasher.hash("senha-descartavel-para-igualar-tempo")

SESSION_COOKIE = "session"
_ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    return _hasher.hash(password)


def verify_password(password_hash: str, password: str) -> bool:
    try:
        return _hasher.verify(password_hash, password)
    except (VerificationError, InvalidHashError):
        return False


def spend_dummy_verification(password: str) -> None:
    verify_password(_DUMMY_HASH, password)


def create_token(user_id: int) -> str:
    settings = get_settings()
    now = int(time.time())
    payload = {"sub": str(user_id), "iat": now, "exp": now + settings.access_token_minutes * 60}
    return jwt.encode(payload, settings.secret_key, algorithm=_ALGORITHM)


def decode_token(token: str) -> int | None:
    try:
        payload = jwt.decode(
            token,
            get_settings().secret_key,
            algorithms=[_ALGORITHM],
            options={"require": ["exp", "sub"]},
        )
        return int(payload["sub"])
    except (jwt.PyJWTError, ValueError, KeyError):
        return None
