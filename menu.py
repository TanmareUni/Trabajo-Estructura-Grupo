from colorama import init, Fore

# Aquí van las importaciones de los otros módulos del proyecto
# from reportes import generar_nomina_viaje
# import clientes, buses, viajes, ventas, archivos

init(autoreset=True)


def titulo(texto: str) -> None:
    print(f"\n{Fore.CYAN}=== {texto} ===")


def ok(msg: str) -> None:
    print(f"{Fore.GREEN}{msg}")


def error(msg: str) -> None:
    print(f"{Fore.RED}Error: {msg}")


def aviso(msg: str) -> None:
    print(f"{Fore.YELLOW}Advertencia: {msg}")


def mostrar_tabla_nomina(nomina: list[dict[str, str | int]]) -> None:
    if len(nomina) == 0:
        aviso("Este viaje aún no tiene pasajeros vigentes.")
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


def menu_clientes() -> None:
    while True:
        titulo("CLIENTES")
        print("1. Registrar cliente")
        print("2. Ver lista de clientes")
        print("3. Buscar cliente")
        print("0. Volver")

        op= input("\nOpción: ").strip()

        if op == "1":
            pass
        elif op == "2":
            pass
        elif op == "3":
            pass
        elif op == "0":
            break
        else:
            error("esa opción no existe.")


def menu_flota_viajes() -> None:
    while True:
        titulo("BUSES Y VIAJES")
        print("1. Registrar bus")
        print("2. Ver buses")
        print("3. Ver ciudades del recorrido")
        print("4. Programar viaje")
        print("5. Ver viajes programados")
        print("0. Volver")

        op= input("\nOpción: ").strip()

        if op == "1":
            pass
        elif op == "2":
            pass
        elif op == "3":
            pass
        elif op == "4":
            pass
        elif op == "5":
            pass
        elif op == "0":
            break
        else:
            error("esa opción no existe.")


def menu_pasajes() -> None:
    while True:
        titulo("PASAJES")
        print("1. Comprar pasaje")
        print("2. Anular pasaje")
        print("0. Volver")

        op= input("\nOpción: ").strip()

        if op == "1":
            pass
        elif op == "2":
            pass
        elif op == "0":
            break
        else:
            error("esa opción no existe.")


def menu_reportes() -> None:
    while True:
        titulo("NÓMINAS Y REPORTES")
        print("1. Nómina de pasajeros por viaje")
        print("2. Ver todos los pasajes de un viaje (vigentes y anulados)")
        print("3. Total recaudado en un viaje")
        print("4. Ver asientos libres y ocupados por tramo")
        print("0. Volver")

        op= input("\nOpción: ").strip()

        if op == "1":
            id_viaje = input("ID del viaje: ").strip()
            print("\n¿Cómo quieres ordenar la lista?")
            print("a) Por apellido paterno")
            print("b) Por nombres")
            print("c) Por número de asiento")
            criterio = input("Elige (a/b/c): ").strip().lower()

            try:
                if criterio not in ("a", "b", "c"):
                    raise ValueError("tienes que elegir a, b o c.")
                
                
                pass
            except ValueError as err:
                error(str(err))
            except Exception as err:
                error(f"no se pudo generar la nómina ({err})")

        elif op == "2":
            pass
        elif op == "3":
            pass
        elif op == "4":
            pass
        elif op == "0":
            break
        else:
            error("esa opción no existe.")


def main() -> None:
    while True:
        titulo("RUTASUR TRANSPORTES")
        print("1. Clientes")
        print("2. Buses, ciudades y viajes")
        print("3. Venta y anulación de pasajes")
        print("4. Nóminas y reportes")
        print("0. Salir")


        op= input("\nElige una opción: ").strip()

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
                error("ingresa un número del 0 al 4.")

  


if __name__ == "__main__":
    main()