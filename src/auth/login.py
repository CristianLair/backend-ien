from db.db import db  
import bcrypt
def login(user=None, password=None):
    if not user or not password:
        raise Exception('El usuario y la contraseña son obligatorios')
    
    found_user = db['usuarios'].find_one({'user': user})
    if not found_user:
        raise Exception('Usuario no encontrado')
    if not bcrypt.checkpw(password.encode('utf-8'), found_user['password']):
        raise Exception('Contraseña inválida')
    
    return found_user
    
    
     
