from datetime import datetime, timedelta, timezone
from db.db import db
from bson import ObjectId
from bson.errors import InvalidId
 
coleccion_partidos = db["partidos"]
coleccion_predicciones = db["predicciones"]
coleccion_usuarios = db["usuarios"]
 
OFFSET_ARGENTINA = timedelta(hours=-3)
 
 
def _serializar(documento):
    documento["_id"] = str(documento["_id"])
    return documento
 
 
def _validar_goles(goles_local, goles_visitante):
    for nombre, valor in (("goles_local", goles_local), ("goles_visitante", goles_visitante)):
        if isinstance(valor, bool) or not isinstance(valor, int):
            return f"'{nombre}' debe ser un número entero"
        if valor < 0:
            return f"'{nombre}' no puede ser negativo"
 
    return None
 
 
def _parsear_fecha_partido(fecha_str):
    """Interpreta 'fecha_str' (formato '%Y-%m-%d %H:%M') como horario Argentina
    (UTC-3, fijo, sin horario de verano) y devuelve el datetime equivalente en UTC.
 
    Se asume que TODAS las fechas de partidos se cargan y se muestran en
    horario Argentina, independientemente de la sede real donde se juegue
    el partido (México, EE.UU. o Canadá en el caso del Mundial 2026).
    """
    if not fecha_str:
        return None
 
    try:
        fecha_naive = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M")
    except ValueError:
        return None
 
    fecha_argentina = fecha_naive.replace(tzinfo=timezone(OFFSET_ARGENTINA))
    return fecha_argentina.astimezone(timezone.utc)
 
 
def _resultado_partido(goles_local, goles_visitante):
    """Devuelve 'local', 'visitante' o 'empate' según el marcador."""
    if goles_local > goles_visitante:
        return "local"
    if goles_local < goles_visitante:
        return "visitante"
    return "empate"
 
 
def _calcular_puntos(prediccion, goles_local_real, goles_visitante_real):
    pred_local = prediccion["goles_local"]
    pred_visitante = prediccion["goles_visitante"]
 
    if pred_local == goles_local_real and pred_visitante == goles_visitante_real:
        return 3
 
    resultado_real = _resultado_partido(goles_local_real, goles_visitante_real)
    resultado_predicho = _resultado_partido(pred_local, pred_visitante)
 
    if resultado_real == resultado_predicho:
        return 1
 
    return 0
 
 
def _procesar_predicciones(partido_id, goles_local, goles_visitante):
    predicciones = coleccion_predicciones.find({
        "partido_id": partido_id,
        "procesado": False,
    })
 
    for prediccion in predicciones:
        puntos = _calcular_puntos(prediccion, goles_local, goles_visitante)
 
        coleccion_predicciones.update_one(
            {"_id": prediccion["_id"]},
            {"$set": {"puntos_obtenidos": puntos, "procesado": True}},
        )
 
        coleccion_usuarios.update_one(
            {"user": prediccion["user"]},
            {"$inc": {"puntos": puntos}},
        )
 
 
def _revertir_predicciones(partido_id):
    predicciones = coleccion_predicciones.find({
        "partido_id": partido_id,
        "procesado": True,
    })
 
    for prediccion in predicciones:
        puntos_previos = prediccion.get("puntos_obtenidos") or 0
 
        coleccion_usuarios.update_one(
            {"user": prediccion["user"]},
            {"$inc": {"puntos": -puntos_previos}},
        )
 
        coleccion_predicciones.update_one(
            {"_id": prediccion["_id"]},
            {"$set": {"puntos_obtenidos": None, "procesado": False}},
        )
 
 
def crear_partido(equipo_local, equipo_visitante, fecha, grupo=None):
    """Crea un partido nuevo.
 
    'fecha' debe ser un string '%Y-%m-%d %H:%M' en horario Argentina (UTC-3).
    Se guarda tal cual (sin convertir), y _parsear_fecha_partido es quien
    la interpreta como Argentina al validar predicciones.
    """
    if equipo_local == equipo_visitante:
        return None, "Los dos equipos deben ser distintos"
 
    nuevo_partido = {
        "equipo_local": equipo_local,
        "equipo_visitante": equipo_visitante,
        "goles_local": None,
        "goles_visitante": None,
        "fecha": fecha,
        "grupo": grupo,
        "finalizado": False,
    }
 
    resultado = coleccion_partidos.insert_one(nuevo_partido)
    nuevo_partido["_id"] = str(resultado.inserted_id)
    return nuevo_partido, None
 
 
def obtener_partidos():
    partidos = list(coleccion_partidos.find())
    if not partidos:
        return None, "No hay partidos cargados"
 
    return [_serializar(p) for p in partidos], None
 
 
def obtener_partido(partido_id):
    try:
        oid = ObjectId(partido_id)
    except InvalidId:
        return None, "ID de partido inválido"
 
    partido = coleccion_partidos.find_one({"_id": oid})
    if partido is None:
        return None, "Partido no encontrado"
 
    return _serializar(partido), None
 
 
def cargar_resultado(partido_id, goles_local, goles_visitante):
    error_validacion = _validar_goles(goles_local, goles_visitante)
    if error_validacion:
        return None, error_validacion
 
    try:
        oid = ObjectId(partido_id)
    except InvalidId:
        return None, "ID de partido inválido"
 
    partido = coleccion_partidos.find_one({"_id": oid})
    if partido is None:
        return None, "Partido no encontrado"
 
    es_correccion = partido.get("finalizado", False)
 
    if es_correccion:
        _revertir_predicciones(str(oid))
 
    coleccion_partidos.update_one(
        {"_id": oid},
        {"$set": {
            "goles_local": goles_local,
            "goles_visitante": goles_visitante,
            "finalizado": True,
        }},
    )
 
    _procesar_predicciones(str(oid), goles_local, goles_visitante)
 
    partido_actualizado = coleccion_partidos.find_one({"_id": oid})
    return _serializar(partido_actualizado), None
 
 
def cargar_resultado_por_equipos(equipo1, equipo2, goles_equipo1, goles_equipo2):
    filtro = {
        "$or": [
            {"equipo_local": equipo1, "equipo_visitante": equipo2},
            {"equipo_local": equipo2, "equipo_visitante": equipo1},
        ],
    }
 
    coincidencias = list(coleccion_partidos.find(filtro))
 
    if not coincidencias:
        return None, f"No se encontró un partido entre '{equipo1}' y '{equipo2}'"
 
    if len(coincidencias) > 1:
        return None, (
            f"Se encontró más de un partido entre '{equipo1}' y '{equipo2}'. "
            "Cargá el resultado usando el partido_id específico."
        )
 
    partido = coincidencias[0]
 
 
    if partido["equipo_local"] == equipo1:
        goles_local, goles_visitante = goles_equipo1, goles_equipo2
    else:
        goles_local, goles_visitante = goles_equipo2, goles_equipo1
 
    return cargar_resultado(str(partido["_id"]), goles_local, goles_visitante)
 
 
def predecir_partido(user, partido_id, goles_local, goles_visitante):
    error_validacion = _validar_goles(goles_local, goles_visitante)
    if error_validacion:
        return None, error_validacion
 
    try:
        oid_partido = ObjectId(partido_id)
    except InvalidId:
        return None, "ID de partido inválido"
 
    partido = coleccion_partidos.find_one({"_id": oid_partido})
    if partido is None:
        return None, "Partido no encontrado"
 
    if partido.get("finalizado"):
        return None, "El partido ya finalizó, no se puede predecir"
 
    fecha_partido_utc = _parsear_fecha_partido(partido.get("fecha"))
    if fecha_partido_utc is not None:
        ahora_utc = datetime.now(timezone.utc)
        if ahora_utc >= fecha_partido_utc:
            return None, "El partido ya comenzó, no se puede predecir"
 
    filtro = {"user": user, "partido_id": partido_id}
    valores = {
        "user": user,
        "partido_id": partido_id,
        "goles_local": goles_local,
        "goles_visitante": goles_visitante,
        "puntos_obtenidos": None,
        "procesado": False,
    }
 
    coleccion_predicciones.update_one(filtro, {"$set": valores}, upsert=True)
 
    prediccion = coleccion_predicciones.find_one(filtro)
    return _serializar(prediccion), None
 
 
def obtener_predicciones_usuario(user):
    predicciones = list(coleccion_predicciones.find({"user": user}))
    if not predicciones:
        return None, "El usuario no tiene predicciones cargadas"
 
    return [_serializar(p) for p in predicciones], None
 
 
def obtener_prediccion(user, partido_id):
    prediccion = coleccion_predicciones.find_one({"user": user, "partido_id": partido_id})
    if prediccion is None:
        return None, "No existe una predicción de este usuario para este partido"
 
    return _serializar(prediccion), Non