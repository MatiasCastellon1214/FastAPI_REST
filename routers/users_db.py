## User DB API ###
from fastapi import APIRouter, HTTPException, status
from db.model.user import User
from db.client import db_client
from db.schemas.user import user_schema, users_schema
from bson import ObjectId


router = APIRouter(prefix="/userdb",
                        tags=["userdb"],
                        responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})

 

# GET

@router.get("/", response_model= list[User])
async def users():
    return users_schema(db_client.users.find())

# Llamada a un usuario por id - Path
@router.get("/{id}")
async def user(id: str):
    return search_user("_id", ObjectId(id))
    
# Llamada a un usuario por id - Query
@router.get("/")
async def user(id: str):
    return search_user("_id", ObjectId(id))
    
    

# POST
@router.post("/", response_model= User, status_code= status.HTTP_201_CREATED)
async def create_user(user: User):
    if type(search_user("email", user.email)) == User:
        raise HTTPException(
        status.HTTP_404_NOT_FOUND, detail="User already exists")
 
    user_dict = user.model_dump()
    user_dict.pop("id", None)

    id = db_client.users.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.users.find_one({"_id": id}))

    return User(**new_user)


def search_user(field: str, key):
    try:
        user = db_client.users.find_one({field: key})
        print(user)
        return User(**user_schema(user))
    except:
        return {"error": "User not found"}
    


# PUT
@router.put("/")
async def user(user: User):

    user_dict = user.model_dump()
    user_dict.pop("id", None)

    try:
        
        db_client.users.find_one_and_replace(
            {"_id": ObjectId(user.id)}, user_dict)
    except:
        return {"error": "User not updated"}
        
  
    return search_user("_id", ObjectId(user.id))


# DELETE
@router.delete("/{id}")
async def user(id: str, status_code= status.HTTP_204_NO_CONTENT):

    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        return {"message": "User not deleted"}
    return {"error": "User deleted"}
