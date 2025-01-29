from bson import ObjectId

def image_product_schema(image_product) -> dict:
    if isinstance(image_product, ObjectId):
        # Si recibimos un ObjectId, solo devolvemos un string
        return str(image_product)
    
    """
    Convierte un documento de imagen de producto en un diccionario con claves estandarizadas.
    """
    return {
        "id": str(image_product["_id"]),
        "image_product": image_product["image_product"],
        "product_id": str(image_product["product_id"] if "product_id" in image_product else "") 
    }

def image_products_schema(image_products) -> list:

    if not image_products:
        return []

    """
    Convierte una lista de documentos de imágenes de productos en una lista de diccionarios.
    """
    # Si es una lusta de ObjectId, convertirlas directamente
    if isinstance(image_products, ObjectId):
        return [str(image_product) for image_product in image_products]

    return [image_product_schema(image_product) for image_product in image_products]