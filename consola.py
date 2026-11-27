"""
Módulo consola: mensajes con colores (colorama) compartidos por todo el proyecto.
Lo usan menu.py, reportes.py e integracion_menu.py. Así ningún módulo importa a menu.py (evita import circular).
"""

from colorama import init, Fore

init(autoreset=True)


#1 Título de menús y secciones
def titulo(texto: str) -> None:
    print(f"\n{Fore.CYAN}=== {texto} ===")


#2 Confirmaciones de operaciones exitosas
def ok(msg: str) -> None:
    print(f"{Fore.GREEN}{msg}")


#3 Errores de validación o de reglas de negocio
def error(msg: str) -> None:
    print(f"{Fore.RED}Error: {msg}")


#4 Advertencias que no detienen la operación
def aviso(msg: str) -> None:
    print(f"{Fore.YELLOW}Advertencia: {msg}") 