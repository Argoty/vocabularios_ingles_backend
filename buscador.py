from db.models.vocabulario import Vocabulario, Palabra
from db.models.usuarios import Usuario, UsuarioDB
from db.schemas.vocabulario import vocabulario_schema, palabra_schema, palabras_vocabulario_schema
from db.schemas.usuarios import usuario_schema
from db.client import db_client

def search_vocabulario(field: str, key):
    try:
        vocabulario_json = db_client.vocabularios.find_one({ field: key })
        return Vocabulario(**vocabulario_schema(vocabulario_json))
    except:
        return {"error": "Vocabulario no encontrado"}

def search_palabras_por_vocabulario(id_vocabulario):
    try:
        vocabulario_json = db_client.palabras.find({ "id_vocabulario": id_vocabulario })
        return palabras_vocabulario_schema(vocabulario_json)
    except:
        return {"error": "Vocabulario no encontrado"}
    

def search_palabra(field: str, key):
    try:
        palabra_json = db_client.palabras.find_one({ field: key })
        return Palabra(**palabra_schema(palabra_json))
    except:
        return {"error": "Palabra no encontrada"}

def search_usuario(field: str, key, con_password: bool):
    try:
        usuario_json = db_client.usuarios.find_one({ field: key })

        if con_password:
            return UsuarioDB(**usuario_schema(usuario_json))
        else:
            usuario_con_schema = usuario_schema(usuario_json)
            del usuario_con_schema["password"]
            return Usuario(**usuario_con_schema)
    except:
        return {"error": "Usuario no encontrado"}