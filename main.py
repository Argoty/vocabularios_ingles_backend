from fastapi import FastAPI, HTTPException

from db.models.vocabulario import Vocabulario, Palabra
# from db.models.usuarios import Usuario

from db.schemas.vocabulario import vocabularios_schema
from db.client import db_client

from buscador import search_vocabulario, search_palabras_por_vocabulario
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv



load_dotenv()


from routers import palabras, usuarios

app = FastAPI()

app.include_router(palabras.router)
app.include_router(usuarios.router)

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def api_vocabulario():
    return { "API VOCABULARIO": "Esta api contiene distintos vocabularios de ingles para aprender y poder ser usada para practicar el idioma"}

@app.get("/vocabularios/info", response_model=list[Vocabulario])
async def obtener_vocabularios():
    return vocabularios_schema(db_client.vocabularios.find())

@app.get("/vocabularios/info/{id}", response_model=Vocabulario)
async def obtener_vocabulario(id: str):
    try:
        vocabulario = search_vocabulario("_id", ObjectId(id))
    except:
        raise HTTPException(status_code=404, detail="El vocabulario no existe")
    
    if not type(vocabulario) == Vocabulario:
        raise HTTPException(status_code=404, detail="El vocabulario no existe")
    
    return vocabulario

@app.get("/vocabularios/{id}", response_model=list[Palabra])
async def obtener_palabras_de_vocabulario(id):
    vocabulario_palabras = search_palabras_por_vocabulario(id)

    if len(vocabulario_palabras) <= 0:
        raise HTTPException(status_code=404, detail="El vocabulario no existe o aun no hay palabras en este")

    return vocabulario_palabras


@app.post("/vocabularios", status_code=201, response_model=Vocabulario)
async def crear_vocabulario(vocab: Vocabulario): # usuario: Usuario = Depends(usuarios.current_user)
    if type(search_vocabulario("numero", vocab.numero)) == Vocabulario:
        raise HTTPException(status_code=404, detail="El vocabulario ya existe")
    
    vocab_dict = dict(vocab)
    del vocab_dict["id"]

    id = db_client.vocabularios.insert_one(vocab_dict).inserted_id

    return search_vocabulario("_id", id)



@app.put("/vocabularios", response_model=Vocabulario)
async def editar_vocabulario(vocab: Vocabulario):
    try:
        if not type(search_vocabulario("_id", ObjectId(vocab.id))) == Vocabulario:
            raise HTTPException(status_code=404, detail="El vocabulario no existe")
    except:
        raise HTTPException(status_code=404, detail="El vocabulario no existe")
    
    same_number = search_vocabulario("numero", vocab.numero)

    if type(same_number) == Vocabulario and same_number.id != vocab.id:
        raise HTTPException(status_code=404, detail="El numero de serie de este vocabulario ya existe") 

    vocab_dict = dict(vocab)
    del vocab_dict["id"]

    db_client.vocabularios.find_one_and_replace({ "_id": ObjectId(vocab.id)}, vocab_dict)  

    return search_vocabulario("_id", ObjectId(vocab.id))



@app.delete("/vocabularios/{id}", status_code=204)
async def eliminar_vocabulario(id: str):
    try: 
        vocab_eliminated = db_client.vocabularios.find_one_and_delete({"_id": ObjectId(id)}) 
    except:
        raise HTTPException(status_code=404, detail="El usuario no existe")

    if not vocab_eliminated:
        raise HTTPException(status_code=404, detail="El usuario no existe")

    
    db_client.palabras.delete_many({"id_vocabulario": id})


        

# correr server local: uvicorn main:app --reload