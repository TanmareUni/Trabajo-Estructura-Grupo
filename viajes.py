
from datetime import datetime

from archivos import leer_archivo, guardar_archivo, siguiente_id
from buses import buscar_bus
from ciudades import obtener_posicion
from tarifas import SEGMENTOS_TOTALES

ARCHIVO_VIAJES = "viajes.json"
TARIFA_BASE_DEFECTO = 10000



def cargar_viajes() -> list[dict]:

    return leer_archivo(ARCHIVO_VIAJES)



def guardar_viajes(viajes: list[dict]) -> None:

    guardar_archivo(ARCHIVO_VIAJES, viajes)



def normalizar_fecha(fecha: str) -> str:

    try:
        return datetime.strptime(fecha.strip(), "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        raise ValueError("La fecha no es válida (formato AAAA-MM-DD)")



def normalizar_hora(hora: str) -> str:

    try:
        return datetime.strptime(hora.strip(), "%H:%M").strftime("%H:%M")
    except ValueError:
        raise ValueError("La hora no es válida (formato HH:MM)")



def buscar_viaje(viajes: list[dict], id_viaje: int) -> dict:

    for viaje in viajes:
        if viaje["id_viaje"] == id_viaje:
            return viaje
    raise ValueError("No existe un viaje con ese ID")



def bus_disponible(bus: dict) -> bool:

    estado = bus["estado"]
    if isinstance(estado, bool):
        return estado
    return str(estado).strip().lower() == "disponible"



def validar_extremos(ciudades: list[dict], id_origen: int, id_destino: int) -> None:

    pos_origen = obtener_posicion(ciudades, id_origen)
    pos_destino = obtener_posicion(ciudades, id_destino)

    if pos_origen == pos_destino:
        raise ValueError("El origen y el destino no pueden ser iguales")

    if {pos_origen, pos_destino} != {0, SEGMENTOS_TOTALES}:
        raise ValueError("Solo se programan viajes Concepción-Santiago o Santiago-Concepción")



def programar_viaje(viajes: list[dict], buses: list[dict], ciudades: list[dict], id_bus: int,
                    fecha: str, hora: str, id_origen: int, id_destino: int,
                    tarifa_base: int = TARIFA_BASE_DEFECTO) -> dict:

    bus = buscar_bus(buses, id_bus)
    if not bus_disponible(bus):
        raise ValueError("El bus no está disponible")

    fecha = normalizar_fecha(fecha)
    hora = normalizar_hora(hora)
    validar_extremos(ciudades, id_origen, id_destino)

    if tarifa_base <= 0:
        raise ValueError("La tarifa base debe ser mayor que cero")


    for viaje in viajes:
        if viaje["id_bus"] == id_bus and viaje["fecha"] == fecha and viaje["hora"] == hora:
            raise ValueError("El bus ya tiene un viaje programado en esa fecha y hora")

    nuevo_viaje = {
        "id_viaje": siguiente_id(viajes, "id_viaje"),
        "id_bus": id_bus,
        "fecha": fecha,
        "hora": hora,
        "id_origen": id_origen,
        "id_destino": id_destino,
        "tarifa_base": tarifa_base
    }
    viajes.append(nuevo_viaje)
    return nuevo_viaje



def obtener_sentido(ciudades: list[dict], viaje: dict) -> int:

    pos_origen = obtener_posicion(ciudades, viaje["id_origen"])
    pos_destino = obtener_posicion(ciudades, viaje["id_destino"])
    if pos_destino > pos_origen:
        return 1
    return -1



def obtener_capacidad_viaje(viajes: list[dict], buses: list[dict], id_viaje: int) -> int:

    viaje = buscar_viaje(viajes, id_viaje)
    bus = buscar_bus(buses, viaje["id_bus"])
    return bus["capacidad"]