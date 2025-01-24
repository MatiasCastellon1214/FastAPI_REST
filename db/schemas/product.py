def product_schema(product) -> dict:
    return {"id": str(product["_id"]),
            "name": product["name"],
            "price": product["price"],
            "stock": product["stock"],
            "category": product["category"]}

def products_schema(products) -> list:
    return [product_schema(product) for product in products]


