# Trabajo-Estructura-Grupo

# Funcionalidades implementadas

## Gestión de viajes

- Cargar y guardar viajes desde viajes.json.
- Generar un identificador automático para cada viaje.
- Programar viajes en el sentido Concepción-Santiago o Santiago-Concepción.
- Validar la fecha con formato AAAA-MM-DD.
- Validar la hora con formato HH:MM.
- Comprobar que el bus seleccionado esté disponible.
- Comprobar que el bus no tenga otro viaje programado en la misma fecha y hora.
- Validar que la tarifa base sea mayor que cero.
- Usar una tarifa base predeterminada de 10.000.
- Buscar viajes por identificador.
- Obtener la capacidad del bus asociado a un viaje.
- Determinar el sentido del viaje.

## Venta de pasajes

- Cargar y guardar pasajes desde pasajes.json.
- Verificar la existencia del cliente.
- Verificar la existencia del viaje.
- Impedir que el origen y el destino sean iguales.
- Impedir tramos que no respeten el sentido del viaje.
- Validar que el asiento sea entero y esté dentro de la capacidad del bus.
- Impedir que se repita un asiento ocupado en un tramo superpuesto.
- Registrar automáticamente el identificador, viaje, cliente, origen, destino, asiento, valor y estado del pasaje.
- Los pasajes se registran inicialmente con estado vigente.

## Anulación y consulta

- Buscar pasajes por identificador.
- Anular un pasaje vigente.
- Impedir anular dos veces el mismo pasaje.
- Mantener el pasaje anulado dentro del registro.
- Consultar todos los pasajes de un viaje.
- Filtrar pasajes por estado.
- Calcular la recaudación vigente sumando únicamente los pasajes vigentes.
- Liberar un asiento en el tramo correspondiente al pasaje anulado.

## Administración de asientos

- Representar cada asiento como un tramo definido por las posiciones de origen
  y destino.
- Detectar cuando dos tramos se superponen.
- Permitir reutilizar un asiento en tramos consecutivos o no superpuestos.
- Identificar los asientos ocupados y libres de un tramo determinado.
- Considerar solamente pasajes vigentes al calcular la ocupación.

## Cálculo de tarifas

- Trabajar con cinco segmentos totales.
- Aplicar un descuento del 10 % por segmento no utilizado.
- Calcular la cantidad de segmentos recorridos entre origen y destino.
- Rechazar tarifas base menores o iguales a cero.
- Rechazar tramos con origen y destino iguales.
- Rechazar tramos fuera del recorrido.
- Redondear el valor calculado a pesos enteros.

La fórmula utilizada es:

porcentaje = 100 - segmentos_no_usados × 10

valor = (tarifa_base × porcentaje + 50) / 100

## Integración con el menú

El módulo integracion_menu.py ofrece las siguientes acciones:

- Programar un viaje ingresando bus, fecha, hora, ciudades y tarifa base.
- Mostrar los viajes registrados con bus, fecha, hora, origen, destino y tarifa.
- Comprar un pasaje ingresando cliente, viaje, origen, destino y asiento.
- Anular un pasaje por identificador.
- Consultar los pasajes asociados a un viaje.
- Mostrar el recaudado vigente de un viaje.
- Consultar los asientos ocupados y libres de un tramo.
- Mostrar las ciudades disponibles para seleccionar origen y destino.
- Leer números enteros con validación.
- Mostrar mensajes de éxito, advertencia o error.

## Estados

- vigente: el pasaje participa en la ocupación y en la recaudación.
- anulado: el pasaje permanece registrado, libera su asiento en el tramo
  correspondiente y no suma a la recaudación.
