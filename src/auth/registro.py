from db.db import db
import bcrypt

def register(user=None, password=None):
    if not user or not password:
        raise Exception('El usuario y la contraseña son obligatorios')

    existing_user = db['usuarios'].find_one({'user': user})
    if existing_user:
        raise Exception('El usuario ya existe')

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_user = {
        'user': user,
        'password': hashed,
        'puntos': 0,
        'apuesta': False,
        'rol': 'cliente',
    }
    db['usuarios'].insert_one(new_user)

    return True