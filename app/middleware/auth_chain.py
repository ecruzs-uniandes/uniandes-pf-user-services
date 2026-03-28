import logging
import uuid as uuid_mod
from abc import ABC, abstractmethod

from fastapi import HTTPException, Request

from app.utils.jwt_handler import decode_token

logger = logging.getLogger(__name__)


class AuthFilter(ABC):
    def __init__(self):
        self._next: AuthFilter | None = None

    def set_next(self, handler: "AuthFilter") -> "AuthFilter":
        self._next = handler
        return handler

    @abstractmethod
    async def handle(self, request: Request) -> dict:
        pass

    async def _call_next(self, request: Request) -> dict:
        if self._next:
            return await self._next.handle(request)
        return request.state.token_payload


class RateLimitFilter(AuthFilter):
    async def handle(self, request: Request) -> dict:
        return await self._call_next(request)


class TokenValidationFilter(AuthFilter):
    async def handle(self, request: Request) -> dict:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token no proporcionado")

        token = auth_header.split(" ", 1)[1]
        try:
            payload = decode_token(token)
        except Exception:
            raise HTTPException(status_code=401, detail="Token inválido o expirado")

        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Se esperaba un access token")

        request.state.token_payload = payload
        return await self._call_next(request)


class RoleFilter(AuthFilter):
    def __init__(self, allowed_roles: list[str] | None = None):
        super().__init__()
        self._allowed_roles = allowed_roles or []

    async def handle(self, request: Request) -> dict:
        payload = request.state.token_payload
        if self._allowed_roles and payload.get("rol") not in self._allowed_roles:
            raise HTTPException(status_code=403, detail="Rol insuficiente")
        return await self._call_next(request)


def build_auth_chain(allowed_roles: list[str] | None = None) -> AuthFilter:
    rate_limit = RateLimitFilter()
    token_validation = TokenValidationFilter()
    role_filter = RoleFilter(allowed_roles)

    rate_limit.set_next(token_validation)
    token_validation.set_next(role_filter)

    return rate_limit


async def get_current_user_id(request: Request) -> str:
    chain = build_auth_chain()
    payload = await chain.handle(request)
    return payload["sub"]


def require_roles(allowed_roles: list[str]):
    async def dependency(request: Request) -> str:
        chain = build_auth_chain(allowed_roles)
        payload = await chain.handle(request)
        return payload["sub"]
    return dependency
