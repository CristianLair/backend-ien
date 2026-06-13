from flask import Flask ,jsonify, request
import sys
import os

# Agrega la carpeta src al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from db.db import db
from controllers.puntajegeneral import cargar_puntos
app = Flask(__name__)

@app.route("/")
def home():
    return {"mensaje": "Servidor funcionando ✅"}

@app.route("/ranking", methods=["POST"])
def ranking():
    body = request.get_json()

    pais = body.get("pais")
    puntos = body.get("puntos")

    if pais is None or puntos is None:
        return jsonify({"error": "Faltan los campos 'pais' y 'puntos'"}), 400

    tabla, error = cargar_puntos(pais, puntos)

    if error:
        return jsonify({"error": error}), 404

    return jsonify(tabla), 200

if __name__ == "__main__":
    app.run(debug=True, port=3000)