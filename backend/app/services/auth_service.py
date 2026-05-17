import os
import requests
import jwt

from fastapi import HTTPException
from fastapi.security import HTTPBearer
from fastapi import Depends

security = HTTPBearer()

CLERK_JWKS_URL = os.getenv("CLERK_JWKS_URL")

def verify_token(token: str):
    """Verifies the JWT token using Clerk's JWKS endpoint.
    """

    try:

      

        signing_key = jwt.PyJWKClient(
            CLERK_JWKS_URL
        ).get_signing_key_from_jwt(token)

        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            options={"verify_aud": False}
        )
        print(payload)
        return payload
    except Exception as e:

        print("JWT ERROR:")
        print(str(e))

        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials"
        )
    
async def get_current_user(credentials = Depends(security)):
    """Dependency to get the current user from the JWT token.
    """

    token = credentials.credentials
    payload = verify_token(token)

    return payload