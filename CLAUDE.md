# CLAUDE.md — user-services

## Comandos

```bash
# Dev
docker-compose up -d                # PostgreSQL + servicio
docker-compose up -d db             # Solo BD (para uvicorn manual)
uvicorn app.main:app --reload --port 8000

# Tests
pytest                              # Todos
pytest --cov=app --cov-report=term-missing  # Con cobertura (≥80% en auth_service, auth_chain)
pytest tests/test_register.py -v    # Un archivo
pytest -k "test_login" -v           # Por nombre

# Migraciones (Alembic usa DATABASE_URL_SYNC con psycopg2, NO asyncpg)
alembic revision --autogenerate -m "descripción"
alembic upgrade head
alembic downgrade -1

# Lint
black app/ tests/ && isort app/ tests/
ruff check app/ tests/
mypy app/

# Docker build
docker build --target production -t gcr.io/<PROJECT_ID>/user-services:latest .
```

## Stack

Python 3.12 · FastAPI 0.115.6 · SQLAlchemy async 2.0.36 · asyncpg 0.30.0 · Pydantic 2.10.4 · Alembic 1.14.1 · bcrypt 4.2.1 · python-jose 3.3.0 · pyotp 2.9.0 · PostgreSQL 16

## Estructura

```
app/
├── main.py              # App, CORS, routers, health
├── config.py            # pydantic-settings, env vars
├── database.py          # AsyncSession, Base, get_db
├── models/user.py       # SQLAlchemy User
├── schemas/user.py      # Pydantic request/response
├── routers/auth.py      # Endpoints HTTP (sin lógica de negocio)
├── services/auth_service.py  # Toda la lógica de negocio
├── middleware/auth_chain.py  # Chain of Responsibility: RateLimit → Token → Role
└── utils/
    ├── jwt_handler.py   # JWT create/decode
    └── security.py      # bcrypt + TOTP
tests/
├── conftest.py          # Fixtures: async_client, test_db, test_user, auth_headers
├── test_register.py     # W07
├── test_login.py        # W08
├── test_auth_chain.py   # AH008
├── test_mfa.py          # MFA
└── test_health.py
```

## Arquitectura — Reglas obligatorias

- **Capas:** Router → Service → Model. Routers solo reciben/delegan. Services tienen la lógica. Models sin lógica.
- **Async everywhere:** Solo `AsyncSession` en endpoints. `psycopg2` solo en Alembic.
- **Chain of Responsibility (AH008):** Orden fijo `RateLimitFilter → TokenValidationFilter → RoleFilter`. Cada filtro hereda de `AuthFilter` con `set_next()` y `handle()`. No cambiar el orden.

## Convenciones

- Archivos: `snake_case.py` · Clases: `PascalCase` · URLs: `kebab-case` · Tablas: `snake_case` plural
- Tests: `test_<action>_<scenario>_<expected>` (ej. `test_register_duplicate_email_returns_409`)
- Errores: `HTTPException` con `{"detail": "Mensaje en español"}`
- Logging: `logging.getLogger(__name__)` — info (éxito), warning (fallo), error (sistema)

## Reglas de negocio clave

### Registro
- Password ≥ 8 chars, username ≥ 3 chars, email validado por Pydantic
- Email y username únicos (409 si duplicado)
- Rol default: `viajero`, MFA default: `False`
- Nunca retornar `hashed_password` ni `mfa_secret` en responses

### Login
- Verificar lockout (`locked_until`) ANTES de verificar password
- 5 intentos fallidos → bloqueo 15 min (423)
- Login exitoso → reset `failed_login_attempts` y `locked_until`
- MFA activo sin `totp_code` → 428; código inválido → 401

### JWT
- Access token: 30 min, payload `{sub, rol, type: "access", exp, iat}`
- Refresh token: 7 días, payload `{sub, type: "refresh", exp, iat}`
- Nunca aceptar refresh donde se espera access (y viceversa)

### MFA
- Setup genera secret base32 de 32 chars, QR URI `otpauth://totp/TravelHub:...`
- Verify con `valid_window=1` (±30s). Éxito → `mfa_activo = True`
- Verify sin setup previo → 400

## Códigos HTTP

| Código | Uso |
|--------|-----|
| 201 | Registro exitoso |
| 200 | Operación exitosa |
| 400 | MFA no configurado / datos inválidos |
| 401 | Credenciales / token inválido o expirado |
| 403 | Rol insuficiente (RBAC) |
| 409 | Email/username duplicado |
| 423 | Cuenta bloqueada |
| 428 | Código MFA requerido |

## NUNCA

- Contraseñas en texto plano o MD5/SHA — solo bcrypt
- Loguear passwords, tokens JWT, mfa_secret
- `from app.* import *` — imports explícitos
- Funciones > 40 líneas
- `try/except Exception: pass`
- `print()` en producción — usar logging
- SQL raw si SQLAlchemy ORM lo resuelve
- DELETE físico — usar soft delete (`activo = False`)
- SQLite en producción
