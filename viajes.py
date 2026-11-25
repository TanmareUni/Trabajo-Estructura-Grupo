"""
Módulo viajes: programar y consultar viajes (RF04).
Los viajes se guardan en viajes.json y se relacionan con buses y ciudades por id_bus, id_origen e id_destino.
"""

from datetime import datetime

from archivos import leer_archivo, guardar_archivo, siguiente_id
from ciudades import obtener_posicion
from tarifas import SEGMENTOS_TOTALES

ARCHIVO_VIAJES = "viajes.json"
TARIFA_BASE_DEFECTO = 10000


#1 Cargar viajes lee el archivo (lista vacía si no existe)
def cargar_viajes() -> list[dict]:
#Retorna la lista de viajes guardados
    return leer_archivo(ARCHIVO_VIAJES)


#2 Guardar viajes escribe la lista completa en el archivo
def guardar_viajes(viajes: list[dict]) -> None:
#Guarda la lista de viajes en el archivo
    guardar_archivo(ARCHIVO_VIAJES, viajes)


#3 Normalizar fecha valida el formato AAAA-MM-DD y la deja con ceros (2026-01-05)
def normalizar_fecha(fecha: str) -> str:
#Retorna la fecha normalizada. Lanza ValueError si no existe o el formato es incorrecto
    try:
        return datetime.strptime(fecha.strip(), "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        raise ValueError("La fecha no es válida (formato AAAA-MM-DD)")


#4 Normalizar hora valida el formato HH:MM (24 horas)
def normalizar_hora(hora: str) -> str:
#Retorna la hora normalizada. Lanza ValueError si el formato es incorrecto
    try:
        return datetime.strptime(hora.strip(), "%H:%M").strftime("%H:%M")
    except ValueError:
        raise ValueError("La hora no es válida (formato HH:MM)")


#5 Buscar viaje por ID se usa al vender pasajes y al emitir reportes
def buscar_viaje(viajes: list[dict], id_viaje: int) -> dict:
#Retorna el viaje con ese ID. Lanza ValueError si no existe
    for viaje in viajes:
        if viaje["id_viaje"] == id_viaje:
            return viaje
    raise ValueError("No existe un viaje con ese ID")


#6 Buscar bus por ID busca en la lista de buses (la lee de buses.json el módulo buses)
def buscar_bus_por_id(buses: list[dict], id_bus: int) -> dict:
#Retorna el bus con ese ID. Lanza ValueError si no existe
    for bus in buses:
        if bus["id_bus"] == id_bus:
            return bus
    raise ValueError("No existe un bus con ese ID")


#7 Bus disponible acepta estado True/False o el texto "disponible"
def bus_disponible(bus: dict) -> bool:
#Retorna True si el bus está disponible para programar viajes
    estado = bus["estado"]
    if isinstance(estado, bool):
        return estado
    return str(estado).strip().lower() == "disponible"


#8 Validar extremos solo se permite Concepción-Santiago o Santiago-Concepción
def validar_extremos(ciudades: list[dict], id_origen: int, id_destino: int) -> None:
#Lanza ValueError si las ciudades no existen o no son los dos extremos del recorrido
    pos_origen = obtener_posicion(ciudades, id_origen)
    pos_destino = obtener_posicion(ciudades, id_destino)

    if pos_origen == pos_destino:
        raise ValueError("El origen y el destino no pueden ser iguales")

    if {pos_origen, pos_destino} != {0, SEGMENTOS_TOTALES}:
        raise ValueError("Solo se programan viajes Concepción-Santiago o Santiago-Concepción")


#9 Programar viaje valida los datos y agrega el viaje a la lista
def programar_viaje(viajes: list[dict], buses: list[dict], ciudades: list[dict], id_bus: int,
                    fecha: str, hora: str, id_origen: int, id_destino: int,
                    tarifa_base: int = TARIFA_BASE_DEFECTO) -> dict:
#Agrega un viaje nuevo y lo retorna. Lanza ValueError si algún dato no es válido
    bus = buscar_bus_por_id(buses, id_bus)
    if not bus_disponible(bus):
        raise ValueError("El bus no está disponible")

    fecha = normalizar_fecha(fecha)
    hora = normalizar_hora(hora)
    validar_extremos(ciudades, id_origen, id_destino)

    if tarifa_base <= 0:
        raise ValueError("La tarifa base debe ser mayor que cero")

    #un mismo bus no puede tener dos viajes a la misma fecha y hora
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


#10 Obtener sentido indica hacia dónde va el viaje (+1 de Concepción a Santiago, -1 al revés)
def obtener_sentido(ciudades: list[dict], viaje: dict) -> int:
#Retorna +1 si el viaje va hacia el norte (posiciones crecientes) o -1 si va hacia el sur
    pos_origen = obtener_posicion(ciudades, viaje["id_origen"])
    pos_destino = obtener_posicion(ciudades, viaje["id_destino"])
    if pos_destino > pos_origen:
        return 1
    return -1


#11 Obtener capacidad capacidad del bus asignado al viaje (para validar asientos)
def obtener_capacidad_viaje(viajes: list[dict], buses: list[dict], id_viaje: int) -> int:
#Retorna la capacidad del bus del viaje. Lanza ValueError si el viaje o el bus no existen
    viaje = buscar_viaje(viajes, id_viaje)
    bus = buscar_bus_por_id(buses, viaje["id_bus"])
    return bus["capacidad"]