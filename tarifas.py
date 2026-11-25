"""
Módulo tarifas: cálculo automático del precio de un pasaje (RF05).
El precio depende de cuántos segmentos del recorrido completo se utilizan.
No usa tabla de combinaciones y no depende del sentido del viaje.
"""

SEGMENTOS_TOTALES = 5          #Concepción (0) -> Santiago (5) son 5 segmentos
DESCUENTO_POR_SEGMENTO = 10    #% de la tarifa base por cada segmento NO utilizado


#1 Contar segmentos cuantos tramos del recorrido recorre el pasajero
def contar_segmentos(pos_origen: int, pos_destino: int) -> int:
#Retorna la cantidad de segmentos entre dos posiciones (sin importar el sentido)
    return abs(pos_destino - pos_origen)


#2 Calcular tarifa descuento acumulativo (no compuesto) por segmento no utilizado
def calcular_tarifa(tarifa_base: int, pos_origen: int, pos_destino: int) -> int:
#Retorna el precio del pasaje. Lanza ValueError si los datos no son válidos
#Ejemplo con base 10000: Concepción(0) -> Talca(3) usa 3 segmentos, 2 sin usar = 20% de descuento = 8000
    if tarifa_base <= 0:
        raise ValueError("La tarifa base debe ser mayor que cero")

    if pos_origen == pos_destino:
        raise ValueError("El origen y el destino no pueden ser iguales")

    usados = contar_segmentos(pos_origen, pos_destino)
    if usados > SEGMENTOS_TOTALES:
        raise ValueError("El tramo está fuera del recorrido")

    no_usados = SEGMENTOS_TOTALES - usados
    porcentaje = 100 - no_usados * DESCUENTO_POR_SEGMENTO

    #se suma 50 antes de dividir para redondear hacia arriba en mitades
    return (tarifa_base * porcentaje + 50) // 100