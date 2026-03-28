def hash_password(password: str) -> str:
    raise NotImplementedError


def verify_password(password: str, hashed: str) -> bool:
    raise NotImplementedError


def generate_totp_secret() -> str:
    raise NotImplementedError


def verify_totp(secret: str, code: str) -> bool:
    raise NotImplementedError
