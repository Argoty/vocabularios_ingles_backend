from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import os

from db.models.usuarios import Usuario
from buscador import search_usuario

from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"],
    responses={404: {"message": "No encontrado"}}
)

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")


ALGORITHM = os.environ.get("ALGORITHM")
SECRET_KEY = os.environ.get("SECRET_KEY") # openssl rand -hex 32


crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def current_user(token: str = Depends(oauth2_schema)):
    exception = HTTPException(
        status_code=401,
        detail="Credenciales no validas",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        username = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get("sub")
        # Si ya se vencio el token manda igual exception
        if username is None:
            raise exception
    except JWTError:
        raise exception
    
    return search_usuario("username", username, con_password=False)


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    usuario_encontrado = search_usuario("username", form.username, con_password=False)

    if not type(usuario_encontrado) == Usuario:
        raise HTTPException(status_code=400, detail="El usuario no existe")
    
    usuarioDB = search_usuario("username", form.username, con_password=True)
    

    if not crypt.verify(form.password, usuarioDB.password):
        raise HTTPException(status_code=400, detail="La contraseña no es correcta")

    access_token = {
        "sub": usuarioDB.username,
        "exp": datetime.utcnow() + timedelta(minutes=2)
    }

    return {
        "access_token": jwt.encode(access_token, SECRET_KEY, algorithm=ALGORITHM),
        "token_type": "bearer"
    }


@router.get("/me", response_model=Usuario)
async def obtener_mi_usuario(usuario: Usuario = Depends(current_user)):
    return usuario




