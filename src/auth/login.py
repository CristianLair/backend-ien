from db.db import db
import bcrypt
from utils.middleweare import generar_token

def login(user=None, password=None):
    if not user or not password:
        raise Exception('El usuario y la contraseña son obligatorios')

    found_user = db['usuarios'].find_one({'user': user})
    if not found_user:
        raise Exception('Usuario no encontrado')

    stored_password = found_user['password']


    print(f"[DEBUG login] type(password)={type(password)} type(stored_password)={type(stored_password)}")

    if isinstance(stored_password, str):
        stored_password = stored_password.encode('utf-8')
    if isinstance(password, str):
        password_bytes = password.encode('utf-8')
    else:
        password_bytes = password

    if not bcrypt.checkpw(password_bytes, stored_password):
        raise Exception('Contraseña inválida')

    rol = found_user.get('rol', 'cliente')
    token = generar_token(user, rol)
    return token