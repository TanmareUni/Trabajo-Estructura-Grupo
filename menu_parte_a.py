
from os import system
system("cls")

from clientes import (cargar_clientes, guardar_clientes, registrar_cliente,
                buscar_cliente, buscar_cliente_por_rut)

clientes = cargar_clientes()

while True:
    print("\n Menu de Opciones")
    print("Clientes")
    print("------------------------------------")
    print("1.Registrar cliente")
    print("2.Listar clientes")
    print("3.Buscar cliente por ID")
    print("4.Buscar cliente por RUT")
    print("5.Salir")
    print("------------------------------------")
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
        print("\nLISTA DE CLIENTES")
        if len(clientes) == 0:
            print("No hay clientes registrados")
        else:
            for cliente in clientes:
                print(f"{cliente['id_cliente']} - {cliente['rut']} - {cliente['nombres']} "
                    f"{cliente['apellido_paterno']} {cliente['apellido_materno']} - {cliente['contacto']}")

    elif opcion == "3":
        # primer try conversión del ID (int() falla si escribe texto)
        try:
            id_cliente = int(input("ID del cliente: "))
        except ValueError:
            print("Error el ID debe ser un número entero")
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
        print("\nPrograma finalizado.")
        break

    else:
        print("\nOpción invalida.")