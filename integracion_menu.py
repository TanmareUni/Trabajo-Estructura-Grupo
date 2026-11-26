from asientos import ocupacion_por_tramo, obtener_tramo
from buses import cargar_buses
from ciudades import cargar_ciudades
from clientes import cargar_clientes
from pasajes import (cargar_pasajes, guardar_pasajes, registrar_pasaje, anular_pasaje,
                     obtener_pasajes_viaje, calcular_recaudacion)
from viajes import (cargar_viajes, guardar_viajes, programar_viaje, buscar_viaje,
                    obtener_capacidad_viaje, TARIFA_BASE_DEFECTO)


def leer_entero(texto: str) -> int:
    try:
        return int(input(texto).strip())
    except ValueError:
        raise ValueError("debes ingresar un número entero.")


def mostrar_ciudades(ciudades: list[dict]) -> None:
    for ciudad in ciudades:
        print(f"  {ciudad['id_ciudad']}. {ciudad['nombre']}")


#menu_flota_viajes opción 4
def accion_programar_viaje() -> None:
    try:
        viajes = cargar_viajes()
        ciudades = cargar_ciudades()
        id_bus = leer_entero("ID del bus: ")
        fecha = input("Fecha (AAAA-MM-DD): ")
        hora = input("Hora (HH:MM): ")
        mostrar_ciudades(ciudades)
        id_origen = leer_entero("ID ciudad inicial: ")
        id_destino = leer_entero("ID ciudad final: ")
        texto_tarifa = input(f"Tarifa base (Enter = {TARIFA_BASE_DEFECTO}): ").strip()
        tarifa = int(texto_tarifa) if texto_tarifa != "" else TARIFA_BASE_DEFECTO

        viaje = programar_viaje(viajes, cargar_buses(), ciudades, id_bus, fecha, hora,
                                id_origen, id_destino, tarifa)
        guardar_viajes(viajes)
        ok(f"Viaje programado con ID {viaje['id_viaje']}.")
    except ValueError as err:
        error(str(err))


#menu_flota_viajes opción 5
def accion_listar_viajes() -> None:
    try:
        viajes = cargar_viajes()
        if len(viajes) == 0:
            aviso("No hay viajes programados.")
            return
        nombres = {c["id_ciudad"]: c["nombre"] for c in cargar_ciudades()}
        for v in viajes:
            print(f"{v['id_viaje']} - Bus {v['id_bus']} - {v['fecha']} {v['hora']} - "
                  f"{nombres[v['id_origen']]} -> {nombres[v['id_destino']]} - ${v['tarifa_base']}")
    except ValueError as err:
        error(str(err))


#menu_pasajes opción 1
def accion_comprar_pasaje() -> None:
    try:
        pasajes = cargar_pasajes()
        ciudades = cargar_ciudades()
        id_cliente = leer_entero("ID del cliente: ")
        id_viaje = leer_entero("ID del viaje: ")
        mostrar_ciudades(ciudades)
        id_origen = leer_entero("ID ciudad de embarque: ")
        id_destino = leer_entero("ID ciudad de destino: ")
        asiento = leer_entero("Número de asiento: ")

        pasaje = registrar_pasaje(pasajes, cargar_clientes(), cargar_viajes(), cargar_buses(),
                                  ciudades, id_cliente, id_viaje, id_origen, id_destino, asiento)
        guardar_pasajes(pasajes)
        ok(f"Pasaje {pasaje['id_pasaje']} registrado. Valor: ${pasaje['valor']}")
    except ValueError as err:
        error(str(err))


#menu_pasajes opción 2
def accion_anular_pasaje() -> None:
    try:
        pasajes = cargar_pasajes()
        anulado = anular_pasaje(pasajes, leer_entero("ID del pasaje a anular: "))
        guardar_pasajes(pasajes)
        ok(f"Pasaje {anulado['id_pasaje']} anulado. El asiento {anulado['asiento']} quedó libre en su tramo.")
    except ValueError as err:
        error(str(err))


#menu_reportes opción 2
def accion_pasajes_de_viaje() -> None:
    try:
        id_viaje = leer_entero("ID del viaje: ")
        buscar_viaje(cargar_viajes(), id_viaje)
        nombres = {c["id_ciudad"]: c["nombre"] for c in cargar_ciudades()}
        lista = obtener_pasajes_viaje(cargar_pasajes(), id_viaje)
        if len(lista) == 0:
            aviso("Este viaje no tiene pasajes.")
            return
        for p in lista:
            print(f"{p['id_pasaje']} - Asiento {p['asiento']} - Cliente {p['id_cliente']} - "
                  f"{nombres[p['id_origen']]} -> {nombres[p['id_destino']]} - ${p['valor']} - {p['estado'].upper()}")
    except ValueError as err:
        error(str(err))


#menu_reportes opción 3
def accion_recaudacion() -> None:
    try:
        id_viaje = leer_entero("ID del viaje: ")
        buscar_viaje(cargar_viajes(), id_viaje)
        ok(f"Recaudación vigente del viaje {id_viaje}: ${calcular_recaudacion(cargar_pasajes(), id_viaje)}")
    except ValueError as err:
        error(str(err))


#menu_reportes opción 4
def accion_ocupacion_tramo() -> None:
    try:
        ciudades = cargar_ciudades()
        id_viaje = leer_entero("ID del viaje: ")
        capacidad = obtener_capacidad_viaje(cargar_viajes(), cargar_buses(), id_viaje)
        mostrar_ciudades(ciudades)
        tramo = obtener_tramo(ciudades, leer_entero("ID ciudad de embarque: "), leer_entero("ID ciudad de destino: "))
        if tramo[0] == tramo[1]:
            raise ValueError("El origen y el destino no pueden ser iguales")
        datos = ocupacion_por_tramo(cargar_pasajes(), ciudades, id_viaje, capacidad, tramo)
        print(f"Ocupados ({len(datos['ocupados'])}): {datos['ocupados']}")
        print(f"Libres ({len(datos['libres'])}): {datos['libres']}")
    except ValueError as err:
        error(str(err))
