# Menú temporal para probar la parte A (clientes, buses y ciudades)
# Más adelante se reemplaza por el menú principal del grupo

from os import system
system("cls")

from clientes import (cargar_clientes, guardar_clientes, registrar_cliente,
            buscar_cliente, buscar_cliente_por_rut)
from buses import (cargar_buses, guardar_buses, registrar_bus,
            buscar_bus, buscar_bus_por_patente)
from ciudades import cargar_ciudades

clientes = cargar_clientes()
buses = cargar_buses()
ciudades = cargar_ciudades()

while True:
    print("\n----------------------------------")
    print(" - RUTASUR - ")
    print("----------------------------------")
    print("1.Registrar cliente")
    print("2.Listar clientes")
    print("3.Buscar cliente por ID")
    print("4.Buscar cliente por RUT")
    print("5.Registrar bus")
    print("6.Listar buses")
    print("7.Buscar bus por ID")
    print("8.Buscar bus por patente")
    print("9.Consultar ciudades")
    print("10.Salir")
    print("----------------------------------")
    opcion = input("Seleccione una opcion: ")

    if opcion == "1":
        rut = input("RUT: ")
        nombres = input("Nombres: ")
        apellido_paterno = input("Apellido paterno: ")
        apellido_materno = input("Apellido materno: ")
        contacto = input("Contacto: ")
        try:
            cliente = registrar_cliente(clientes, rut, nombres, apellido_paterno, apellido_materno, contacto)
            guardar_clientes(clientes)
            print(f"Cliente registrado con ID {cliente['id_cliente']}.")
        except ValueError as e:
            print(f"Error: {e}")

    elif opcion == "2":
        print("\n Lista de Clientes ")
        if len(clientes) == 0:
            print("No hay clientes registrados")
        else:
            for cliente in clientes:
                print(f"{cliente['id_cliente']} - {cliente['rut']} - {cliente['nombres']} "
                f"{cliente['apellido_paterno']} {cliente['apellido_materno']} - {cliente['contacto']}")

    elif opcion == "3":
        #primer try conversión del ID (int falla si escribe texto)
        try:
            id_cliente = int(input("ID del cliente: "))
        except ValueError:
            print("Error el ID debe ser un numero entero")
        else:
            try:
                cliente = buscar_cliente(clientes, id_cliente)
                print(f"{cliente['id_cliente']} - {cliente['rut']} - {cliente['nombres']} "
                f"{cliente['apellido_paterno']} {cliente['apellido_materno']} - {cliente['contacto']}")
            except ValueError as e:
                print(f"Error: {e}")

    elif opcion == "4":
        rut = input("RUT a buscar: ")
        try:
            cliente = buscar_cliente_por_rut(clientes, rut)
            print(f"{cliente['id_cliente']} - {cliente['rut']} - {cliente['nombres']} "
            f"{cliente['apellido_paterno']} {cliente['apellido_materno']} - {cliente['contacto']}")
        except ValueError as e:
            print(f"Error: {e}")

    elif opcion == "5":
        patente = input("Patente (ej: AB1234): ")
        estado = input("Estado (disponible / no disponible): ")
        #primer try conversion de la capacidad (int falla si escribe texto)
        try:
            capacidad = int(input("Capacidad (cantidad de asientos): "))
        except ValueError:
            print("Error la capacidad debe ser un numero entero")
        else:
            #segundo try validaciones de la funcion (raise ValueError)
            try:
                bus = registrar_bus(buses, patente, capacidad, estado)
                guardar_buses(buses)
                print(f"Bus registrado con ID {bus['id_bus']}.")
            except ValueError as e:
                print(f"Error: {e}")

    elif opcion == "6":
        print("\n Lista de Buses ")
        if len(buses) == 0:
            print("No hay buses registrados")
        else:
            for bus in buses:
                print(f"{bus['id_bus']} - {bus['patente']} - {bus['capacidad']} asientos - {bus['estado']}")

    elif opcion == "7":
        try:
            id_bus = int(input("ID del bus: "))
        except ValueError:
            print("Error el ID debe ser un numero entero")
        else:
            try:
                bus = buscar_bus(buses, id_bus)
                print(f"{bus['id_bus']} - {bus['patente']} - {bus['capacidad']} asientos - {bus['estado']}")
            except ValueError as e:
                print(f"Error: {e}")

    elif opcion == "8":
        patente = input("Patente a buscar: ")
        try:
            bus = buscar_bus_por_patente(buses, patente)
            print(f"{bus['id_bus']} - {bus['patente']} - {bus['capacidad']} asientos - {bus['estado']}")
        except ValueError as e:
            print(f"Error: {e}")

    elif opcion == "9":
        print("\nCiudades del Recorrido (sur a norte)")
        for ciudad in ciudades:
            print(f"{ciudad['posicion']} - {ciudad['nombre']}")

    elif opcion == "10":
        print("\nPrograma finalizado.")
        break

    else:
        print("\nOpción inválida.")
