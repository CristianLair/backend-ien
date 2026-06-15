from flask import Flask ,jsonify, request
from flask_cors import CORS
import sys
import os

# Agrega la carpeta src al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from db.db import db
from controllers.puntajegeneral import obtener_paises
app = Flask(__name__)
CORS(app)
@app.route("/")
def home():
    return {"mensaje": "Servidor funcionando ✅"}

@app.route("/paises", methods=["GET"])
def ranking():
    tabla, error = obtener_paises()

    if error:
        return jsonify({"error": error}), 404

    return jsonify(tabla), 200
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(debug=False, host="0.0.0.0", port=port)