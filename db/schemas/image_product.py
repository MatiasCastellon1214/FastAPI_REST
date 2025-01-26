def image_product_schema(image_product) -> dict:
    """
    Convierte un documento de imagen de producto en un diccionario con claves estandarizadas.
    """
    return {
        "id": str(image_product["_id"]),
        "image": image_product["image_product"],
        "product_id": str(image_product["product_id"])
    }

def image_products_schema(image_products) -> list:
    """
    Convierte una lista de documentos de imágenes de productos en una lista de diccionarios.
    """
    return [image_product_schema(image_product) for image_product in image_products]