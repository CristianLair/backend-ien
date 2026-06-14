from flask import Flask, jsonify, request
from copy import deepcopy

app = Flask(__name__)


GRUPOS = {
    "GrupoA": {"México": 0, "Sudáfrica": 0, "Corea del Sur": 0, "República Checa": 0},
    "GrupoB": {"Canadá": 0, "Qatar": 0, "Suiza": 0, "Bosnia y Herzegovina": 0},
    "GrupoC": {"Brasil": 0, "Marruecos": 0, "Haití": 0, "Escocia": 0},
    "GrupoD": {"Estados Unidos": 0, "Paraguay": 0, "Australia": 0, "Turquía": 0},
    "GrupoE": {"Alemania": 0, "Curazao": 0, "Costa de Marfil": 0, "Ecuador": 0},
    "GrupoF": {"Países Bajos": 0, "Japón": 0, "Túnez": 0, "Suecia": 0},
    "GrupoG": {"Bélgica": 0, "Egipto": 0, "Irán": 0, "Nueva Zelanda": 0},
    "GrupoH": {"España": 0, "Cabo Verde": 0, "Arabia Saudita": 0, "Uruguay": 0},
    "GrupoI": {"Francia": 0, "Senegal": 0, "Noruega": 0, "Irak": 0},
    "GrupoJ": {"Argentina": 0, "Argelia": 0, "Austria": 0, "Jordania": 0},
    "GrupoK": {"Portugal": 0, "Uzbekistán": 0, "Colombia": 0, "RD Congo": 0},
    "GrupoL": {"Inglaterra": 0, "Croacia": 0, "Ghana": 0, "Panamá": 0},
}

grupos = deepcopy(GRUPOS)



def grupo_ordenado(nombre_grupo):
    return [
        {"pais": pais, "puntos": pts}
        for pais, pts in sorted(
            grupos[nombre_grupo].items(), key=lambda x: x[1], reverse=True
        )
    ]



@app.route("/")
def root():
    return jsonify({"mensaje": "API Ranking Selecciones — endpoints disponibles en /grupos"})


@app.route("/grupos", methods=["GET"])
def obtener_todos_los_grupos():
    return jsonify({nombre: grupo_ordenado(nombre) for nombre in grupos})


@app.route("/grupos/<nombre_grupo>", methods=["GET"])
def obtener_grupo(nombre_grupo):
    if nombre_grupo not in grupos:
        return jsonify({"error": f"Grupo '{nombre_grupo}' no encontrado"}), 404
    return jsonify({"grupo": nombre_grupo, "tabla": grupo_ordenado(nombre_grupo)})


@app.route("/grupos/<nombre_grupo>/puntos", methods=["PUT"])
def actualizar_puntos_grupo(nombre_grupo):
    if nombre_grupo not in grupos:
        return jsonify({"error": f"Grupo '{nombre_grupo}' no encontrado"}), 404

    data = request.get_json()
    if not data or "puntos" not in data:
        return jsonify({"error": "El cuerpo debe tener la clave 'puntos'"}), 400

    paises_invalidos = [p for p in data["puntos"] if p not in grupos[nombre_grupo]]
    if paises_invalidos:
        return jsonify({"error": f"Países no pertenecen a {nombre_grupo}: {paises_invalidos}"}), 400

    grupos[nombre_grupo].update(data["puntos"])
    return jsonify({"grupo": nombre_grupo, "tabla": grupo_ordenado(nombre_grupo)})


@app.route("/grupos/<nombre_grupo>/pais", methods=["PATCH"])
def actualizar_puntos_pais(nombre_grupo):
    if nombre_grupo not in grupos:
        return jsonify({"error": f"Grupo '{nombre_grupo}' no encontrado"}), 404

    data = request.get_json()
    if not data or "pais" not in data or "puntos" not in data:
        return jsonify({"error": "El cuerpo debe tener 'pais' y 'puntos'"}), 400

    pais = data["pais"]
    if pais not in grupos[nombre_grupo]:
        return jsonify({"error": f"'{pais}' no pertenece al {nombre_grupo}"}), 404

    grupos[nombre_grupo][pais] = data["puntos"]
    return jsonify({"grupo": nombre_grupo, "tabla": grupo_ordenado(nombre_grupo)})


@app.route("/grupos/reset", methods=["POST"])
def resetear_puntos():
    global grupos
    grupos = deepcopy(GRUPOS)
    return jsonify({"mensaje": "Todos los puntos han sido reiniciados a 0"})


@app.route("/ranking", methods=["GET"])
def ranking_global():
    top = request.args.get("top", 10, type=int)
    todos = [
        {"pais": pais, "grupo": nombre_grupo, "puntos": pts}
        for nombre_grupo, paises in grupos.items()
        for pais, pts in paises.items()
    ]
    todos.sort(key=lambda x: x["puntos"], reverse=True)
    return jsonify({"ranking": todos[:top]})

if __name__ == "__main__":
    app.run(debug=True)