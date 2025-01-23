from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# Iniciar el server: uvicorn users:app --reload

# Entidad User

class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int 

users_list = [User(id= 1,name= "Jaimito", surname= "3.14jota", url="www.jaimito.com", age= 25),
            User(id= 2,name= "Pepito", surname= "dev", url="www.pepitodev.com", age= 225),
            User(id= 3,name= "Cuis", surname= "Maceiro", url="www.cuis.com", age= 42)]



# GET
@router.get("/usersjson")
async def usersjson():
    return [{"name": "Jaimito", "surname": "3.14jota", "url":"www.jaimito.com", "age": 25}, 
            {"name": "Pepito", "surname": "dev", "url":"www.pepitodev.com", "age": 225},
            {"name": "Cuis", "surname": "Maceiro", "url":"www.cuis.com", "age": 42}]

@router.get("/users")
async def users():
    return users_list

# Llamada a un usuario por id - Path
@router.get("/user/{id}")
async def user(id: int):
    return search_user(id)
    
# Llamada a un usuario por id - Query
@router.get("/userquery/")
async def user(id: int):
    return search_user(id)
    
    

# POST
@router.post("/user/", response_model= User, status_code= 201)
async def create_user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=400, detail="User already exists")
 
    users_list.append(user)
    return user


def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "User not found"}
    


# PUT
@router.put("/user/")
async def user(user: User):
    
    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    
    if not found:
        return {"error": "User not updated"}
  
    return user


# DELETE
@router.delete("/user/{id}")
async def user(id: int):

    found = False

    for index, user in enumerate(users_list):
        if user.id == id:
            del users_list[index]
            found = True
            return {"message": "User deleted"}
    return {"error": "User not deleted"}
