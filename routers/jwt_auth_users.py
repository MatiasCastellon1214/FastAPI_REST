# Instalamos PyJWT para generar y verificar los tokens JWT en Python
# pip install pyjwt
# En este caso utilizamos: pip install "python-jose[cryptography]"

# PassLib es un gran paquete de Python para manejar hashes de contraseñas
# pip install "passlib[bcrypt]"

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone


# to get a string like this run:
# openssl rand -hex 32
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1
SECRET_KEY = "b9b96d42688bf4ec58f6be4b5eb320bdd0ef369689d206c3f60aeba8cbd2f198"

router = APIRouter(prefix="/jwtauth",
                        tags=["jwtauth"],
                        responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Contexto de encriptación
crypt = CryptContext(schemes=["bcrypt"])


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str
    

users_db = {
    "Jaimitox": {
        "username": "Jaimitox",
        "full_name": "Jaimito García",
        "email": "jaimitogarcia@gmail.com",
        "disabled": False,
        "password": "$2a$12$LECx2huV5CXrZm4HWZl/4uKLhN.tPJpCP5gdw1jSTniWFdgx5y7cS"
    },
    "Jaimitox2": {
        "username": "Jaimitox2",
        "full_name": "Jaimito García2",
        "email": "jaimitogarcia2@gmail.com",
        "disabled": True,
        "password": "$2a$12$Z6KUtbqER/4E6k4.UE5S4.RbkZ94DxN1BfUPXBFwLsNWceS5eOcey"
    },
}  


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

async def auth_user(token: str = Depends(oauth2_scheme)):

    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Invalid token", 
        headers= {"WWW-Authenticate": "Bearer"})

    try:
        username = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception
        
    except JWTError:
        raise exception
    
    return search_user(username)


# Criterio de dependencia
async def current_user(user: User = Depends(auth_user)):
    
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Inactive user")
    return user

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form_data.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Incorrect username")
    
    user = search_user_db(form_data.username)

    if not crypt.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Incorrect password")
    
    access_token_expiration = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    expire = datetime.now(timezone.utc) + access_token_expiration

    access_token = {"sub": user.username, "exp": expire}

    return {"access_token": jwt.encode(access_token, SECRET_KEY, algorithm= ALGORITHM), "token_type": "bearer"}


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user