from db.schemas.image_product import image_products_schema


def product_schema(product) -> dict:
    # Obtener las imágenes si existen
    images = []

    if product.get("image", []):
        if "image" in product and isinstance(product["image"], list):
            image_ids = product["image"]
            # Convertir ObjectId a string para cada imagen
            images = [str(img_id) if isinstance(img_id, object) else img_id for img_id in image_ids]
    

    return {"id": str(product["_id"]),
            "name": product["name"],
            "price": product["price"],
            "stock": product["stock"],
            "category": product["category"],
            "image": images 
            }

def products_schema(products) -> list:
    return [product_schema(product) for product in products]


