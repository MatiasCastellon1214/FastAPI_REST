from pydantic import BaseModel
from typing import Optional

class Image(BaseModel):
    id: Optional[str] = None
    image: str
    