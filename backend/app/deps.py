from __future__ import annotations

from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from .config import get_settings
from .db import get_db
from .models import AdminUser
from .security import SESSION_COOKIE, decode_token

_SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}


def client_ip(request: Request) -> str:
    """IP do cliente. O X-Forwarded-For só é considerado atrás de proxy confiável."""
    if get_settings().trust_proxy:
        forwarded = request.headers.get("x-forwarded-for", "")
        if forwarded:
            # O último valor é o acrescentado pelo nosso próprio proxy.
            return forwarded.split(",")[-1].strip() or "unknown"
    return request.client.host if request.client else "unknown"


def current_admin(request: Request, db: Session = Depends(get_db)) -> AdminUser:
    token = request.cookies.get(SESSION_COOKIE)
    user_id = decode_token(token) if token else None
    user = db.get(AdminUser, user_id) if user_id is not None else None
    if user is None:
        raise HTTPException(status_code=401, detail="Não autenticado")
    return user


def require_csrf_header(request: Request) -> None:
    """Defesa extra contra CSRF: mutações exigem um cabeçalho que formulários cross-site não enviam."""
    if request.method not in _SAFE_METHODS and request.headers.get("x-requested-with") != "fetch":
        raise HTTPException(status_code=403, detail="Requisição inválida")
