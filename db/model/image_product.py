from pydantic import BaseModel
from typing import Optional

class ImageProduct(BaseModel):
    id: Optional[str] = None
    image: str
    