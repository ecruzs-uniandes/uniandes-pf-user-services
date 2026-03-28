import logging

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import (
    MFASetupResponse,
    MessageResponse,
    TokenResponse,
    UserRegisterRequest,
    UserResponse,
)
from app.utils.security import hash_password

logger = logging.getLogger(__name__)


async def register_user(request: UserRegisterRequest, db: AsyncSession) -> UserResponse:
    result = await db.execute(
        select(User).where(
            (User.email == request.email) | (User.username == request.username)
        )
    )
    existing = result.scalar_one_or_none()

    if existing:
        field = "email" if existing.email == request.email else "username"
        raise HTTPException(
            status_code=409,
            detail=f"Ya existe un usuario con ese {field}",
        )

    user = User(
        email=request.email,
        username=request.username,
        nombre=request.nombre,
        hashed_password=hash_password(request.password),
        telefono=request.telefono,
        pais=request.pais,
        idioma=request.idioma,
        moneda_preferida=request.moneda_preferida,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    logger.info("Usuario registrado: %s", user.email)
    return UserResponse.model_validate(user)


async def login_user(email: str, password: str, totp_code: str | None, db: AsyncSession) -> TokenResponse:
    raise NotImplementedError


async def refresh_tokens(refresh_token: str, db: AsyncSession) -> TokenResponse:
    raise NotImplementedError


async def get_current_user(user_id: str, db: AsyncSession) -> UserResponse:
    raise NotImplementedError


async def setup_mfa(user_id: str, db: AsyncSession) -> MFASetupResponse:
    raise NotImplementedError


async def verify_mfa(user_id: str, totp_code: str, db: AsyncSession) -> MessageResponse:
    raise NotImplementedError
