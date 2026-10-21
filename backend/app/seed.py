"""Conteúdo inicial do site.

Somente informações fornecidas pelo próprio Flayks. Nada aqui deve ser acrescentado sem
confirmação dele: sem clientes, métricas, empregos ou diplomas inventados.
"""

from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .models import Project, SiteContent, TimelineItem

DEFAULT_CONTENT: dict[str, str] = {
    "positioning": "Software Engineer • Founder • AI & Cybersecurity",
    "intro": (
        "Engenheiro de software e fundador da Netsenti AI. Construo produtos digitais na "
        "interseção entre inteligência artificial e cibersegurança e desenvolvo o LarMatch, "
        "uma plataforma para tornar a busca por imóveis mais inteligente e personalizada."
    ),
    "about": (
        "Sou fundador da Netsenti AI, uma iniciativa brasileira voltada à interseção entre "
        "Inteligência Artificial e Cibersegurança, e desenvolvo o LarMatch, uma plataforma que "
        "busca tornar a procura por imóveis mais inteligente e personalizada.\n\n"
        "Desenvolvo sites e aplicativos Android. Em 2026, concluí cursos na Alura em React, "
        "TypeScript, JavaScript, Python, APIs, segurança em nuvem e engenharia de dados, entre outros.\n\n"
        "Meu projeto de IA foi selecionado para o SusHi Tech Tokyo 2026, onde estive em Tóquio "
        "como representante brasileiro."
    ),
    "availability": (
        "Aberto a oportunidades como desenvolvedor. Trabalho bem em equipe e prefiro o regime de home office."
    ),
    "email": "flayksdev@gmail.com",
    "linkedin_url": "https://www.linkedin.com/in/flayks-oliveira/",
    "github_url": "https://github.com/flayksdev",
    "photo_caption": "Tokyo Big Sight, durante o SusHi Tech Tokyo 2026, com a bandeira de Vila Velha.",
    "skills": (
        "Front-end: HTML5, CSS3, JavaScript, TypeScript, React, Next.js\n"
        "Back-end e dados: Node.js, Python, APIs, bancos de dados\n"
        "Ferramentas: Git, GitHub\n"
        "Plataformas: Web, Android\n"
        "Áreas de atuação e estudo: Engenharia de software, Inteligência Artificial, Cibersegurança\n"
        "Idiomas: Português do Brasil, Inglês (intermediário)"
    ),
}

DEFAULT_PROJECTS: list[dict] = [
    {
        "slug": "larmatch",
        "title": "LarMatch",
        "summary": (
            "Plataforma que busca tornar a procura por imóveis mais inteligente e personalizada, "
            "com descoberta e matching de imóveis de acordo com o perfil de cada pessoa."
        ),
        "status": "em_desenvolvimento",
        "url": None,
        "repo_url": None,
        "tags": ["Produto digital", "Imóveis"],
        "position": 0,
    },
    {
        "slug": "netsenti-ai",
        "title": "Netsenti AI",
        "summary": (
            "Iniciativa brasileira voltada à interseção entre Inteligência Artificial e "
            "Cibersegurança. Protótipo em desenvolvimento, ainda sem usuários."
        ),
        "status": "prototipo",
        "url": "https://netsenti.com",
        "repo_url": None,
        "tags": ["IA", "Cibersegurança"],
        "position": 1,
    },
]

DEFAULT_TIMELINE: list[dict] = [
    {
        "kind": "reconhecimento",
        "title": "International AI Awards 2026: Bronze Winner, Best AI Innovation",
        "description": "",
        "date_label": "2026",
        "position": 0,
    },
    {
        "kind": "evento",
        "title": "SusHi Tech Tokyo 2026",
        "description": (
            "Representante brasileiro no evento, realizado no Tokyo Big Sight, em Tóquio. "
            "Meu projeto de IA foi selecionado para o Japão."
        ),
        "date_label": "Abril de 2026",
        "position": 1,
    },
    {
        "kind": "curso",
        "title": "Cursos concluídos na Alura",
        "description": (
            "React 19, React com TypeScript, React full stack, JavaScript, HTML e CSS, Python, "
            "Padrões de API, Lógica de programação, Pensamento computacional, Internet, trilhas "
            "introdutórias de Node.js, Cloud Security, Engenharia de Dados, Governança de Dados e UI Design."
        ),
        "date_label": "2026",
        "position": 2,
    },
]


def seed_if_empty(db: Session) -> bool:
    """Carrega o conteúdo inicial só se o site ainda não tem nenhum texto salvo."""
    existing = db.scalar(select(func.count()).select_from(SiteContent))
    if existing:
        return False
    for key, value in DEFAULT_CONTENT.items():
        db.add(SiteContent(key=key, value=value))
    for item in DEFAULT_PROJECTS:
        db.add(Project(**item, visible=True))
    for item in DEFAULT_TIMELINE:
        db.add(TimelineItem(**item, visible=True))
    db.commit()
    return True
