def vocabulario_schema(vocabulario) -> dict:
    return {
        "id": str(vocabulario["_id"]),
        "nombre": vocabulario["nombre"],
        "numero": vocabulario["numero"],
    }

def vocabularios_schema(vocabularios) -> list:
    return [vocabulario_schema(vocabulario) for vocabulario in vocabularios]


def palabra_schema(palabra) -> dict:
    return {
        "id": str(palabra["_id"]),
        "id_vocabulario": palabra["id_vocabulario"],
        "palabra": palabra["palabra"],
        "traduccion": palabra["traduccion"]
    }

def palabras_vocabulario_schema(palabras) -> list:
    return [palabra_schema(palabra) for palabra in palabras]