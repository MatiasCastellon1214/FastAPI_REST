from pydantic import BaseModel
from typing import Optional, List
from .image_product import ImageProduct


class Product(BaseModel):
    id: Optional[str] = None
    name: str
    price: float
    stock: int
    category: str
    image: Optional[List[str]] = []