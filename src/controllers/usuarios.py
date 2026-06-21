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
def ranking_global(top=10):
    try:
        usuarios = list(
            coleccion_usuarios.find(
                {},
                {
                    "_id": 1,
                    "user": 1,
                    "puntos": 1
                }
            )
        )

        ranking = [
            {
                "_id": str(usuario["_id"]),
                "user": usuario.get("user", ""),
                "puntos": usuario.get("puntos", 0)
            }
            for usuario in usuarios
        ]

        ranking.sort(
            key=lambda x: x["puntos"],
            reverse=True
        )

        return ranking[:top], None

    except Exception as e:
        return None, str(e)

def obtener_perfil(user):
    usuario = coleccion_usuarios.find_one({"user": user}, {"_id": 0, "password": 0})
    if usuario is None:
        return None, "Usuario no encontrado"

    return usuario, None