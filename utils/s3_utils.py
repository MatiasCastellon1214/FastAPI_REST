# Establecemos las variables de entorno para conectarnos con AWS S3 fastapi-bucket-product
# Luego de haber creado el bucket en AWS S3, se deben establecer las variables de entorno dentro de nuestro entorno (fastAPI) para poder conectarse a él.
# conda env config vars set AWS_ACCESS_KEY_ID="tu_access_key_id"
# conda env config vars set AWS_SECRET_ACCESS_KEY="tu_secret_access_key"
# Desactivar y volver a activar el entorno para que los cambios surtan efecto.


# Instalamos el SDK de AWS para Python (Boto3) con el siguiente comando:
# pip install boto3

import boto3
from botocore.exceptions import NoCredentialsError
import uuid

from fastapi import HTTPException

AWS_S3_BUCKET = "fastapi-bucket-images"
AWS_S3_BUCKET_PRODUCT = "fastapi-bucket-product"


# Upload image to AWS S3

def upload_image_to_aws(file, filename: str, content_type: str):
    # Configuramos el cliente de S3
    s3 = boto3.client('s3')
    try:
        unique_filename = f"{(uuid.uuid4())}_{filename}"
        
        # Obtener el Content-Type del archivo de forma correcta
        #content_type = file.content_type

        s3.upload_fileobj(
            file,  # Archivo para subir
            AWS_S3_BUCKET,  # Nombre del Bucket
            unique_filename,  # Nombre único del archivo en S3
            ExtraArgs={
                "ContentType": content_type  # Tipo de archivo
            })

        # Generar la URL del archivo subido
        url = f"https://{AWS_S3_BUCKET}.s3.amazonaws.com/{unique_filename}"

        return url
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="AWS credentials not available")  # Manejo de error si faltan las credenciales
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading image: {str(e)}")


def upload_image_product_to_aws(file, filename: str, content_type: str):
    # Configuramos el cliente de S3
    s3 = boto3.client('s3')
    try:
        unique_filename = f"{(uuid.uuid4())}_{filename}"
        
        # Obtener el Content-Type del archivo de forma correcta
        #content_type = file.content_type

        s3.upload_fileobj(
            file,  # Archivo para subir
            AWS_S3_BUCKET_PRODUCT,  # Nombre del Bucket
            unique_filename,  # Nombre único del archivo en S3
            ExtraArgs={
                "ContentType": content_type  # Tipo de archivo
            })

        # Generar la URL del archivo subido
        url = f"https://{AWS_S3_BUCKET_PRODUCT}.s3.amazonaws.com/{unique_filename}"

        return url
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="AWS credentials not available")  # Manejo de error si faltan las credenciales
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading product image: {str(e)}")




# Delete image from AWS S3

def delete_image_from_aws(s3_url: str):
    s3 = boto3.client('s3')

    # Verificar que la URL del objeto sea válida
    if not s3_url.startswith(f"https://{AWS_S3_BUCKET}.s3.amazonaws.com/"):
        raise HTTPException(status_code=400, detail="Invalid URL")

    # Parsear el bucket y la clave del objeto desde la URL de S3
    bucket_name = "fastapi-bucket-images"
    bucket_key = s3_url.replace(f"https://{bucket_name}.s3.amazonaws.com/", "")


    try:
        
        # Eliminara el objeto del bucket
        s3.delete_object(
            Bucket=AWS_S3_BUCKET,
            Key=bucket_key
        )
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="AWS credentials not available")  # Manejo de error si faltan las credenciales
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting image: {str(e)}")
    



def delete_image_product_from_aws(s3_url: str):
    s3 = boto3.client('s3')

    # Verificar que la URL del objeto sea válida
    if not s3_url.startswith(f"https://{AWS_S3_BUCKET_PRODUCT}.s3.amazonaws.com/"):
        raise HTTPException(status_code=400, detail="Invalid URL")

    # Parsear el bucket y la clave del objeto desde la URL de S3
    bucket_name = "fastapi-bucket-product"
    bucket_key = s3_url.replace(f"https://{bucket_name}.s3.amazonaws.com/", "")


    try:
        
        # Eliminara el objeto del bucket
        s3.delete_object(
            Bucket=AWS_S3_BUCKET_PRODUCT,
            Key=bucket_key
        )
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="AWS credentials not available")  # Manejo de error si faltan las credenciales
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting product image: {str(e)}")
    



'''
# Función genérica para subir archivos a S3
def upload_file_to_s3(file, filename: str, content_type: str, bucket: str) -> str:
    """
    Sube un archivo a un bucket de AWS S3 y retorna la URL del archivo subido.
    """
    s3 = boto3.client('s3')
    try:
        unique_filename = f"{uuid.uuid4()}_{filename}"

        s3.upload_fileobj(
            file,
            bucket,
            unique_filename,
            ExtraArgs={
                "ContentType": content_type
            }
        )

        # Generar la URL pública del archivo subido
        url = f"https://{bucket}.s3.amazonaws.com/{unique_filename}"
        return url

    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="AWS credentials not available")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")


# Funciones específicas para subir imágenes
def upload_image_to_aws(file, filename: str, content_type: str) -> str:
    """
    Sube una imagen al bucket de imágenes de AWS S3.
    """
    return upload_file_to_s3(file, filename, content_type, AWS_S3_BUCKET)


def upload_image_product_to_aws(file, filename: str, content_type: str) -> str:
    """
    Sube una imagen de producto al bucket de productos de AWS S3.
    """
    return upload_file_to_s3(file, filename, content_type, AWS_S3_BUCKET_PRODUCT)


# Función genérica para eliminar archivos de S3
def delete_file_from_s3(s3_url: str, bucket: str):
    """
    Elimina un archivo de un bucket de AWS S3 dado su URL.
    """
    s3 = boto3.client('s3')

    # Validar que la URL pertenece al bucket correcto
    if not s3_url.startswith(f"https://{bucket}.s3.amazonaws.com/"):
        raise HTTPException(status_code=400, detail="Invalid URL")

    # Obtener la clave del objeto a partir de la URL
    bucket_key = s3_url.replace(f"https://{bucket}.s3.amazonaws.com/", "")

    try:
        s3.delete_object(
            Bucket=bucket,
            Key=bucket_key
        )
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="AWS credentials not available")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting file: {str(e)}")


# Funciones específicas para eliminar imágenes
def delete_image_from_aws(s3_url: str):
    """
    Elimina una imagen del bucket de imágenes de AWS S3.
    """
    delete_file_from_s3(s3_url, AWS_S3_BUCKET)


def delete_image_product_from_aws(s3_url: str):
    """
    Elimina una imagen de producto del bucket de productos de AWS S3.
    """
    delete_file_from_s3(s3_url, AWS_S3_BUCKET_PRODUCT)
'''