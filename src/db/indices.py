from db import db
 
def crear_indices():
    db["usuarios"].create_index("user", unique=True)
    db["predicciones"].create_index(
        [("user", 1), ("partido_id", 1)],
        unique=True,
    )
    db["predicciones"].create_index([("partido_id", 1), ("procesado", 1)])
 
    print("Índices creados correctamente.")
 
 
if __name__ == "__main__":
    crear_indices()