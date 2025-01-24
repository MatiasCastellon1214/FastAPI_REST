from pydantic import BaseModel
from typing import Optional


class Product(BaseModel):
    id: Optional[str] = None
    name: str
    price: float
    stock: int
    category: str