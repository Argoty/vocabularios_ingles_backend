def usuario_schema(usuario) -> dict:
    return {
        "id": str(usuario["_id"]),
        "username": usuario["username"],
        "email": usuario["email"],
        "password": usuario["password"]
    }
