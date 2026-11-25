"""
Módulo clientes: registrar, listar y buscar clientes (RF01).
Los clientes se guardan en clientes.json y se relacionan con los pasajes por id_cliente.
"""

from archivos import leer_archivo, guardar_archivo, siguiente_id

ARCHIVO_CLIENTES = "clientes.json"


#1 Cargar clientes lee el archivo (lista vacía si no existe)
def cargar_clientes() -> list[dict]:
#Retorna la lista de clientes guardados
    return leer_archivo(ARCHIVO_CLIENTES)


#2 Guardar clientes escribe la lista completa en el archivo
def guardar_clientes(clientes: list[dict]) -> None:
#Guarda la lista de clientes en el archivo
    guardar_archivo(ARCHIVO_CLIENTES, clientes)


#3 Normalizar RUT deja el RUT sin puntos ni espacios y con el guion (ej: 12345678-5)
def normalizar_rut(rut: str) -> str:
#Retorna el RUT limpio en mayuscula y con guion antes del dígito verificador
    limpio = rut.replace(".", "").replace("-", "").replace(" ", "").upper()
    if len(limpio) < 2:
        return limpio
    return limpio[:-1] + "-" + limpio[-1]


#4 Validar RUT revisa el formato y el dígito verificador (módulo 11)
def validar_rut(rut: str) -> None:
#Lanza ValueError si el RUT no es válido
    rut = normalizar_rut(rut)
    if "-" not in rut:
        raise ValueError("El RUT no es valido")

    cuerpo = rut.split("-")[0]
    digito = rut.split("-")[1]

    if not cuerpo.isdigit() or len(cuerpo) < 7:
        raise ValueError("El RUT no es valido")

    #se multiplica cada dígito (de derecha a izquierda) por 2,3,4,5,6,7,2,3...
    suma = 0
    multiplicador = 2
    for numero in reversed(cuerpo):
        suma += int(numero) * multiplicador
        multiplicador += 1
        if multiplicador > 7:
            multiplicador = 2

    resto = 11 - (suma % 11)
    if resto == 11:
        esperado = "0"
    elif resto == 10:
        esperado = "K"
    else:
        esperado = str(resto)

    if digito != esperado:
        raise ValueError("El RUT no es válido (dígito verificador incorrecto)")


#5 Registrar cliente valida los datos y agrega el cliente a la lista
def registrar_cliente(clientes: list[dict], rut: str, nombres: str, apellido_paterno: str,apellido_materno: str, contacto: str) -> dict:
#Agrega un cliente nuevo y lo retorna Lanza ValueError si algun dato no es válido
    if rut.strip() == "":
        raise ValueError("El RUT no puede estar vacio")
    
    if nombres.strip() == "":
        raise ValueError("Los nombres no pueden estar vacios")
    
    if apellido_paterno.strip() == "":
        raise ValueError("El apellido paterno no puede estar vacio")
    
    if apellido_materno.strip() == "":
        raise ValueError("El apellido materno no puede estar vacio")
    
    if contacto.strip() == "":
        raise ValueError("El contacto no puede estar vacio")

    validar_rut(rut)
    rut = normalizar_rut(rut)

    for cliente in clientes:
        if cliente["rut"] == rut:
            raise ValueError("Ya existe un cliente con ese RUT")

    nuevo_cliente = {
        "id_cliente": siguiente_id(clientes, "id_cliente"),
        "rut": rut,
        "nombres": nombres.strip(),
        "apellido_paterno": apellido_paterno.strip(),
        "apellido_materno": apellido_materno.strip(),
        "contacto": contacto.strip()
    }
    clientes.append(nuevo_cliente)
    return nuevo_cliente


#6 Buscar cliente por ID se usa al vender un pasaje
def buscar_cliente(clientes: list[dict], id_cliente: int) -> dict:
#Retorna el cliente con ese ID manda ValueError si no existe
    for cliente in clientes:
        if cliente["id_cliente"] == id_cliente:
            return cliente
    raise ValueError("No existe un cliente con ese ID")


#7 Buscar cliente por RUT
def buscar_cliente_por_rut(clientes: list[dict], rut: str) -> dict:
#Retorna el cliente con ese RUT manda ValueError si no existe
    rut = normalizar_rut(rut)
    for cliente in clientes:
        if cliente["rut"] == rut:
            return cliente
    raise ValueError("No existe un cliente con ese RUT")