from db.db import db  

coleccion = db["paises"]

def obtener_paises():
    documento = coleccion.find_one({}, {"_id": 0}) 

    if documento:
        return documento, None

    return None, "No hay datos"