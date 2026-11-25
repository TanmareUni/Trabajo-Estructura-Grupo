"""
Modulo ciudades: catalogo fijo de las seis ciudades del recorrido (RF03).
El orden es de sur a norte: la posicion sirve para calcular tramos y tarifas.
"""

from archivos import leer_archivo, guardar_archivo

ARCHIVO_CIUDADES = "ciudades.json"

CIUDADES_BASE = [
    {"id_ciudad": 1, "nombre": "Concepción", "posicion": 0},
    {"id_ciudad": 2, "nombre": "Chillán", "posicion": 1},
    {"id_ciudad": 3, "nombre": "Linares", "posicion": 2},
    {"id_ciudad": 4, "nombre": "Talca", "posicion": 3},
    {"id_ciudad": 5, "nombre": "Rancagua", "posicion": 4},
    {"id_ciudad": 6, "nombre": "Santiago", "posicion": 5},
]


#1 Cargar ciudades si el archivo no existe o esta vacio, se crea con el catalogo base
def cargar_ciudades() -> list[dict]:
#Retorna la lista de ciudades guardada en el archivo (la crea si no existe)
    ciudades = leer_archivo(ARCHIVO_CIUDADES)
    if len(ciudades) == 0:
        guardar_archivo(ARCHIVO_CIUDADES, CIUDADES_BASE)
        ciudades = CIUDADES_BASE
    return ciudades


#2 Buscar ciudad por ID se usa para validar los viajes y los pasajes
def buscar_ciudad(ciudades: list[dict], id_ciudad: int) -> dict:
#Retorna la ciudad con ese ID manda ValueError si no existe
    for ciudad in ciudades:
        if ciudad["id_ciudad"] == id_ciudad:
            return ciudad
    raise ValueError("La ciudad no existe en el catálogo")


#3 Obtener posición número de la ciudad en el recorrido (0 = Concepción, 5 = Santiago)
def obtener_posicion(ciudades: list[dict], id_ciudad: int) -> int:
#Retorna la posición de la ciudad en el recorrido manda ValueError si no existe
    ciudad = buscar_ciudad(ciudades, id_ciudad)
    return ciudad["posicion"]