from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import SiteContent

# Campos de texto editáveis no painel e o tamanho máximo de cada um.
CONTENT_LIMITS: dict[str, int] = {
    "positioning": 120,
    "intro": 600,
    "about": 3000,
    "availability": 300,
    "email": 254,
    "linkedin_url": 300,
    "github_url": 300,
    "photo_caption": 200,
    "skills": 1500,
}
URL_KEYS = {"linkedin_url", "github_url"}


def get_content(db: Session) -> dict[str, str]:
    rows = {row.key: row.value for row in db.scalars(select(SiteContent))}
    return {key: rows.get(key, "") for key in CONTENT_LIMITS}


def parse_skills(text: str) -> list[dict[str, object]]:
    """Cada linha no formato 'Grupo: item, item, item'."""
    groups: list[dict[str, object]] = []
    for line in text.splitlines():
        if ":" not in line:
            continue
        group, _, rest = line.partition(":")
        items = [item.strip() for item in rest.split(",") if item.strip()]
        if group.strip() and items:
            groups.append({"group": group.strip(), "items": items})
    return groups
