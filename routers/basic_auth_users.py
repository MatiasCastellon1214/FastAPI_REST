from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter(prefix="/basicauth",
                        tags=["basicauth"],
                        responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

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
        "password": "123456"
    },
    "Jaimitox2": {
        "username": "Jaimitox2",
        "full_name": "Jaimito García2",
        "email": "jaimitogarcia2@gmail.com",
        "disabled": True,
        "password": "654321"
    },
}     


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

# Criterio de dependencia
async def current_user(token: str = Depends(oauth2_scheme)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid token", 
            headers= {"WWW-Authenticate": "Bearer"})
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
    if not form_data.password == user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Incorrect password")
    return {"access_token": user.username, "token_type": "bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user