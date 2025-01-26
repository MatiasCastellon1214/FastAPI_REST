from fastapi import APIRouter, HTTPException, status, UploadFile, File
from db.model.image_product import ImageProduct
from db.client import db_client
from db.schemas.image_product import image_product_schema, image_products_schema
from bson import ObjectId
from utils.s3_utils import upload_image_product_to_aws, delete_image_product_from_aws

# pip install boto3 python-multipart

router = APIRouter(prefix="/image_productdb",
                        tags=["image_productdb"],
                        responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})


def image_search_product(field: str, key):
    try:
        image_product = db_client.image_products.find_one({field: key})
        print(image_product)
        return ImageProduct(**image_product_schema(image_product))
    except:
        return {"error": "Image of Product not found"}
    

# GET

@router.get("/", response_model= list[ImageProduct])
async def image_products():
    return image_products_schema(db_client.image_products.find())
    
# Llamada a la imagen de un producto por id - Path  
@router.get("/{id}")
async def image_product(id: str):
    return image_search_product("_id", ObjectId(id))
'''''
# Llamada a la imagen de un producto por id - Query
@router.get("/search")
async def image_product(id: str):
    return image_search_product("_id", ObjectId(id))
'''

# POST
@router.post("/", response_model= ImageProduct, status_code= status.HTTP_201_CREATED)
async def create_image_product(file: UploadFile = File(...)):
    
    if type(image_search_product("image_product", file.filename)) == ImageProduct:
        raise HTTPException(
        status.HTTP_404_NOT_FOUND, 
        detail="Image of Product already exists")
    
    # Subir la imagen a AWS S3
    s3_url = upload_image_product_to_aws(file.file, file.filename, file.content_type)

    image_product_dict = {"image_product": s3_url}

    if not isinstance(s3_url, str) and 'error' in s3_url:
        raise HTTPException(
        status.HTTP_500_INTERNAL_SERVER_ERROR, 
        detail=s3_url["error"])

    # Crear el objeto de la imagen del producto generada
    #image_product = ImageProduct(image=s3_url)

    
    # Insertar la imagen del producto en la base de datos
    id = db_client.image_products.insert_one(image_product_dict).inserted_id

    new_image_product = image_product_schema(db_client.image_products.find_one({"_id": id}))

    return ImageProduct(**new_image_product)

# PUT
@router.put("/{id}")
async def update_image_product(id: str, file: UploadFile = File(...)):
    image_product = image_search_product("_id", ObjectId(id))
    
    if type(image_product) != ImageProduct:
        raise HTTPException(
        status.HTTP_404_NOT_FOUND, 
        detail="Image of Product not found")
    
    # Eliminar la imagen del bucket S3
    currente_s3_url = image_product.image
    if currente_s3_url:
        try:
            delete_image_product_from_aws(currente_s3_url)
        except:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail="Error deleting image of Product from AWS")
    
    # Subir la nueva imagen a AWS S3
    try:
        s3_url = upload_image_product_to_aws(file.file, file.filename, file.content_type)
    except:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Error uploading image of Product to AWS")

    image_product_dict = {"image_product": s3_url}

    if not isinstance(s3_url, str) and 'error' in s3_url:
        raise HTTPException(
        status.HTTP_500_INTERNAL_SERVER_ERROR, 
        detail=s3_url["error"])
    
    # Actualizar la imagen del producto en la base de datos
    db_client.image_products.update_one({"_id": ObjectId(id)}, {"$set": image_product_dict})

    return ImageProduct(**image_product_schema(
        db_client.image_products.find_one({"_id": ObjectId(id)})))


  
# DELETE
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_image_product(id: str):

    try:
        object_id = ObjectId(id)
    except Exception as e:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, 
            detail="Invalid ID")
    
    # Buscar la imagen de producto en la base de datos
    found = db_client.image_products.find_one({"_id": object_id})
    
    if not found:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, 
            detail="Image of Product not found")

    # Eliminar la imagen de producto del bucket S3
    s3_url = found.get("image_product")
    if s3_url:
        try:
            delete_image_product_from_aws(s3_url)
        except:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail="Error deleting image of Product from AWS")

  
    # Eliminar la imagen de producto de la base de datos
    found = db_client.image_products.find_one_and_delete({"_id": object_id})
    
    return {"message": "Image of Product deleted successfully"}
    
