def create_access_token(data: dict) -> str:
    raise NotImplementedError


def create_refresh_token(data: dict) -> str:
    raise NotImplementedError


def decode_token(token: str) -> dict:
    raise NotImplementedError
