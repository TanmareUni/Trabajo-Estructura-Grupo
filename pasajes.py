
from archivos import leer_archivo, guardar_archivo, siguiente_id
from asientos import (ESTADO_VIGENTE, ESTADO_ANULADO, obtener_tramo,
                      validar_asiento, asiento_libre_en_tramo)
from ciudades import obtener_posicion
from clientes import buscar_cliente
from tarifas import calcular_tarifa
from viajes import buscar_viaje, obtener_capacidad_viaje, obtener_sentido

ARCHIVO_PASAJES = "pasajes.json"



def cargar_pasajes() -> list[dict]:

    return leer_archivo(ARCHIVO_PASAJES)



def guardar_pasajes(pasajes: list[dict]) -> None:

    guardar_archivo(ARCHIVO_PASAJES, pasajes)



def registrar_pasaje(pasajes: list[dict], clientes: list[dict], viajes: list[dict],
                     buses: list[dict], ciudades: list[dict], id_cliente: int, id_viaje: int,
                     id_origen: int, id_destino: int, asiento: int) -> dict:

    buscar_cliente(clientes, id_cliente)
    viaje = buscar_viaje(viajes, id_viaje)

    pos_origen = obtener_posicion(ciudades, id_origen)
    pos_destino = obtener_posicion(ciudades, id_destino)
    if pos_origen == pos_destino:
        raise ValueError("El origen y el destino no pueden ser iguales")


    sentido_pasaje = 1 if pos_destino > pos_origen else -1
    if sentido_pasaje != obtener_sentido(ciudades, viaje):
        raise ValueError("El tramo no respeta el sentido del viaje")

    capacidad = obtener_capacidad_viaje(viajes, buses, id_viaje)
    validar_asiento(asiento, capacidad)

    tramo = obtener_tramo(ciudades, id_origen, id_destino)
    if not asiento_libre_en_tramo(pasajes, ciudades, id_viaje, asiento, tramo):
        raise ValueError("El asiento ya está ocupado en un tramo que se superpone")

    nuevo_pasaje = {
        "id_pasaje": siguiente_id(pasajes, "id_pasaje"),
        "id_viaje": id_viaje,
        "id_cliente": id_cliente,
        "id_origen": id_origen,
        "id_destino": id_destino,
        "asiento": asiento,
        "valor": calcular_tarifa(viaje["tarifa_base"], pos_origen, pos_destino),
        "estado": ESTADO_VIGENTE
    }
    pasajes.append(nuevo_pasaje)
    return nuevo_pasaje



def buscar_pasaje(pasajes: list[dict], id_pasaje: int) -> dict:

    for pasaje in pasajes:
        if pasaje["id_pasaje"] == id_pasaje:
            return pasaje
    raise ValueError("No existe un pasaje con ese ID")



def anular_pasaje(pasajes: list[dict], id_pasaje: int) -> dict:

    pasaje = buscar_pasaje(pasajes, id_pasaje)
    if pasaje["estado"] == ESTADO_ANULADO:
        raise ValueError("El pasaje ya está anulado")
    pasaje["estado"] = ESTADO_ANULADO
    return pasaje



def obtener_pasajes_viaje(pasajes: list[dict], id_viaje: int, estado: str | None = None) -> list[dict]:

    resultado: list[dict] = []
    for pasaje in pasajes:
        if pasaje["id_viaje"] != id_viaje:
            continue
        if estado is not None and pasaje["estado"] != estado:
            continue
        resultado.append(pasaje)
    return resultado



def calcular_recaudacion(pasajes: list[dict], id_viaje: int) -> int:

    total = 0
    for pasaje in obtener_pasajes_viaje(pasajes, id_viaje, ESTADO_VIGENTE):
        total += pasaje["valor"]
    return total