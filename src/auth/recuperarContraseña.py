from db.db import db
import bcrypt

def reset_password(user=None, new_password=None):
    if not user or not new_password:
        raise Exception('El usuario y la nueva contraseña son obligatorios')
    
    found_user = db['usuarios'].find_one({'user': user})
    if not found_user:
        raise Exception('Usuario no encontrado')
    
    hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    
    db['usuarios'].update_one(
        {'user': user},
        {'$set': {'password': hashed}}
    )
    
    return {'message': 'Contraseña actualizada exitosamente'}