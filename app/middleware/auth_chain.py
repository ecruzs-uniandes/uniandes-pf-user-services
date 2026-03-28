from abc import ABC, abstractmethod

from fastapi import Request


class AuthFilter(ABC):
    def __init__(self):
        self._next: AuthFilter | None = None

    def set_next(self, handler: "AuthFilter") -> "AuthFilter":
        self._next = handler
        return handler

    @abstractmethod
    async def handle(self, request: Request) -> dict | None:
        raise NotImplementedError


class RateLimitFilter(AuthFilter):
    async def handle(self, request: Request) -> dict | None:
        raise NotImplementedError


class TokenValidationFilter(AuthFilter):
    async def handle(self, request: Request) -> dict | None:
        raise NotImplementedError


class RoleFilter(AuthFilter):
    def __init__(self, allowed_roles: list[str] | None = None):
        super().__init__()
        self._allowed_roles = allowed_roles or []

    async def handle(self, request: Request) -> dict | None:
        raise NotImplementedError
