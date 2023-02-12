from pydantic import BaseModel
from typing import Optional

class Usuario(BaseModel):
    id: Optional[str]
    username: str
    email: str

class UsuarioDB(Usuario):
    password: str