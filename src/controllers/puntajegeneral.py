ranking_selecciones = {
    "Canadá": 0, "México": 0, "Estados Unidos": 0,
    "Alemania": 0, "Austria": 0, "Bélgica": 0,
    "Bosnia y Herzegovina": 0, "Croacia": 0, "Escocia": 0,
    "España": 0, "Francia": 0, "Inglaterra": 0,
    "Noruega": 0, "Países Bajos": 0, "Portugal": 0,
    "República Checa": 0, "Suecia": 0, "Suiza": 0,
    "Turquía": 0, "Argentina": 0, "Brasil": 0,
    "Colombia": 0, "Ecuador": 0, "Paraguay": 0,
    "Uruguay": 0, "Argelia": 0, "Cabo Verde": 0,
    "Costa de Marfil": 0, "Egipto": 0, "Ghana": 0,
    "Marruecos": 0, "RD Congo": 0, "Senegal": 0,
    "Sudáfrica": 0, "Túnez": 0, "Arabia Saudita": 0,
    "Australia": 0, "Corea del Sur": 0, "Irak": 0,
    "Irán": 0, "Japón": 0, "Jordania": 0,
    "Qatar": 0, "Uzbekistán": 0, "Curazao": 0,
    "Haití": 0, "Panamá": 0, "Nueva Zelanda": 0
}

def cargar_puntos(pais, puntos):
    if pais not in ranking_selecciones:
        return None, f"El país '{pais}' no existe en el ranking"

    ranking_selecciones[pais] = int(puntos)

    tabla = sorted(
        ranking_selecciones.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return [{"posicion": i, "pais": p, "puntos": pts}
            for i, (p, pts) in enumerate(tabla, start=1)], None  