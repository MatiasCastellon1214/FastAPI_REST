## Product DB API ###
from fastapi import APIRouter, HTTPException, status
from db.model.product import Product
from db.client import db_client
from db.schemas.product import product_schema, products_schema
from bson import ObjectId


router = APIRouter(prefix="/productdb",
                        tags=["productdb"],
                        responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})


def search_product(field: str, key):
    try:
        product = db_client.products.find_one({field: key})
        print(product)
        return Product(**product_schema(product))
    except:
        return {"error": "Product not found"}
    


# GET

@router.get("/", response_model= list[Product])
async def products():
    return products_schema(db_client.products.find())

# Llamada a un producto por id - Path
@router.get("/{id}")
async def product(id: str):
    return search_product("_id", ObjectId(id))

# Llamada a un producto por id - Query
@router.get("/search")
async def product(id: str):
    return search_product("_id", ObjectId(id))



# POST
@router.post("/", response_model= Product, status_code= status.HTTP_201_CREATED)
async def create_product(product: Product):
    if type(search_product("name", product.name)) == Product:
        raise HTTPException(
        status.HTTP_404_NOT_FOUND, detail="Product already exists")
 
    product_dict = product.model_dump()
    product_dict.pop("id", None)

    id = db_client.products.insert_one(product_dict).inserted_id

    new_product = product_schema(db_client.products.find_one({"_id": id}))

    return Product(**new_product)


# PUT   
@router.put("/")
async def update_product(product: Product):
    
    product_dict = product.model_dump()
    product_dict.pop("id", None)

    try:
        db_client.products.find_one_and_replace({"_id": ObjectId(product.id)}, product_dict)

    except:
        return {"error": "Product not updated"}

    return search_product("_id", ObjectId(product.id))


# DELETE    
@router.delete("/{id}")
async def delete_product(id: str, status_code= status.HTTP_204_NO_CONTENT):

    found = db_client.products.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND, 
            detail="Product not deleted")
    return {"message": "Product deleted"}


    