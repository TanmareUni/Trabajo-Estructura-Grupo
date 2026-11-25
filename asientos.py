"""
Módulo asientos: reutilización de asientos por tramo y ocupación (RF06, RF09).

Un mismo asiento podrá asignarse a varios pasajeros en un viaje únicamente si sus tramos no se superponen. Ejemplo
válido: asiento 12 Concepción–Chillán; luego Chillán–Talca; después Talca–Santiago. Ejemplo inválido: asiento 12
Chillán–Talca y Linares–Rancagua, porque existe superposición.

El descenso en una ciudad libera el asiento para un embarque en esa misma ciudad. La validación debe considerar el
sentido del viaje, las ventas vigentes y los datos persistidos tras reiniciar la aplicación.
"""

from ciudades import obtener_posicion

ESTADO_VIGENTE = "vigente"
ESTADO_ANULADO = "anulado"


#1 Obtener tramo convierte origen/destino (IDs de ciudad) en un tramo ordenado de posiciones
def obtener_tramo(ciudades: list[dict], id_origen: int, id_destino: int) -> tuple[int, int]:
#Retorna (inicio, fin) sin importar el sentido. Lanza ValueError si una ciudad no existe
    pos_origen = obtener_posicion(ciudades, id_origen)
    pos_destino = obtener_posicion(ciudades, id_destino)
    return (min(pos_origen, pos_destino), max(pos_origen, pos_destino))


#2 Tramos se superponen revisa si dos tramos comparten algún segmento
def tramos_se_superponen(tramo_a: tuple[int, int], tramo_b: tuple[int, int]) -> bool:
#Retorna True si hay superposición. (0,1) y (1,3) NO se superponen; (1,3) y (2,4) sí
    return tramo_a[0] < tramo_b[1] and tramo_b[0] < tramo_a[1]


#3 Validar asiento revisa que el número esté dentro de la capacidad del bus
def validar_asiento(asiento: int, capacidad: int) -> None:
#Lanza ValueError si el asiento no es un entero entre 1 y la capacidad
    if not isinstance(asiento, int) or isinstance(asiento, bool):
        raise ValueError("El asiento debe ser un número entero")
    if asiento < 1 or asiento > capacidad:
        raise ValueError(f"El asiento debe estar entre 1 y {capacidad}")


#4 Asiento libre en tramo búsqueda secuencial sobre las ventas vigentes del viaje
def asiento_libre_en_tramo(pasajes: list[dict], ciudades: list[dict], id_viaje: int,
                           asiento: int, tramo: tuple[int, int]) -> bool:
#Retorna True si ningún pasaje vigente del viaje usa ese asiento en un tramo superpuesto
#Los pasajes anulados se ignoran (no participan en la ocupación)
    for pasaje in pasajes:
        if pasaje["id_viaje"] != id_viaje or pasaje["asiento"] != asiento:
            continue
        if pasaje["estado"] != ESTADO_VIGENTE:
            continue
        tramo_vendido = obtener_tramo(ciudades, pasaje["id_origen"], pasaje["id_destino"])
        if tramos_se_superponen(tramo, tramo_vendido):
            return False
    return True


#5 Ocupación por tramo lista de asientos ocupados y libres para un tramo (RF09)
def ocupacion_por_tramo(pasajes: list[dict], ciudades: list[dict], id_viaje: int,
                        capacidad: int, tramo: tuple[int, int]) -> dict[str, list[int]]:
#Retorna {"ocupados": [...], "libres": [...]} con números de asiento en orden ascendente
    ocupados: list[int] = []
    libres: list[int] = []
    for asiento in range(1, capacidad + 1):
        if asiento_libre_en_tramo(pasajes, ciudades, id_viaje, asiento, tramo):
            libres.append(asiento)
        else:
            ocupados.append(asiento)
    return {"ocupados": ocupados, "libres": libres}