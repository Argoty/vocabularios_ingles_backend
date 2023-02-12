from pydantic import BaseModel
from typing import Optional

class Vocabulario(BaseModel):
    id: Optional[str]
    nombre: str
    numero: float

class Palabra(BaseModel):
    id: Optional[str]
    id_vocabulario: str
    palabra: str
    traduccion: str