
from ciudades import obtener_posicion

ESTADO_VIGENTE = "vigente"
ESTADO_ANULADO = "anulado"



def obtener_tramo(ciudades: list[dict], id_origen: int, id_destino: int) -> tuple[int, int]:

    pos_origen = obtener_posicion(ciudades, id_origen)
    pos_destino = obtener_posicion(ciudades, id_destino)
    return (min(pos_origen, pos_destino), max(pos_origen, pos_destino))



def tramos_se_superponen(tramo_a: tuple[int, int], tramo_b: tuple[int, int]) -> bool:

    return tramo_a[0] < tramo_b[1] and tramo_b[0] < tramo_a[1]



def validar_asiento(asiento: int, capacidad: int) -> None:

    if not isinstance(asiento, int) or isinstance(asiento, bool):
        raise ValueError("El asiento debe ser un número entero")
    if asiento < 1 or asiento > capacidad:
        raise ValueError(f"El asiento debe estar entre 1 y {capacidad}")



def asiento_libre_en_tramo(pasajes: list[dict], ciudades: list[dict], id_viaje: int,
                           asiento: int, tramo: tuple[int, int]) -> bool:


    for pasaje in pasajes:
        if pasaje["id_viaje"] != id_viaje or pasaje["asiento"] != asiento:
            continue
        if pasaje["estado"] != ESTADO_VIGENTE:
            continue
        tramo_vendido = obtener_tramo(ciudades, pasaje["id_origen"], pasaje["id_destino"])
        if tramos_se_superponen(tramo, tramo_vendido):
            return False
    return True



def ocupacion_por_tramo(pasajes: list[dict], ciudades: list[dict], id_viaje: int,
                        capacidad: int, tramo: tuple[int, int]) -> dict[str, list[int]]:

    ocupados: list[int] = []
    libres: list[int] = []
    for asiento in range(1, capacidad + 1):
        if asiento_libre_en_tramo(pasajes, ciudades, id_viaje, asiento, tramo):
            libres.append(asiento)
        else:
            ocupados.append(asiento)
    return {"ocupados": ocupados, "libres": libres}