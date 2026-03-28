from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.user import (
    MFASetupResponse,
    MFAVerifyRequest,
    MessageResponse,
    RefreshTokenRequest,
    TokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
)
from app.services import auth_service

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(request: UserRegisterRequest, db: AsyncSession = Depends(get_db)):
    return await auth_service.register_user(request, db)


@router.post("/login", response_model=TokenResponse)
async def login(request: UserLoginRequest, db: AsyncSession = Depends(get_db)):
    raise NotImplementedError


@router.post("/refresh", response_model=TokenResponse)
async def refresh(request: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    raise NotImplementedError


@router.get("/me", response_model=UserResponse)
async def get_me():
    raise NotImplementedError


@router.post("/mfa/setup", response_model=MFASetupResponse)
async def mfa_setup():
    raise NotImplementedError


@router.post("/mfa/verify", response_model=MessageResponse)
async def mfa_verify(request: MFAVerifyRequest):
    raise NotImplementedError
