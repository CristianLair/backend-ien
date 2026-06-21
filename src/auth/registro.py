from db.db import db
import re
import bcrypt
def tiene_caracteres_especiales(texto):
    return re.search(r"[^A-Za-z0-9]", texto) is not None
def register(user=None, password=None):
    if not isinstance(user, str) or not isinstance(password, str):
        raise Exception('Usuario y contraseña deben ser texto')

    if not user or not password:
        raise Exception('El usuario y la contraseña son obligatorios')
    if not user.strip() or not password.strip():
        raise Exception("El usuario y contraseña no puede contener espacios.")
    validacionUser = tiene_caracteres_especiales(user)
    if validacionUser == True:
        raise Exception("El usuario no puede contener carecteres especiales.")
    user = user.lower().strip()
    existing_user = db['usuarios'].find_one({'user': user})
    if existing_user:
        raise Exception('El usuario ya existe')

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    new_user = {
        'user': user,
        'password': hashed,
        'puntos': 0,
        'apuesta': False,
        'rol': 'cliente',
    }
    db['usuarios'].insert_one(new_user)

    return True