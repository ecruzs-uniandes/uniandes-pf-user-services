from os import getenv


class Settings:
    def __init__(self):
        self.DATABASE_URL = getenv(
            "DATABASE_URL",
            "postgresql+asyncpg://travelhub:travelhub_dev@localhost:5432/travelhub_users"
        )
        self.DATABASE_URL_SYNC = getenv(
            "DATABASE_URL_SYNC",
            "postgresql+psycopg2://travelhub:travelhub_dev@localhost:5432/travelhub_users"
        )
        self.JWT_SECRET_KEY = getenv(
            "JWT_SECRET_KEY",
            "dev-secret-key-change-in-production"
        )
        self.JWT_ALGORITHM = getenv("JWT_ALGORITHM", "RS256")
        self.JWT_ISSUER = getenv("JWT_ISSUER", "https://auth.travelhub.app")
        self.JWT_AUDIENCE = getenv("JWT_AUDIENCE", "travelhub-api")
        self.JWT_ACCESS_TTL = int(getenv("JWT_ACCESS_TTL", "900"))
        self.JWT_REFRESH_TTL = int(getenv("JWT_REFRESH_TTL", "604800"))
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
        self.REFRESH_TOKEN_EXPIRE_DAYS = int(getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
        self.BCRYPT_ROUNDS = int(getenv("BCRYPT_ROUNDS", "12"))
        self.MAX_LOGIN_ATTEMPTS = int(getenv("MAX_LOGIN_ATTEMPTS", "5"))
        self.LOCKOUT_MINUTES = int(getenv("LOCKOUT_MINUTES", "15"))
        self.RATE_LIMIT_REQUESTS = int(getenv("RATE_LIMIT_REQUESTS", "100"))
        self.RATE_LIMIT_WINDOW_SECONDS = int(getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))
        self.ENVIRONMENT = getenv("ENVIRONMENT", "development")
        self.DEBUG = getenv("DEBUG", "True") == "True"


settings = Settings()