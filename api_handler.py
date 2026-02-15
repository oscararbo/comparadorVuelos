import requests
import csv
from datetime import datetime

def guardar_precio(vuelo):
    # Guardar el precio del vuelo en un archivo CSV para análisis histórico
    with open('historico_precios.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([vuelo['origen'], vuelo['destino'], vuelo['fecha_salida'], vuelo['fecha_regreso'], vuelo['precio'], datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

def buscar_vuelos(origen, destino, fecha_salida, fecha_regreso):
    # Construir la URL de la API con los parámetros de búsqueda
    url = f"https://api.ejemplo.com/vuelos?origen={origen}&destino={destino}&fecha_salida={fecha_salida}&fecha_regreso={fecha_regreso}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        vuelos = response.json()

        for vuelo in vuelos:
            guardar_precio(vuelo)

        return vuelos
    except requests.RequestException as e:
        print(f"Error al consultar la API: {e}")
        return None
