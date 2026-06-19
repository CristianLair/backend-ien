from flask import Flask ,jsonify, request
from flask_cors import CORS
import sys
import os

# Agrega la carpeta src al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from db.db import db
from controllers.puntajegeneral import obtener_paises
from auth.registro import register
from auth.login import login
from auth.recuperarContraseña import reset_password

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
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(debug=False, host="0.0.0.0", port=port)