from fastapi import APIRouter, HTTPException
from db.models.vocabulario import Palabra, Vocabulario
from db.client import db_client
from bson import ObjectId
from buscador import search_palabra, search_vocabulario

router = APIRouter(
    prefix="/palabras",
    tags=["palabras"],
    responses={404: {"message": "No encontrado"}})


@router.get("/{id}", response_model=Palabra)
async def obtener_palabra(id: str):
    try:
        palabra = search_palabra("_id", ObjectId(id))
    except:
        raise HTTPException(status_code=404, detail="La palabra no existe")
    
    if not type(palabra) == Palabra:
        raise HTTPException(status_code=404, detail="La palabra no existe")
    
    return palabra

@router.post("/", response_model=Palabra, status_code=201)
async def crear_palabra(palabra: Palabra):
    try:
        if not type(search_vocabulario("_id", ObjectId(palabra.id_vocabulario))) == Vocabulario:
            raise HTTPException(status_code=404, detail="El vocabulario no existe")
    except:
        raise HTTPException(status_code=404, detail="El vocabulario no existe")

    if type(search_palabra("palabra", palabra.palabra)) == Palabra:
        raise HTTPException(status_code=404, detail="La palabra ya existe")
    
    palabra_dict = dict(palabra)
    del palabra_dict["id"]

    id = db_client.palabras.insert_one(palabra_dict).inserted_id
    return search_palabra("_id", id)



@router.put("/", response_model=Palabra)
async def editar_palabra(palabra: Palabra):
    try:
        if not type(search_palabra("_id", ObjectId(palabra.id))) == Palabra:
            raise HTTPException(status_code=404, detail="La palabra que se intenta editar no existe")
    except:
        raise HTTPException(status_code=404, detail="La palabra que se intenta editar no existe")
    
    try:
        if not type(search_vocabulario("_id", ObjectId(palabra.id_vocabulario))) == Vocabulario:
            raise HTTPException(status_code=404, detail="El vocabulario no existe")
    except:
        raise HTTPException(status_code=404, detail="El vocabulario no existe")


    same_palabra = search_palabra("palabra", palabra.palabra)
    if type(same_palabra) == Palabra and same_palabra.id != palabra.id:
        raise HTTPException(status_code=404, detail="Esta palabra ya existe traducida") 

    palabra_dict = dict(palabra)
    del palabra_dict["id"]

    db_client.palabras.find_one_and_replace({ "_id": ObjectId(palabra.id)}, palabra_dict)  

    return search_palabra("_id", ObjectId(palabra.id))


@router.delete("/{id}", status_code=204)
async def eliminar_palabra(id: str):
    try: 
        palabra_eliminated = db_client.palabras.find_one_and_delete({"_id": ObjectId(id)}) 
    except:
        raise HTTPException(status_code=404, detail="La palabra no existe")

    if not palabra_eliminated:
        raise HTTPException(status_code=404, detail="La palabra no existe")




