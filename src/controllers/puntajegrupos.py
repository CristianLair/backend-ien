from db.db import db

coleccion_grupos = db["grupos"]


def _obtener_documento():
    documento = coleccion_grupos.find_one()
    if documento is None:
        return None
    documento.pop("_id", None)
    return documento


def _ordenar_tabla(paises_dict):
    return [
        {"pais": pais, "puntos": pts}
        for pais, pts in sorted(
            paises_dict.items(), key=lambda x: x[1], reverse=True
        )
    ]


def obtener_todos_los_grupos():
    documento = _obtener_documento()
    if documento is None:
        return None, "No se encontraron grupos cargados"

    tabla = {
        nombre_grupo: _ordenar_tabla(paises)
        for nombre_grupo, paises in documento.items()
    }
    return tabla, None


def obtener_grupo(nombre_grupo):
    documento = _obtener_documento()
    if documento is None:
        return None, "No se encontraron grupos cargados"

    if nombre_grupo not in documento:
        return None, f"Grupo '{nombre_grupo}' no encontrado"

    tabla = _ordenar_tabla(documento[nombre_grupo])
    return tabla, None


def actualizar_puntos_grupo(nombre_grupo, pais1, puntos1, pais2, puntos2):
    documento = _obtener_documento()
    if documento is None:
        return None, "No se encontraron grupos cargados"

    if nombre_grupo not in documento:
        return None, f"Grupo '{nombre_grupo}' no encontrado"

    paises_grupo = documento[nombre_grupo]

    paises_invalidos = [p for p in (pais1, pais2) if p not in paises_grupo]
    if paises_invalidos:
        return None, f"Países no pertenecen a {nombre_grupo}: {paises_invalidos}"

    if pais1 == pais2:
        return None, "Los dos países del partido deben ser distintos"

    nuevo_puntaje_pais1 = paises_grupo[pais1] + puntos1
    nuevo_puntaje_pais2 = paises_grupo[pais2] + puntos2

    set_fields = {
        f"{nombre_grupo}.{pais1}": nuevo_puntaje_pais1,
        f"{nombre_grupo}.{pais2}": nuevo_puntaje_pais2,
    }
    coleccion_grupos.update_one({}, {"$set": set_fields})

    paises_actualizados = {
        **paises_grupo,
        pais1: nuevo_puntaje_pais1,
        pais2: nuevo_puntaje_pais2,
    }
    tabla = _ordenar_tabla(paises_actualizados)
    return tabla, None


def actualizar_puntos_pais(nombre_grupo, pais, puntos):
    documento = _obtener_documento()
    if documento is None:
        return None, "No se encontraron grupos cargados"

    if nombre_grupo not in documento:
        return None, f"Grupo '{nombre_grupo}' no encontrado"

    if pais not in documento[nombre_grupo]:
        return None, f"'{pais}' no pertenece al {nombre_grupo}"

    coleccion_grupos.update_one({}, {"$set": {f"{nombre_grupo}.{pais}": puntos}})

    paises_actualizados = {**documento[nombre_grupo], pais: puntos}
    tabla = _ordenar_tabla(paises_actualizados)
    return tabla, None


def resetear_puntos():
    documento = _obtener_documento()
    if documento is None:
        return False, "No se encontraron grupos cargados"

    set_fields = {
        f"{nombre_grupo}.{pais}": 0
        for nombre_grupo, paises in documento.items()
        for pais in paises
    }
    coleccion_grupos.update_one({}, {"$set": set_fields})
    return True, None


def ranking_global_equipos(top=10):
    documento = _obtener_documento()
    if documento is None:
        return None, "No se encontraron grupos cargados"

    todos = [
        {"pais": pais, "grupo": nombre_grupo, "puntos": pts}
        for nombre_grupo, paises in documento.items()
        for pais, pts in paises.items()
    ]
    todos.sort(key=lambda x: x["puntos"], reverse=True)
    return todos[:top], None