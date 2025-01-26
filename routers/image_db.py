from fastapi import APIRouter, HTTPException, status, UploadFile, File
from db.model.image import Image
from db.client import db_client
from db.schemas.image import image_schema, images_schema
from bson import ObjectId
from utils.s3_utils import upload_image_to_aws, delete_image_from_aws

# pip install boto3 python-multipart

router = APIRouter(prefix="/image_db",
                        tags=["image_db"],
                        responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})

def search_image(field: str, key):
    try:
        image = db_client.images.find_one({field: key})
        print(image)
        return Image(**image_schema(image))
    except:
        return {"error": "Image not found"}
    
# GET

@router.get("/", response_model= list[Image])
async def images():
    return images_schema(db_client.images.find())
   

# POST

@router.post("/", response_model= Image, status_code= status.HTTP_201_CREATED)
async def create_image(file: UploadFile = File(...)):
    
    if type(search_image("image", file.filename)) == Image:
        raise HTTPException(
        status.HTTP_404_NOT_FOUND, 
        detail="Image already exists")
    
    # Subir la imagen a AWS S3
    s3_url = upload_image_to_aws(file.file, file.filename, file.content_type)

    image_dict = {"image": s3_url}

    if not isinstance(s3_url, str) and 'error' in s3_url:
        raise HTTPException(
        status.HTTP_500_INTERNAL_SERVER_ERROR, 
        detail=s3_url["error"])


    
    # Insertar la imagen del producto en la base de datos
    id = db_client.images.insert_one(image_dict).inserted_id

    new_image = image_schema(db_client.images.find_one({"_id": id}))

    return Image(**new_image)


# PUT   
@router.put("/{id}", response_model= Image)
async def update_image(id: str, file: UploadFile = File(...)):
    
    image = search_image("_id", ObjectId(id))
    
    if type(image) != Image:
        raise HTTPException(
        status.HTTP_404_NOT_FOUND, 
        detail="Image not found")
    
    # Eliminar la imagen del bucket S3
    currente_s3_url = image.image
    if currente_s3_url:
        try:
            delete_image_from_aws(currente_s3_url)
        except:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail="Error deleting image from AWS")


    # Subir la imagen a AWS S3
    try:
        s3_url = upload_image_to_aws(file.file, file.filename, file.content_type)
    except:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Error uploading image to AWS")

    # Actualizar la imagen en la base de datos
    image_dict = {"image": s3_url}

    if not isinstance(s3_url, str) and 'error' in s3_url:
        raise HTTPException(
        status.HTTP_500_INTERNAL_SERVER_ERROR, 
        detail=s3_url["error"])

    db_client.images.update_one({"_id": ObjectId(id)}, {"$set": image_dict})
    
    # Retornar la imagen actualizada
    return Image(**image_schema(db_client.images.find_one({"_id": ObjectId(id)})))


# DELETE
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_image(id: str):

    try:
        object_id = ObjectId(id) 
    except Exception as e:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, 
            detail="Invalid ID")
    
    # Buscar la imagen en la base de datos
    found = db_client.images.find_one({"_id": object_id})
    
    if not found:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, 
            detail="Image not found")
    
    # Eliminar la imagen del bucket S3
    s3_url = found.get("image")
    if s3_url:
        try:
            delete_image_from_aws(s3_url)
        except:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail="Error deleting image from AWS")
    
    # Eliminar la imagen de la base de datos
    found = db_client.images.find_one_and_delete({"_id": object_id})

    return {"message": "Image deleted successfully"}