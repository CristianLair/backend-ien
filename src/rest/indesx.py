from flask import Flask ,jsonify, request
from flask_cors import CORS
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from db.db import db
from controllers.puntajegeneral import obtener_paises, actualizar_puntos_paises
from controllers.partidos import (
    crear_partido,
    obtener_partidos,
    obtener_partido,
    cargar_resultado,
    predecir_partido,
    obtener_predicciones_usuario,
    obtener_prediccion,
    cargar_resultado_por_equipos
)
from utils.middleweare import token_required, admin_required
from controllers.usuarios import cambiar_rol, obtener_perfil
from auth.registro import register
from auth.login import login
from auth.recuperarContraseña import reset_password
from controllers.puntajegrupos import (
    obtener_todos_los_grupos,
    obtener_grupo,
    actualizar_puntos_grupo,
    actualizar_puntos_pais,
    resetear_puntos,
    ranking_global,
)

app = Flask(__name__)
CORS(app)
@app.route("/")
def home():
    return {"mensaje": "Servidor funcionando ✅"}
@app.route("/ping")
def ping():
    return {"status": "alive"}, 200
@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    user = data.get('user')
    password = data.get('password')

    try:
        token = login(user, password)
        return jsonify({'success': True, 'message': 'login realizado con exito', 'token': token}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
@app.route("/paises", methods=["GET"])
@token_required
def ranking():
    tabla, error = obtener_paises()

    if error:
        return jsonify({"error": error}), 404

    return jsonify(tabla), 200
@app.route("/paises/puntos", methods=["PUT"])
@token_required
@admin_required
def actualizar_puntos_paises_route():
    data = request.get_json()
    if not data:
        return jsonify({"error": "El cuerpo no puede estar vacío"}), 400

    campos_requeridos = ["pais1", "puntos1", "pais2", "puntos2"]
    faltantes = [c for c in campos_requeridos if c not in data]
    if faltantes:
        return jsonify({"error": f"Faltan los campos: {faltantes}"}), 400

    tabla, error = actualizar_puntos_paises(
        data["pais1"],
        data["puntos1"],
        data["pais2"],
        data["puntos2"],
    )

    if error:
        status = 404 if "no encontrados" in error else 400
        return jsonify({"error": error}), status

    return jsonify(tabla), 200
@app.route('/registro', methods=['POST'])
def registro():
    data = request.get_json()
    user = data.get('user')
    password = data.get('password')
    
    try:
        register(user, password)
        return jsonify({'success': True, 'message': 'registro con exito'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/resetPassword', methods=['POST'])
def reset_password_user():
    data = request.get_json()
    user = data.get('user')
    password = data.get('password')
    
    try:
        reset_password(user, password)
        return jsonify({'success': True, 'message': 'contraseña se realizo el cambio con exito'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route("/grupos", methods=["GET"])
@token_required
def obtener_todos_los_grupos_route():
    tabla, error = obtener_todos_los_grupos()

    if error:
        return jsonify({"error": error}), 404

    return jsonify(tabla), 200


@app.route("/grupos/<nombre_grupo>", methods=["GET"])
@token_required
def obtener_grupo_route(nombre_grupo):
    tabla, error = obtener_grupo(nombre_grupo)

    if error:
        return jsonify({"error": error}), 404

    return jsonify({"grupo": nombre_grupo, "tabla": tabla}), 200


@app.route("/grupos/<nombre_grupo>/puntos", methods=["PUT"])
@token_required
def actualizar_puntos_grupo_route(nombre_grupo):
    data = request.get_json()
    if not data:
        return jsonify({"error": "El cuerpo no puede estar vacío"}), 400

    campos_requeridos = ["pais1", "puntos1", "pais2", "puntos2"]
    faltantes = [c for c in campos_requeridos if c not in data]
    if faltantes:
        return jsonify({"error": f"Faltan los campos: {faltantes}"}), 400

    tabla, error = actualizar_puntos_grupo(
        nombre_grupo,
        data["pais1"],
        data["puntos1"],
        data["pais2"],
        data["puntos2"],
    )

    if error:
        status = 404 if "no encontrado" in error or "no pertenecen" in error else 400
        return jsonify({"error": error}), status

    return jsonify({"grupo": nombre_grupo, "tabla": tabla}), 200

@app.route("/grupos/<nombre_grupo>/pais", methods=["PATCH"])
@token_required
def actualizar_puntos_pais_route(nombre_grupo):
    data = request.get_json()
    if not data or "pais" not in data or "puntos" not in data:
        return jsonify({"error": "El cuerpo debe tener 'pais' y 'puntos'"}), 400

    tabla, error = actualizar_puntos_pais(nombre_grupo, data["pais"], data["puntos"])

    if error:
        status = 404
        return jsonify({"error": error}), status

    return jsonify({"grupo": nombre_grupo, "tabla": tabla}), 200


@app.route("/grupos/reset", methods=["POST"])
@token_required
@admin_required
def resetear_puntos_route():
    ok, error = resetear_puntos()

    if error:
        return jsonify({"error": error}), 404

    return jsonify({"mensaje": "Todos los puntos han sido reiniciados a 0"}), 200


@app.route("/ranking", methods=["GET"])
@token_required
def ranking_global_route():
    top = request.args.get("top", 10, type=int)
    ranking, error = ranking_global(top)

    if error:
        return jsonify({"error": error}), 404

    return jsonify({"ranking": ranking}), 200

@app.route("/predicciones", methods=["POST"])
@token_required
def predecir_partido_route():
    data = request.get_json()
    if not data:
        return jsonify({"error": "El cuerpo no puede estar vacío"}), 400

    campos_requeridos = ["partido_id", "goles_local", "goles_visitante"]
    faltantes = [c for c in campos_requeridos if c not in data]
    if faltantes:
        return jsonify({"error": f"Faltan los campos: {faltantes}"}), 400

    prediccion, error = predecir_partido(
        request.user,
        data["partido_id"],
        data["goles_local"],
        data["goles_visitante"],
    )

    if error:
        status = 400 if ("inválido" in error or "finalizó" in error) else 404
        return jsonify({"error": error}), status

    return jsonify(prediccion), 200


@app.route("/predicciones", methods=["GET"])
@token_required
def obtener_predicciones_usuario_route():
    predicciones, error = obtener_predicciones_usuario(request.user)

    if error:
        return jsonify({"error": error}), 404

    return jsonify(predicciones), 200


@app.route("/predicciones/<partido_id>", methods=["GET"])
@token_required
def obtener_prediccion_route(partido_id):
    prediccion, error = obtener_prediccion(request.user, partido_id)

    if error:
        return jsonify({"error": error}), 404

    return jsonify(prediccion), 200
@app.route("/partidos", methods=["POST"])
@token_required
def crear_partido_route():
    data = request.get_json()
    if not data:
        return jsonify({"error": "El cuerpo no puede estar vacío"}), 400

    campos_requeridos = ["equipo_local", "equipo_visitante", "fecha"]
    faltantes = [c for c in campos_requeridos if c not in data]
    if faltantes:
        return jsonify({"error": f"Faltan los campos: {faltantes}"}), 400

    partido, error = crear_partido(
        data["equipo_local"],
        data["equipo_visitante"],
        data["fecha"],
        data.get("grupo"),
    )

    if error:
        return jsonify({"error": error}), 400

    return jsonify(partido), 201


@app.route("/partidos", methods=["GET"])
@token_required
def obtener_partidos_route():
    partidos, error = obtener_partidos()

    if error:
        return jsonify({"error": error}), 404

    return jsonify(partidos), 200


@app.route("/partidos/<partido_id>", methods=["GET"])
@token_required
def obtener_partido_route(partido_id):
    partido, error = obtener_partido(partido_id)

    if error:
        status = 400 if "inválido" in error else 404
        return jsonify({"error": error}), status

    return jsonify(partido), 200


@app.route("/partidos/<partido_id>/resultado", methods=["PUT"])
@token_required
@admin_required
def cargar_resultado_route(partido_id):
    data = request.get_json()
    if not data or "goles_local" not in data or "goles_visitante" not in data:
        return jsonify({"error": "El cuerpo debe tener 'goles_local' y 'goles_visitante'"}), 400

    partido, error = cargar_resultado(partido_id, data["goles_local"], data["goles_visitante"])

    if error:
        status = 400 if ("inválido" in error or "ya tiene" in error) else 404
        return jsonify({"error": error}), status

    return jsonify(partido), 200
@app.route("/partidos/resultado-por-equipos", methods=["PUT"])
@token_required
@admin_required
def cargar_resultado_por_equipos_route():
    data = request.get_json()
    campos_requeridos = ["equipo1", "goles_equipo1", "equipo2", "goles_equipo2"]
    if not data or any(c not in data for c in campos_requeridos):
        return jsonify({"error": f"El cuerpo debe tener: {campos_requeridos}"}), 400

    partido, error = cargar_resultado_por_equipos(
        data["equipo1"], data["equipo2"],
        data["goles_equipo1"], data["goles_equipo2"],
    )

    if error:
        status = 400 if ("más de un partido" in error or "ya tiene" in error) else 404
        return jsonify({"error": error}), status

    return jsonify(partido), 200

@app.route("/usuarios/rol", methods=["PATCH"])
@token_required
@admin_required
def cambiar_rol_route():
    data = request.get_json()
    if not data or "user" not in data or "rol" not in data:
        return jsonify({"error": "El cuerpo debe tener 'user' y 'rol'"}), 400

    resultado, error = cambiar_rol(data["user"], data["rol"])

    if error:
        status = 404 if "no encontrado" in error else 400
        return jsonify({"error": error}), status

    return jsonify(resultado), 200
@app.route("/usuarios/perfil", methods=["GET"])
@token_required
def perfil_route():
    perfil, error = obtener_perfil(request.user)

    if error:
        return jsonify({"error": error}), 404

    return jsonify(perfil), 200
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(debug=False, host="0.0.0.0", port=port)