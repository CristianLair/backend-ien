from flask import Flask ,jsonify, request
from flask_cors import CORS
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from db.db import db
from controllers.puntajegeneral import obtener_paises
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

@app.route("/paises", methods=["GET"])
def ranking():
    tabla, error = obtener_paises()

    if error:
        return jsonify({"error": error}), 404

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

@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    user = data.get('user')
    password = data.get('password')
    
    try:
        login(user, password)
        return jsonify({'success': True, 'message': 'login realizado con exito'}), 200
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
def obtener_todos_los_grupos_route():
    tabla, error = obtener_todos_los_grupos()

    if error:
        return jsonify({"error": error}), 404

    return jsonify(tabla), 200


@app.route("/grupos/<nombre_grupo>", methods=["GET"])
def obtener_grupo_route(nombre_grupo):
    tabla, error = obtener_grupo(nombre_grupo)

    if error:
        return jsonify({"error": error}), 404

    return jsonify({"grupo": nombre_grupo, "tabla": tabla}), 200


@app.route("/grupos/<nombre_grupo>/puntos", methods=["PUT"])
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
def resetear_puntos_route():
    ok, error = resetear_puntos()

    if error:
        return jsonify({"error": error}), 404

    return jsonify({"mensaje": "Todos los puntos han sido reiniciados a 0"}), 200


@app.route("/ranking", methods=["GET"])
def ranking_global_route():
    top = request.args.get("top", 10, type=int)
    ranking, error = ranking_global(top)

    if error:
        return jsonify({"error": error}), 404

    return jsonify({"ranking": ranking}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(debug=False, host="0.0.0.0", port=port)