def _va_despues(p1: dict, p2: dict, criterio: str) -> bool:
    if criterio == "a":
        c1 = (
            str(p1["apellido_paterno"]).lower(),
            str(p1["apellido_materno"]).lower(),
            str(p1["nombres"]).lower(),
        )
        c2 = (
            str(p2["apellido_paterno"]).lower(),
            str(p2["apellido_materno"]).lower(),
            str(p2["nombres"]).lower(),
        )
        return c1 > c2

    elif criterio == "b":
        c1 = (
            str(p1["nombres"]).lower(),
            str(p1["apellido_paterno"]).lower(),
            str(p1["apellido_materno"]).lower(),
        )
        c2 = (
            str(p2["nombres"]).lower(),
            str(p2["apellido_paterno"]).lower(),
            str(p2["apellido_materno"]).lower(),
        )
        return c1 > c2

    else: 
        c1 = (int(p1["asiento"]), int(p1["posicion_origen"]))
        c2 = (int(p2["asiento"]), int(p2["posicion_origen"]))
        return c1 > c2


def ordenar_bubble_sort(lista: list[dict], criterio: str) -> list[dict]:
    copia = lista[:]
    n = len(copia)

    for i in range(n):
        cambio = False
        for j in range(0, n - i - 1):
            if _va_despues(copia[j], copia[j + 1], criterio):
                copia[j], copia[j + 1] = copia[j + 1], copia[j]
                cambio = True
        if not cambio:
            break

    return copia


def generar_nomina_viaje(
    id_viaje: str,
    pasajes: list[dict],
    clientes: list[dict],
    ciudades: list[dict],
    criterio: str = "c",
) -> list[dict]:
    if criterio not in ("a", "b", "c"):
        raise ValueError("criterio inválido. Elige a, b o c.")

    dict_clientes = {str(c["id_cliente"]): c for c in clientes}
    dict_ciudades = {str(ciu["id_ciudad"]): ciu for ciu in ciudades}

    nomina = []

    for p in pasajes:
        if str(p["id_viaje"]) == str(id_viaje) and str(p["estado"]).lower() == "vigente":
            cli = dict_clientes.get(str(p["id_cliente"]))
            ori = dict_ciudades.get(str(p["id_origen"]))
            des = dict_ciudades.get(str(p["id_destino"]))

            if cli and ori and des:
                nomina.append(
                    {
                        "asiento": int(p["asiento"]),
                        "apellido_paterno": str(cli["apellido_paterno"]),
                        "apellido_materno": str(cli["apellido_materno"]),
                        "nombres": str(cli["nombres"]),
                        "ciudad_embarque": str(ori["nombre"]),
                        "ciudad_destino": str(des["nombre"]),
                        "posicion_origen": int(ori["posicion"]),
                    }
                )

    return ordenar_bubble_sort(nomina, criterio)


def obtener_pasajes_viaje(
    id_viaje: str,
    pasajes: list[dict],
    clientes: list[dict],
    ciudades: list[dict],
) -> list[dict]:
    dict_clientes = {str(c["id_cliente"]): c for c in clientes}
    dict_ciudades = {str(ciu["id_ciudad"]): ciu for ciu in ciudades}

    lista = []

    for p in pasajes:
        if str(p["id_viaje"]) == str(id_viaje):
            cli = dict_clientes.get(str(p["id_cliente"]))
            ori = dict_ciudades.get(str(p["id_origen"]))
            des = dict_ciudades.get(str(p["id_destino"]))

            nombre = f"{cli['nombres']} {cli['apellido_paterno']}" if cli else "Sin datos"
            lista.append(
                {
                    "id_pasaje": str(p["id_pasaje"]),
                    "asiento": int(p["asiento"]),
                    "pasajero": nombre,
                    "origen": str(ori["nombre"]) if ori else str(p["id_origen"]),
                    "destino": str(des["nombre"]) if des else str(p["id_destino"]),
                    "valor": int(p["valor"]),
                    "estado": str(p["estado"]).lower(),
                }
            )

    return lista


def calcular_recaudacion_viaje(id_viaje: str, pasajes: list[dict]) -> int:
    total = 0
    for p in pasajes:
        if str(p["id_viaje"]) == str(id_viaje) and str(p["estado"]).lower() == "vigente":
            total += int(p["valor"])
    return total


def consultar_ocupacion_tramo(
    id_viaje: str,
    id_origen_tramo: str,
    id_destino_tramo: str,
    viajes: list[dict],
    buses: list[dict],
    ciudades: list[dict],
    pasajes: list[dict],
) -> dict:
    viaje_encontrado = None
    for v in viajes:
        if str(v["id_viaje"]) == str(id_viaje):
            viaje_encontrado = v
            break

    if viaje_encontrado is None:
        raise ValueError("ese viaje no existe.")

    bus_encontrado = None
    for b in buses:
        if str(b["id_bus"]) == str(viaje_encontrado["id_bus"]):
            bus_encontrado = b
            break

    if bus_encontrado is None:
        raise ValueError("no se encontró el bus de este viaje.")

    posiciones = {str(c["id_ciudad"]): int(c["posicion"]) for c in ciudades}

    if str(id_origen_tramo) not in posiciones or str(id_destino_tramo) not in posiciones:
        raise ValueError("alguna de las ciudades ingresadas no existe.")

    pos_ori = posiciones[str(id_origen_tramo)]
    pos_des = posiciones[str(id_destino_tramo)]

    if pos_ori == pos_des:
        raise ValueError("el origen y el destino no pueden ser iguales.")

    inicio_req = min(pos_ori, pos_des)
    fin_req = max(pos_ori, pos_des)

    ocupados_set = set()

    for p in pasajes:
        if str(p["id_viaje"]) == str(id_viaje) and str(p["estado"]).lower() == "vigente":
            p_ori = posiciones[str(p["id_origen"])]
            p_des = posiciones[str(p["id_destino"])]
            inicio_p = min(p_ori, p_des)
            fin_p = max(p_ori, p_des)

            if inicio_req < fin_p and inicio_p < fin_req:
                ocupados_set.add(int(p["asiento"]))

    capacidad = int(bus_encontrado["capacidad"])
    ocupados = []
    libres = []

    for asiento in range(1, capacidad + 1):
        if asiento in ocupados_set:
            ocupados.append(asiento)
        else:
            libres.append(asiento)

    return {
        "capacidad": capacidad,
        "ocupados": ocupados,
        "libres": libres,
    }