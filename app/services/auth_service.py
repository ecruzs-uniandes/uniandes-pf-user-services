from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import (
    MFASetupResponse,
    MessageResponse,
    TokenResponse,
    UserRegisterRequest,
    UserResponse,
)


async def register_user(request: UserRegisterRequest, db: AsyncSession) -> UserResponse:
    raise NotImplementedError


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
