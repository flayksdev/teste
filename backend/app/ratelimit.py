from __future__ import annotations

import threading
import time
from collections import deque

from fastapi import HTTPException


class RateLimiter:
    """Janela deslizante em memória.

    Vale para um único processo. Com vários workers/réplicas, cada um mantém a sua
    própria contagem; para limites globais use um armazenamento compartilhado (ex.: Redis).
    """

    def __init__(self, limit: int, window_seconds: int) -> None:
        self.limit = limit
        self.window = window_seconds
        self._events: dict[str, deque[float]] = {}
        self._lock = threading.Lock()

    def hit(self, key: str) -> int | None:
        """Registra o evento. Retorna None se permitido, ou os segundos até liberar."""
        now = time.monotonic()
        with self._lock:
            if len(self._events) > 10_000:
                self._purge(now)
            bucket = self._events.setdefault(key, deque())
            while bucket and now - bucket[0] >= self.window:
                bucket.popleft()
            if len(bucket) >= self.limit:
                return max(1, int(self.window - (now - bucket[0])))
            bucket.append(now)
            return None

    def reset(self) -> None:
        with self._lock:
            self._events.clear()

    def _purge(self, now: float) -> None:
        for key in [k for k, b in self._events.items() if not b or now - b[-1] >= self.window]:
            del self._events[key]


def enforce(limiter: RateLimiter, key: str) -> None:
    retry_after = limiter.hit(key)
    if retry_after is not None:
        raise HTTPException(
            status_code=429,
            detail="Muitas tentativas. Aguarde um pouco e tente de novo.",
            headers={"Retry-After": str(retry_after)},
        )


login_ip_limiter = RateLimiter(limit=10, window_seconds=15 * 60)
login_email_limiter = RateLimiter(limit=5, window_seconds=15 * 60)
contact_limiter = RateLimiter(limit=5, window_seconds=60 * 60)
ask_ip_limiter = RateLimiter(limit=10, window_seconds=60 * 60)
ask_global_limiter = RateLimiter(limit=300, window_seconds=24 * 60 * 60)

_ALL = (login_ip_limiter, login_email_limiter, contact_limiter, ask_ip_limiter, ask_global_limiter)


def reset_all() -> None:
    for limiter in _ALL:
        limiter.reset()
