#Paises participantes
ranking_selecciones = [{"Canadá": 0,
  "México": 0,
  "Estados Unidos": 0,
  "Alemania": 0,
  "Austria": 0,
  "Bélgica": 0,
  "Bosnia y Herzegovina": 0,
  "Croacia": 0,
  "Escocia": 0,
  "España": 0,
  "Francia": 0,
  "Inglaterra": 0,
  "Noruega": 0,
  "Países Bajos": 0,
  "Portugal": 0,
  "República Checa": 0,
  "Suecia": 0,
  "Suiza": 0,
  "Turquía": 0,
  "Argentina": 0,
  "Brasil": 0,
  "Colombia": 0,
  "Ecuador": 0,
  "Paraguay": 0,
  "Uruguay": 0,
  "Argelia": 0,
  "Cabo Verde": 0,
  "Costa de Marfil": 0,
  "Egipto": 0,
  "Ghana": 0,
  "Marruecos": 0,
  "RD Congo": 0,
  "Senegal": 0,
  "Sudáfrica": 0,
  "Túnez": 0,
  "Arabia Saudita": 0,
  "Australia": 0,
  "Corea del Sur": 0,
  "Irak": 0,
  "Irán": 0,
  "Japón": 0,
  "Jordania": 0,
  "Qatar": 0,
  "Uzbekistán": 0,
  "Curazao": 0,
  "Haití": 0,
  "Panamá": 0,
  "Nueva Zelanda": 0 }]
#Lista de grupos
grupos = {
    "GrupoA": [{'México': 0, 'Sudáfrica': 0, 'Corea del Sur': 0, 'República Checa': 0,}],
    "GrupoB": [{'Canadá': 0, 'Qatar': 0, 'Suiza': 0,  'Bosnia y Herzegovina': 0,}],
    "GrupoC": [{'Brasil': 0, 'Marruecos': 0, 'Haití': 0, 'Escocia': 0}],
    "GrupoD": [{'Estados Unidos': 0, 'Paraguay': 0, 'Australia': 0, 'Turquía': 0,}],
    "GrupoE": [{'Alemania': 0, 'Curazao': 0, 'Costa de Marfil': 0, 'Ecuador': 0}],
    "GrupoF": [{'Países Bajos': 0, 'Japón': 0, 'Túnez': 0, 'Suecia': 0}],
    "GrupoG": [{'Bélgica': 0, 'Egipto': 0, 'Irán': 0, 'Nueva Zelanda': 0}],
    "GrupoH": [{'España': 0, 'Cabo Verde': 0, 'Arabia Saudita': 0, 'Uruguay': 0}],
    "GrupoI": [{'Francia': 0, 'Senegal': 0, 'Noruega': 0, 'Irak': 0}],
    "GrupoJ": [{'Argentina': 0, 'Argelia': 0, 'Austria': 0, 'Jordania': 0}],
    "GrupoK": [{'Portugal': 0, 'Uzbekistán': 0, 'Colombia': 0, 'RD Congo': 0}],
    "GrupoL": [{'Inglaterra': 0, 'Croacia': 0, 'Ghana': 0, 'Panamá': 0}]
}
def cargar_todos_los_puntos(grupos):
    for grupo in grupos:
        for pais in grupos[grupo][0]:
            puntos = int(input(f"Ingrese los puntos de {pais}: "))
            grupos[grupo][0][pais] = puntos
cargar_todos_los_puntos(grupos)

for grupo in grupos:
    print(f"\n{grupo}")
    ordenado = sorted(
        grupos[grupo][0].items(),
        key=lambda x: x[1],
        reverse=True
    )
    for pais, puntos in ordenado:
        print(f"{pais}: {puntos} puntos")
