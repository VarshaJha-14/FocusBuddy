"""
auth/clerk.py — Clerk JWT verification using PyJWT and Clerk's JWKS endpoint.
"""

import logging
from typing import Optional

import jwt
from jwt import PyJWKClient
from fastapi import Request, HTTPException

logger = logging.getLogger(__name__)

_jwks_client_cache: dict[str, PyJWKClient] = {}


def get_jwks_url(publishable_key: str) -> str:
    """
    Derive the JWKS URL from a Clerk publishable key.
    Format: pk_live_<base64> or pk_test_<base64>
    The base64 portion decodes to the frontend API URL.
    """
    import base64
    try:
        # Strip prefix and decode
        _, _, encoded = publishable_key.partition("_")[2].partition("_")
        # Clerk publishable key: pk_test_<encoded> or pk_live_<encoded>
        parts = publishable_key.split("_")
        # parts = ['pk', 'test'|'live', '<encoded>']
        encoded_part = parts[2]
        # Add padding if needed
        padded = encoded_part + "=" * (-len(encoded_part) % 4)
        frontend_api = base64.b64decode(padded).decode("utf-8").rstrip("$")
        return f"https://{frontend_api}/.well-known/jwks.json"
    except Exception as e:
        logger.error(f"Failed to derive JWKS URL from publishable key: {e}")
        raise ValueError("Invalid Clerk publishable key format") from e


def _get_jwks_client(publishable_key: str) -> PyJWKClient:
    """Return a cached PyJWKClient for the given publishable key."""
    if publishable_key not in _jwks_client_cache:
        jwks_url = get_jwks_url(publishable_key)
        logger.info(f"Initializing JWKS client for: {jwks_url}")
        _jwks_client_cache[publishable_key] = PyJWKClient(jwks_url)
    return _jwks_client_cache[publishable_key]


def verify_token(token: str, publishable_key: str) -> dict:
    """
    Verify a Clerk JWT and return its claims.
    Raises HTTPException(401) on any failure.
    """
    try:
        client = _get_jwks_client(publishable_key)
        signing_key = client.get_signing_key_from_jwt(token)
        claims = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            options={"verify_exp": True},
        )
        return claims
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")
    except Exception as e:
        logger.error(f"JWT verification error: {e}")
        raise HTTPException(status_code=401, detail="Could not verify credentials")


def make_auth_dependency(publishable_key: Optional[str]):
    """
    Returns a FastAPI dependency function.
    If publishable_key is None (not configured), always returns None
    so unauthenticated dev mode still works.
    """
    async def get_current_user_id(request: Request) -> Optional[str]:
        if not publishable_key:
            return None

        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing Authorization header")

        token = auth_header.removeprefix("Bearer ").strip()
        claims = verify_token(token, publishable_key)
        user_id = claims.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Token missing subject claim")
        return user_id

    return get_current_user_id