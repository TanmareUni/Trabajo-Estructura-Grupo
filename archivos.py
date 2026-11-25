"""
Módulo archivos: lectura y escritura de los archivos JSON del sistema RutaSur.
Todos los módulos (clientes, buses, viajes, pasajes) usan estas funciones.
"""

import json

#1 Leer archivo retorna la lista de registros guardados en el archivo

def leer_archivo(ruta: str) -> list[dict]:
#Lee un archivo JSON y retorna una lista de diccionarios
#Si el archivo no existe o está vacío, retorna una lista vacía
#Lanza ValueError si el archivo no se puede leer o está dañado
    try:
        archivo = open(ruta, "r", encoding="utf-8")
        contenido = archivo.read()
        archivo.close()
    except FileNotFoundError:
        #primera vez que se ejecuta el programa el archivo todavía no existe
        return []
    except OSError:
        raise ValueError(f"No se pudo leer el archivo {ruta}")

    if contenido.strip() == "":
        #archivo vacío no hay registros
        return []

    try:
        return json.loads(contenido)
    except json.JSONDecodeError:
        raise ValueError(f"El archivo {ruta} está dañado")


#2 Guardar archivo escribe la lista de registros completa en el archivo
def guardar_archivo(ruta: str, registros: list[dict]) -> None:
#Guarda la lista de diccionarios en un archivo JSON
#Lanza ValueError si no se puede escribir el archivo
    try:
        archivo = open(ruta, "w", encoding="utf-8")
        json.dump(registros, archivo, indent=4, ensure_ascii=False)
        archivo.close()
    except OSError:
        raise ValueError(f"No se pudo guardar el archivo {ruta}")


#3 Siguiente ID calcula el proximo identificador numerico único
def siguiente_id(registros: list[dict], campo: str) -> int:
#Retorna el mayor ID existente + 1 (o 1 si no hay registros)
    mayor = 0
    for registro in registros:
        if registro[campo] > mayor:
            mayor = registro[campo]
    return mayor + 1