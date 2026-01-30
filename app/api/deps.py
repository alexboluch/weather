from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader

from app.config import settings


api_key_header = APIKeyHeader(name="x-token", auto_error=False)


def validate_token(token: str = Security(api_key_header)):
    if not token or token != settings.STATIC_TOKEN:
        raise HTTPException(
            status_code=403,
            detail="Forbidden: Invalid or missing x-token"
        )
    return token
