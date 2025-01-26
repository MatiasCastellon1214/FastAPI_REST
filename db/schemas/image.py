def image_schema(image) -> dict:
    """
    Convierte un documento de imagen en un diccionario con claves estandarizadas.
    """
    return {
        "id": str(image["_id"]), # Convierte el ObjectId a string
        "image": image["image"] # URL o ruta de la imagen
    }

def images_schema(images) -> list:
    """
    Convierte una lista de documentos de imágenes en una lista de diccionarios.
    """
    return [image_schema(image) for image in images]

'''
def image_schema(image) -> dict:
    if "_id" not in image or "image" not in image:
        raise ValueError("El documento de imagen no contiene las claves requeridas ('_id', 'image')")
    return {
        "id": str(image["_id"]),
        "image": image["image"]
    }

'''