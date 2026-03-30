import secrets


def generate_token(length: int = 48) -> str:
    """Generate a URL-safe session token."""
    return secrets.token_urlsafe(length)
