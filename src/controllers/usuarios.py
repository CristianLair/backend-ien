from db.db import db

coleccion_usuarios = db["usuarios"]

ROLES_VALIDOS = ["cliente", "admin"]


def cambiar_rol(user, nuevo_rol):
    if nuevo_rol not in ROLES_VALIDOS:
        return None, f"Rol inválido. Debe ser uno de: {ROLES_VALIDOS}"

    usuario = coleccion_usuarios.find_one({"user": user})
    if usuario is None:
        return None, "Usuario no encontrado"

    coleccion_usuarios.update_one(
        {"user": user},
        {"$set": {"rol": nuevo_rol}},
    )

    return {"user": user, "rol": nuevo_rol}, None


def obtener_perfil(user):
    usuario = coleccion_usuarios.find_one({"user": user}, {"_id": 0, "password": 0})
    if usuario is None:
        return None, "Usuario no encontrado"

    return usuario, None