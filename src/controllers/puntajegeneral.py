from db.db import db  

coleccion = db["paises"]

def obtener_paises():
    documento = coleccion.find_one({}, {"_id": 0}) 

    if documento:
        return documento, None

    return None, "No hay datos"
def actualizar_puntos_paises(pais1, puntos1, pais2, puntos2):
    documento = coleccion.find_one({}, {"_id": 0})

    if documento is None:
        return None, "No hay datos"

    paises = documento.get("paises", {})

    paises_invalidos = [p for p in (pais1, pais2) if p not in paises]
    if paises_invalidos:
        return None, f"Países no encontrados: {paises_invalidos}"

    if pais1 == pais2:
        return None, "Los dos países del partido deben ser distintos"

    nuevo_puntaje_pais1 = paises[pais1] + puntos1
    nuevo_puntaje_pais2 = paises[pais2] + puntos2

    set_fields = {
        f"paises.{pais1}": nuevo_puntaje_pais1,
        f"paises.{pais2}": nuevo_puntaje_pais2,
    }
    coleccion.update_one({}, {"$set": set_fields})

    paises_actualizados = {
        **paises,
        pais1: nuevo_puntaje_pais1,
        pais2: nuevo_puntaje_pais2,
    }
    return {"paises": paises_actualizados}, None