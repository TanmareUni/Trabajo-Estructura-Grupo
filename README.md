# Trabajo-Estructura-Grupo

## Alcance

| RF | Qué cubre esta parte |
|---|---|
| RF04 | Programar y consultar viajes |
| RF05 | Venta de pasajes y cálculo automático de tarifas |
| RF06 | Reutilización de asientos por tramo |
| RF07 | Anulación de pasajes |
| RF09 | Pasajes vigentes y anulados de un viaje, recaudación vigente y ocupación de asientos por tramo |

## Instalación

Requiere Python 3.10 o superior.

```bash
pip install -r requirements.txt   # instala colorama
```

## Ejecución

Las funciones de esta parte se usan desde el menú principal del sistema, donde `integracion_menu.py` las conecta con las opciones de viajes y pasajes.

## Organización

| Archivo | Responsabilidad |
|---|---|
| `tarifas.py` | Precio de un pasaje según los segmentos recorridos |
| `asientos.py` | Superposición de tramos, validación de asientos y ocupación por tramo |
| `viajes.py` | Programar viajes; validación de bus, fecha, hora y extremos del recorrido |
| `pasajes.py` | Venta, anulación, listado por viaje y recaudación vigente |
| `consola.py` | Mensajes con colores (colorama): títulos, confirmaciones, errores y advertencias |
| `integracion_menu.py` | Funciones del menú que conectan estos módulos con la consola |

### Archivos de datos

| Archivo | Campos |
|---|---|
| `viajes.json` | `id_viaje`, `id_bus`, `fecha`, `hora`, `id_origen`, `id_destino`, `tarifa_base` |
| `pasajes.json` | `id_pasaje`, `id_viaje`, `id_cliente`, `id_origen`, `id_destino`, `asiento`, `valor`, `estado` |

Las relaciones se hacen solo por ID (`id_bus`, `id_cliente`, `id_viaje`, `id_origen`, `id_destino`), sin duplicar datos de otras entidades.

## Reglas implementadas

- **Tarifa:** `tarifa_base` menos 10% por cada uno de los 5 segmentos del recorrido que no se usan (descuento acumulativo, no compuesto). No depende del sentido. Con base $10.000: Concepción–Santiago $10.000, Chillán–Santiago $9.000, Concepción–Talca $8.000, Chillán–Talca $7.000, Santiago–Rancagua y Talca–Linares $6.000.
- **Viajes:** solo Concepción–Santiago o Santiago–Concepción, con bus existente y disponible. Un bus no puede tener dos viajes en la misma fecha y hora.
- **Venta:** el cliente y el viaje deben existir, el tramo debe respetar el sentido del viaje, el origen debe ser distinto del destino y el asiento debe estar dentro de la capacidad del bus.
- **Reutilización de asientos:** un asiento puede venderse varias veces en un viaje si los tramos no se superponen. El descenso en una ciudad libera el asiento para un embarque en esa misma ciudad.
- **Anulación:** el pasaje cambia de estado `vigente` a `anulado` y no se borra. Libera el asiento solo en su tramo. No se puede anular dos veces. Los pasajes anulados no cuentan en la ocupación ni en la recaudación.

## Estructuras y algoritmos

### Búsqueda secuencial

`buscar_viaje`, `buscar_pasaje` y `asiento_libre_en_tramo` recorren las listas de registros cargadas desde los archivos JSON.

- **Justificación:** las listas son pequeñas y no necesitan mantenerse ordenadas por ID. `asiento_libre_en_tramo` debe revisar todos los pasajes vigentes del viaje para comparar tramos, por lo que una búsqueda binaria no es aplicable.
- **Valor funcional:** valida que un viaje exista, permite anular un pasaje por su ID y decide si un asiento está libre en un tramo.

### Algoritmo de superposición de tramos

Decisión de diseño de `asientos.py`: cada pasaje se representa como un intervalo `(inicio, fin)` con las posiciones de las ciudades. Dos tramos se superponen cuando `inicio_a < fin_b` y `inicio_b < fin_a`.

- Chillán–Talca `(1, 3)` y Linares–Rancagua `(2, 4)` se superponen, así que el asiento se rechaza.
- Concepción–Chillán `(0, 1)` y Chillán–Talca `(1, 3)` no se superponen, así que el asiento se reutiliza.
- El tramo se ordena con `min` y `max`, por lo que funciona igual en ambos sentidos del viaje.

## Casos de aceptación cubiertos

Esta parte cumple, entre otros, los siguientes casos de aceptación del enunciado:

- Tarifas: Concepción–Santiago 100%, Chillán–Santiago 90%, Santiago–Rancagua 60%.
- Origen igual al destino: venta rechazada.
- Asiento fuera de capacidad: operación rechazada.
- Asiento ocupado en tramo superpuesto: venta rechazada.
- Asiento reutilizado en tramo consecutivo: venta permitida.
- Anulación de un pasaje vigente: el asiento queda libre solo en ese tramo.
- Anulación repetida: operación rechazada.
- Recaudación luego de anular: excluye el pasaje anulado.
- Guardar y volver a cargar los pasajes conserva los datos y sus estados.

## Dependencias de otras partes

| Módulo | Qué usa esta parte |
|---|---|
| `archivos.py` | `leer_archivo`, `guardar_archivo`, `siguiente_id` |
| `ciudades.py` | `obtener_posicion` |
| `clientes.py` | `buscar_cliente` |
| `buses.py` | `buscar_bus`, `cargar_buses` |
