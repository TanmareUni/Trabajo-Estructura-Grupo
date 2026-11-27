# Menu principal del sistema RutaSur
# Une el menu de clientes y buses (parte A) con viajes y pasajes (parte B) y nominas y reportes (parte C)

from os import system
system("cls")

from colorama import Fore
from consola import titulo, ok, error, aviso
from clientes import (cargar_clientes, guardar_clientes, registrar_cliente, buscar_cliente, buscar_cliente_por_rut)
from buses import (cargar_buses, guardar_buses, registrar_bus, buscar_bus, buscar_bus_por_patente)
from ciudades import cargar_ciudades
from viajes import cargar_viajes, buscar_viaje
from pasajes import cargar_pasajes
from integracion_menu import (mostrar_ciudades, accion_programar_viaje, accion_listar_viajes,accion_comprar_pasaje, accion_anular_pasaje)
from reportes import (generar_nomina_viaje, obtener_pasajes_viaje, calcular_recaudacion_viaje, consultar_ocupacion_tramo)


#Texto de un cliente en una sola linea
def texto_cliente(cliente: dict) -> str:
    return (f"{cliente['id_cliente']} - {cliente['rut']} - {cliente['nombres']} "
            f"{cliente['apellido_paterno']} {cliente['apellido_materno']} - {cliente['contacto']}")


#Texto de un bus en una sola linea
def texto_bus(bus: dict) -> str:
    return f"{bus['id_bus']} - {bus['patente']} - {bus['capacidad']} asientos - {bus['estado']}"


#Pedir el ID de un viaje y comprobar que exista
def pedir_viaje() -> int:
    try:
        id_viaje = int(input("ID del viaje: ").strip())
    except ValueError:
        raise ValueError("el ID del viaje debe ser un numero entero")
    buscar_viaje(cargar_viajes(), id_viaje)
    return id_viaje


def mostrar_tabla_nomina(nomina: list[dict]) -> None:
    if len(nomina) == 0:
        aviso("Este viaje aun no tiene pasajeros vigentes.")
        return

    print(
        f"\n{Fore.CYAN}"
        f"{'Asiento':<8} | {'Ap. Paterno':<15} | {'Ap. Materno':<15} | "
        f"{'Nombres':<18} | {'Sube en':<12} | {'Baja en':<12}"
    )
    print(f"{Fore.CYAN}{'-' * 90}")

    for fila in nomina:
        print(
            f"{str(fila['asiento']):<8} | "
            f"{fila['apellido_paterno']:<15} | "
            f"{fila['apellido_materno']:<15} | "
            f"{fila['nombres']:<18} | "
            f"{fila['ciudad_embarque']:<12} | "
            f"{fila['ciudad_destino']:<12}"
        )


def mostrar_pasajes_viaje(lista_pasajes: list[dict]) -> None:
    if len(lista_pasajes) == 0:
        aviso("No hay pasajes registrados para este viaje.")
        return
    print(
        f"\n{Fore.CYAN}"
        f"{'ID':<8} | {'Asiento':<8} | {'Pasajero':<26} | "
        f"{'Origen':<12} | {'Destino':<12} | {'Valor':<10} | {'Estado':<10}"
    )
    print(f"{Fore.CYAN}{'-' * 98}")

    for p in lista_pasajes:
        #vigentes en verde y anulados en rojo
        color = Fore.GREEN if p["estado"] == "vigente" else Fore.RED
        print(
            f"{color}{p['id_pasaje']:<8} | {str(p['asiento']):<8} | {p['pasajero']:<26} | "
            f"{p['origen']:<12} | {p['destino']:<12} | {str(p['valor']):<10} | {p['estado']:<10}"
        )


def menu_clientes() -> None:
    while True:
        titulo("CLIENTES")
        print("1. Registrar cliente")
        print("2. Ver lista de clientes")
        print("3. Buscar cliente por ID")
        print("4. Buscar cliente por RUT")
        print("0. Volver")

        op = input("\nOpcion: ").strip()

        if op == "1":
            rut = input("RUT: ")
            nombres = input("Nombres: ")
            apellido_paterno = input("Apellido paterno: ")
            apellido_materno = input("Apellido materno: ")
            contacto = input("Contacto: ")
            try:
                clientes = cargar_clientes()
                cliente = registrar_cliente(clientes, rut, nombres, apellido_paterno, apellido_materno, contacto)
                guardar_clientes(clientes)
                ok(f"Cliente registrado con ID {cliente['id_cliente']}.")
            except ValueError as e:
                error(str(e))

        elif op == "2":
            try:
                clientes = cargar_clientes()
                if len(clientes) == 0:
                    aviso("No hay clientes registrados.")
                else:
                    for cliente in clientes:
                        print(texto_cliente(cliente))
            except ValueError as e:
                error(str(e))

        elif op == "3":
            #conversion del ID (falla si escribe texto)
            try:
                id_cliente = int(input("ID del cliente: "))
            except ValueError:
                error("el ID debe ser un numero entero")
            else:
                try:
                    cliente = buscar_cliente(cargar_clientes(), id_cliente)
                    print(texto_cliente(cliente))
                except ValueError as e:
                    error(str(e))

        elif op == "4":
            rut = input("RUT a buscar: ")
            try:
                cliente = buscar_cliente_por_rut(cargar_clientes(), rut)
                print(texto_cliente(cliente))
            except ValueError as e:
                error(str(e))

        elif op == "0":
            break
        else:
            error("esa opcion no existe.")


def menu_flota_viajes() -> None:
    while True:
        titulo("BUSES Y VIAJES")
        print("1. Registrar bus")
        print("2. Ver buses")
        print("3. Ver ciudades del recorrido")
        print("4. Programar viaje")
        print("5. Ver viajes programados")
        print("6. Buscar bus por ID")
        print("7. Buscar bus por patente")
        print("0. Volver")

        op = input("\nOpcion: ").strip()

        if op == "1":
            patente = input("Patente (ej: AB1234): ")
            estado = input("Estado (disponible / no disponible): ")
            #conversion de la capacidad (falla si escribe texto)
            try:
                capacidad = int(input("Capacidad (cantidad de asientos): "))
            except ValueError:
                error("la capacidad debe ser un numero entero")
            else:
                #validaciones de la funcion (raise ValueError)
                try:
                    buses = cargar_buses()
                    bus = registrar_bus(buses, patente, capacidad, estado)
                    guardar_buses(buses)
                    ok(f"Bus registrado con ID {bus['id_bus']}.")
                except ValueError as e:
                    error(str(e))

        elif op == "2":
            try:
                buses = cargar_buses()
                if len(buses) == 0:
                    aviso("No hay buses registrados.")
                else:
                    for bus in buses:
                        print(texto_bus(bus))
            except ValueError as e:
                error(str(e))

        elif op == "3":
            try:
                for ciudad in cargar_ciudades():
                    print(f"{ciudad['id_ciudad']} - {ciudad['nombre']} (posicion {ciudad['posicion']})")
            except ValueError as e:
                error(str(e))

        elif op == "4":
            accion_programar_viaje()

        elif op == "5":
            accion_listar_viajes()

        elif op == "6":
            try:
                id_bus = int(input("ID del bus: "))
            except ValueError:
                error("el ID debe ser un numero entero")
            else:
                try:
                    bus = buscar_bus(cargar_buses(), id_bus)
                    print(texto_bus(bus))
                except ValueError as e:
                    error(str(e))

        elif op == "7":
            patente = input("Patente a buscar: ")
            try:
                bus = buscar_bus_por_patente(cargar_buses(), patente)
                print(texto_bus(bus))
            except ValueError as e:
                error(str(e))

        elif op == "0":
            break
        else:
            error("esa opcion no existe.")


def menu_pasajes() -> None:
    while True:
        titulo("PASAJES")
        print("1. Comprar pasaje")
        print("2. Anular pasaje")
        print("0. Volver")

        op = input("\nOpcion: ").strip()

        if op == "1":
            accion_comprar_pasaje()
        elif op == "2":
            accion_anular_pasaje()
        elif op == "0":
            break
        else:
            error("esa opcion no existe.")


def menu_reportes() -> None:
    while True:
        titulo("NOMINAS Y REPORTES")
        print("1. Nomina de pasajeros por viaje")
        print("2. Ver todos los pasajes de un viaje (vigentes y anulados)")
        print("3. Total recaudado en un viaje")
        print("4. Ver asientos libres y ocupados por tramo")
        print("0. Volver")

        op = input("\nOpcion: ").strip()

        if op == "1":
            try:
                id_viaje = pedir_viaje()
                print("\nComo quieres ordenar la lista?")
                print("a) Por apellido paterno")
                print("b) Por nombres")
                print("c) Por numero de asiento")
                criterio = input("Elige (a/b/c): ").strip().lower()

                nomina = generar_nomina_viaje(id_viaje, cargar_pasajes(), cargar_clientes(), cargar_ciudades(), criterio)
                mostrar_tabla_nomina(nomina)
            except ValueError as err:
                error(str(err))

        elif op == "2":
            try:
                id_viaje = pedir_viaje()
                lista = obtener_pasajes_viaje(id_viaje, cargar_pasajes(), cargar_clientes(), cargar_ciudades())
                mostrar_pasajes_viaje(lista)
            except ValueError as err:
                error(str(err))

        elif op == "3":
            try:
                id_viaje = pedir_viaje()
                total = calcular_recaudacion_viaje(id_viaje, cargar_pasajes())
                ok(f"Recaudacion vigente del viaje {id_viaje}: ${total} CLP")
            except ValueError as err:
                error(str(err))

        elif op == "4":
            try:
                id_viaje = pedir_viaje()
                ciudades = cargar_ciudades()
                mostrar_ciudades(ciudades)
                id_origen = input("ID ciudad de origen del tramo: ").strip()
                id_destino = input("ID ciudad de destino del tramo: ").strip()

                info = consultar_ocupacion_tramo(id_viaje, id_origen, id_destino, cargar_viajes(), cargar_buses(), ciudades, cargar_pasajes())
                titulo(f"OCUPACION DEL TRAMO (CAPACIDAD: {info['capacidad']})")
                print(f"{Fore.RED}Ocupados ({len(info['ocupados'])}): {info['ocupados']}")
                print(f"{Fore.GREEN}Libres ({len(info['libres'])}): {info['libres']}")
            except ValueError as err:
                error(str(err))

        elif op == "0":
            break
        else:
            error("esa opcion no existe.")


def main() -> None:
    while True:
        titulo("RUTASUR TRANSPORTES")
        print("1. Clientes")
        print("2. Buses, ciudades y viajes")
        print("3. Venta y anulacion de pasajes")
        print("4. Nominas y reportes")
        print("0. Salir")

        op = input("\nElige una opcion: ").strip()

        if op == "1":
            menu_clientes()
        elif op == "2":
            menu_flota_viajes()
        elif op == "3":
            menu_pasajes()
        elif op == "4":
            menu_reportes()
        elif op == "0":
            ok("Saliendo del sistema...")
            break
        else:
            error("ingresa un numero del 0 al 4.")


if __name__ == "__main__":
    main()
