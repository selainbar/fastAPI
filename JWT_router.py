import jwt
from datetime import datetime, timedelta
from fastapi import APIRouter, Response, HTTPException, Cookie
from fastapi.security import OAuth2PasswordBearer

# Secret key should be stored securely (e.g., in environment variables)
SECRET_KEY = "abracadabra"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/JWT/generate")

router = APIRouter(
    prefix="/JWT",
    tags=["Authentication"],
    responses={404: {"description": "Not found"}},
)
@router.post("/generate")
async def generate_token(username: str, password: str, response: Response):
    expiration = datetime.now() + timedelta(minutes=30)
    payload = {
        "user": username,
        "password": password,
        "exp": expiration
    }
    
    # Generate the JWT token
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    
    # Set the token as an HttpOnly cookie
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=1800,  # 30 minutes in seconds
        expires=expiration.strftime("%a, %d %b %Y %H:%M:%S GMT"),
        samesite="lax",
        secure=False,  # Set to True in production with HTTPS
    )
    
    return {"message": "Login successful"}
    
@router.get("/verify")
async def verify_token(access_token: str = Cookie(None)):
    if not access_token:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )
    
    try:
        # Decode and verify the token
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("user")
        
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        return {"username": username, "authenticated": True}
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except (jwt.JWTError, Exception):
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(access_token: str = Cookie(None)):
    if access_token is None:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )
    
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("user")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except (jwt.JWTError, Exception):
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Logout successful"}
