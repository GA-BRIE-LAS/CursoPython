# =====================================================================
#  EJERCICIO 1 - Limpieza y resumen de sensores de temperatura
# =====================================================================


def limpiar_registro_sensor(registro_raw: dict[str, str]):
    """Recibe un registro 'sucio' y devuelve un diccionario estandarizado."""

    # Limpiamos el identificador (le sacamos los espacios de los costados)
    sensor_id = registro_raw["sensor_id"].strip()

    # Obtenemos la temperatura, le sacamos el sufijo de unidad y la pasamos a float
    temperatura = float(
        registro_raw["temperatura"]
        .replace("°C", "")
        .replace("C", "")
        .strip()
    )

    # Obtenemos la ubicacion; si no viene la clave, usamos un valor por defecto
    ubicacion = registro_raw.get("ubicacion", "").strip()
    if ubicacion == "":
        ubicacion = "Ubicación desconocida"

    # Devolvemos el registro ya estandarizado
    registro_limpio = {
        "sensor_id": sensor_id,
        "temperatura": temperatura,
        "ubicacion": ubicacion
    }
    return registro_limpio


def generar_resumen_sensores(lista_sensores_limpios, umbral_temperatura):
    """Devuelve una tupla: (lista de sensores en alerta, promedio de temperatura)."""

    lista_sensores_alerta = []
    suma_temperaturas = 0

    for sensor in lista_sensores_limpios:
        temperatura = sensor["temperatura"]
        sensor_id = sensor["sensor_id"]

        # Si supera el umbral, lo agregamos a la lista de alertas
        if temperatura > umbral_temperatura:
            lista_sensores_alerta.append(sensor_id)

        suma_temperaturas += temperatura

    # Verificamos que la lista no este vacia para no dividir por cero
    if len(lista_sensores_limpios) > 0:
        promedio_temperatura = suma_temperaturas / len(lista_sensores_limpios)
    else:
        promedio_temperatura = 0

    return lista_sensores_alerta, promedio_temperatura


# ----------------------- Bloque principal -----------------------
sensores_raw = [
    {
        "sensor_id": " TEMP-015 ",
        "temperatura": "28.7 °C",
        "ubicacion": " Sector de Producción "
    },
    {
        "sensor_id": " TEMP-016",
        "temperatura": "32.5C",
        "ubicacion": "Depósito"
    },
    {
        "sensor_id": "TEMP-017 ",
        "temperatura": "25.3 °C",
        "ubicacion": "Laboratorio"
    },
    {
        "sensor_id": " TEMP-018 ",
        "temperatura": "35.8C"
        # Este registro NO trae "ubicacion": se usará "Ubicación desconocida"
    },
    {
        "sensor_id": "TEMP-019",
        "temperatura": "27.1 °C",
        "ubicacion": "Almacén"
    }
]

# Limpiamos todos los registros
sensores_limpios = []
for registro in sensores_raw:
    registro_limpio = limpiar_registro_sensor(registro)
    sensores_limpios.append(registro_limpio)

# El umbral de alerta lo pide al usuario
umbral = float(input("Ingrese el umbral de temperatura (°C): "))

# Generamos el resumen
sensores_alerta, promedio_global = generar_resumen_sensores(sensores_limpios, umbral)

# Mostramos los resultados
for sensor in sensores_limpios:
    print(f"sensor: {sensor['sensor_id']} - temperatura: {sensor['temperatura']} - ubicación: {sensor['ubicacion']}")

print(f"Umbral establecido: {umbral}")
print(f"Promedio global: {promedio_global:.2f} °C")
print(f"Dispositivos en alerta (superan el umbral): {sensores_alerta}")
