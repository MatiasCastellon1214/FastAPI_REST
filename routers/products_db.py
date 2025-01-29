## Product DB API ###
from fastapi import APIRouter, HTTPException, status
from db.model.product import Product
from db.client import db_client
from db.schemas.product import product_schema, products_schema
from bson import ObjectId

from utils.s3_utils import delete_image_product_from_aws



router = APIRouter(prefix="/productdb",
                        tags=["productdb"],
                        responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})


def search_product(field: str, key):
    try:
        product = db_client.products.find_one({field: key})
        print(product)
        return Product(**product_schema(product)) if product else None
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
        status.HTTP_404_NOT_FOUND, 
        detail="Product already exists")
 
    product_dict = product.model_dump()
    product_dict.pop("id", None)
    product_dict["images"] = []


    # Insertar el producto en la base de datos
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
@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
async def delete_product(id: str):

    try:
        try: 
            product_id = ObjectId(id)
        except:
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST, 
                detail="Invalid ID")
        # Buscar el producto en la base de datos antes de eliminarlo
        found = db_client.products.find_one({"_id": product_id})
        if not found:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND, 
                detail="Product not deleted")

        # Eliminar el producto de la base de datos
        if "image" in found and found["image"]:
            for image_id in found["image"]:
                # Buscar cada imagen del producto
                image = db_client.image_products.find_one({"_id": image_id})
                if image:
                    # Eliminar cada imagen del bucket S3
                    delete_image_product_from_aws(image["image_product"])
                    # Eliminar cada imagen de la base de datos
                    db_client.image_products.delete_one({"_id": image_id})

        # Finalmente, eliminar el producto
        db_client.products.delete_one({"_id": ObjectId(id)})
        
        return {"message": "Product and associated images deleted successfully"}
    
    except Exception as e:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, 
            detail=str(e))





    