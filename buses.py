#Modulo buses registrar, listar y consultar buses (RF02)
#Los buses se guardan en buses.json y se relacionan con los viajes por id_bus

from archivos import leer_archivo, guardar_archivo, siguiente_id

ARCHIVO_BUSES = "buses.json"
ESTADOS_BUS = ["disponible", "no disponible"]


#1 Cargar buses lee el archivo (lista vacía si no existe)
def cargar_buses() -> list[dict]:
    return leer_archivo(ARCHIVO_BUSES)


#2 Guardar buses escribe la lista completa en el archivo
def guardar_buses(buses: list[dict]) -> None:
    guardar_archivo(ARCHIVO_BUSES, buses)


#3 Normalizar patente sin espacios ni guiones y en mayuscula (ej: AB1234)
def normalizar_patente(patente: str) -> str:
    return patente.replace("-", "").replace(" ", "").upper()


#4 Registrar bus valida los datos y agrega el bus a la lista
def registrar_bus(buses: list[dict], patente: str, capacidad: int, estado: str) -> dict:
    if patente.strip() == "":
        raise ValueError("La patente no puede estar vacia")

    patente = normalizar_patente(patente)
    if len(patente) != 6 or not patente.isalnum():
        raise ValueError("La patente debe tener 6 letras o números (ej: AB1234)")

    if capacidad <= 0:
        raise ValueError("La capacidad debe ser un numero entero positivo")

    estado = estado.strip().lower()
    if estado not in ESTADOS_BUS:
        raise ValueError("El estado debe ser 'disponible' o 'no disponible'")

    for bus in buses:
        if bus["patente"] == patente:
            raise ValueError("Ya existe un bus con esa patente")

    nuevo_bus = {
        "id_bus": siguiente_id(buses, "id_bus"),
        "patente": patente,
        "capacidad": capacidad,
        "estado": estado
    }
    buses.append(nuevo_bus)
    return nuevo_bus


#5 Buscar bus por id se usa al programar un viaje
def buscar_bus(buses: list[dict], id_bus: int) -> dict:
    for bus in buses:
        if bus["id_bus"] == id_bus:
            return bus
    raise ValueError("No existe un bus con ese ID")


#6 Buscar bus por patente
def buscar_bus_por_patente(buses: list[dict], patente: str) -> dict:
    patente = normalizar_patente(patente)
    for bus in buses:
        if bus["patente"] == patente:
            return bus
    raise ValueError("No existe un bus con esa patente")
