from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal
from urllib.parse import urlparse

from pydantic import AfterValidator, BaseModel, ConfigDict, EmailStr, Field, field_validator

ProjectStatus = Literal["em_desenvolvimento", "prototipo", "publicado"]
TimelineKind = Literal["reconhecimento", "evento", "curso", "formacao", "experiencia"]


def check_http_url(value: str | None) -> str | None:
    """Aceita apenas URLs http(s); string vazia vira None."""
    if value is None:
        return None
    value = value.strip()
    if value == "":
        return None
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc or len(value) > 500:
        raise ValueError("A URL deve começar com http:// ou https://")
    return value


OptionalUrl = Annotated[str | None, AfterValidator(check_http_url)]
Tag = Annotated[str, Field(min_length=1, max_length=30)]


# ---------- Público ----------
class PublicProject(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    slug: str
    title: str
    summary: str
    status: ProjectStatus
    url: str | None
    repo_url: str | None
    tags: list[str]


class PublicTimelineItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    kind: TimelineKind
    title: str
    description: str
    date_label: str


class SkillGroup(BaseModel):
    group: str
    items: list[str]


class SiteOut(BaseModel):
    content: dict[str, str]
    skills: list[SkillGroup]
    projects: list[PublicProject]
    timeline: list[PublicTimelineItem]
    assistant_enabled: bool


class ContactIn(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    email: EmailStr
    message: str = Field(min_length=10, max_length=4000)
    # Campo isca: humanos não o veem nem o preenchem.
    website: str = Field(default="", max_length=200)

    @field_validator("name", "message")
    @classmethod
    def _strip(cls, v: str) -> str:
        return v.strip()


class AskIn(BaseModel):
    question: str = Field(min_length=3, max_length=500)

    @field_validator("question")
    @classmethod
    def _strip(cls, v: str) -> str:
        return v.strip()


class AskOut(BaseModel):
    answer: str


# ---------- Autenticação ----------
class LoginIn(BaseModel):
    email: str = Field(min_length=3, max_length=254)
    password: str = Field(min_length=1, max_length=256)


class MeOut(BaseModel):
    email: str


# ---------- Administração ----------
class ContentUpdate(BaseModel):
    values: dict[str, str]


class ProjectIn(BaseModel):
    slug: str = Field(min_length=2, max_length=80, pattern=r"^[a-z0-9]+(-[a-z0-9]+)*$")
    title: str = Field(min_length=1, max_length=120)
    summary: str = Field(min_length=1, max_length=1200)
    status: ProjectStatus
    url: OptionalUrl = None
    repo_url: OptionalUrl = None
    tags: list[Tag] = Field(default_factory=list, max_length=12)
    position: int = Field(default=0, ge=0, le=1000)
    visible: bool = True


class ProjectOut(ProjectIn):
    model_config = ConfigDict(from_attributes=True)

    id: int


class TimelineIn(BaseModel):
    kind: TimelineKind
    title: str = Field(min_length=1, max_length=160)
    description: str = Field(default="", max_length=2000)
    date_label: str = Field(default="", max_length=40)
    position: int = Field(default=0, ge=0, le=1000)
    visible: bool = True


class TimelineOut(TimelineIn):
    model_config = ConfigDict(from_attributes=True)

    id: int


class MessageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    message: str
    created_at: datetime
    is_read: bool


class MessagePatch(BaseModel):
    is_read: bool
