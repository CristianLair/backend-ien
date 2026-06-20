import os
import jwt
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import request, jsonify

SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
ALGORITHM = "HS256"


def generar_token(user, rol="cliente"):
    payload = {
        "user": user,
        "rol": rol,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"error": "Falta el header Authorization"}), 401

        partes = auth_header.split(" ")
        if len(partes) != 2 or partes[0] != "Bearer":
            return jsonify({"error": "Formato esperado: Bearer <token>"}), 401

        token = partes[1]

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "El token expiró"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido"}), 401

        request.user = payload.get("user")
        request.rol = payload.get("rol", "cliente")

        return f(*args, **kwargs)

    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if getattr(request, "rol", None) != "admin":
            return jsonify({"error": "Esta acción requiere rol de administrador"}), 403

        return f(*args, **kwargs)

    return decorated