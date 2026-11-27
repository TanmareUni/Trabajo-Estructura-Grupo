
SEGMENTOS_TOTALES = 5
DESCUENTO_POR_SEGMENTO = 10



def contar_segmentos(pos_origen: int, pos_destino: int) -> int:

    return abs(pos_destino - pos_origen)



def calcular_tarifa(tarifa_base: int, pos_origen: int, pos_destino: int) -> int:


    if tarifa_base <= 0:
        raise ValueError("La tarifa base debe ser mayor que cero")

    if pos_origen == pos_destino:
        raise ValueError("El origen y el destino no pueden ser iguales")

    usados = contar_segmentos(pos_origen, pos_destino)
    if usados > SEGMENTOS_TOTALES:
        raise ValueError("El tramo está fuera del recorrido")

    no_usados = SEGMENTOS_TOTALES - usados
    porcentaje = 100 - no_usados * DESCUENTO_POR_SEGMENTO


    return (tarifa_base * porcentaje + 50) // 100