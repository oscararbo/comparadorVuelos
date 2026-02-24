import requests
import csv
from datetime import datetime
import base64

# Configuración de la API de Amadeus
API_KEY = "mN5fRmRwBqt3jm20HlkG7e0KG1zmoIeW"
API_SECRET = "H9XWSheVPuSq1lwa"

# Endpoints de Amadeus
AUTH_URL = "https://test.api.amadeus.com/v1/security/oauth2/token"
FLIGHT_SEARCH_URL = "https://test.api.amadeus.com/v2/shopping/flight-offers"

# Variable para cachear el token de acceso
_access_token = None
_token_expiry = None


def obtener_access_token():

    global _access_token, _token_expiry

    # Verificar si el token en caché aún es válido
    if _access_token and _token_expiry and datetime.now() < _token_expiry:
        return _access_token

    # Crear la cadena de autenticación básica
    auth_string = f"{API_KEY}:{API_SECRET}"
    auth_base64 = base64.b64encode(auth_string.encode()).decode()

    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {
        "grant_type": "client_credentials"
    }

    try:
        response = requests.post(AUTH_URL, headers=headers, data=payload)
        response.raise_for_status()
        data = response.json()

        _access_token = data.get("access_token")
        expires_in = data.get("expires_in", 1800)
        _token_expiry = datetime.now().timestamp() + expires_in - 60

        return _access_token
    except requests.RequestException as e:
        print(f"Error al obtener token de acceso: {e}")
        return None


def buscar_vuelos_amadeus(origen, destino, fecha_salida, fecha_regreso, adultos=1):

    token = obtener_access_token()
    if not token:
        return None

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    params = {
        "originLocationCode": origen.upper(),
        "destinationLocationCode": destino.upper(),
        "departureDate": fecha_salida,
        "adults": adultos,
        "max": 10
    }

    # Agregar fecha de regreso si existe
    if fecha_regreso:
        params["returnDate"] = fecha_regreso

    try:
        response = requests.get(FLIGHT_SEARCH_URL, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error en la búsqueda de vuelos: {e}")
        return None


def formatear_vuelos_amadeus(data_api):

    vuelos_formateados = []

    if not data_api or "data" not in data_api:
        return vuelos_formateados

    for offer in data_api.get("data", []):
        try:
            precio = offer.get("price", {}).get("total", "N/A")
            moneda = offer.get("price", {}).get("currency", "EUR")

            # Información de los tramos (itinerary)
            itinerary_info = []

            for itin in offer.get("itineraries", []):
                duracion = itin.get("duration", "N/A")

                # Procesar cada segmento (vuelo individual)
                for segment in itin.get("segments", []):
                    origin = segment.get("departure", {}).get("at", "N/A")[:16]
                    destination = segment.get("arrival", {}).get("at", "N/A")[:16]
                    carrier = segment.get("carrierCode", "N/A")
                    flight_number = segment.get("number", "N/A")
                    aircraft = segment.get("aircraft", {}).get("code", "N/A")

                    itinerary_info.append(
                        f"  {segment.get('departure', {}).get('iataCode', '???')} → "
                        f"{segment.get('arrival', {}).get('iataCode', '???')} | "
                        f"{carrier}{flight_number} | Salida: {origin} → Llegada: {destination}"
                    )

            # Información de pasajeros
            pasajeros_info = []
            for traveler in offer.get("travelerPricings", []):
                tipo_pasajero = traveler.get("travelerType", "ADULT")
                precio_pasajero = traveler.get("fareDetailsBySegment", [])
                pasajeros_info.append(f"  {tipo_pasajero}")

            # Compilar información del vuelo
            vuelo_str = f"Precio: {precio} {moneda}\n"

            for itin in offer.get("itineraries", []):
                duracion = itin.get("duration", "N/A")
                vuelo_str += f"Duración: {duracion}\n"

            vuelo_str += "Vuelos:\n"
            for info in itinerary_info:
                vuelo_str += f"{info}\n"

            vuelos_formateados.append(vuelo_str)

        except Exception as e:
            print(f"Error al formatear vuelo: {e}")
            continue

    return vuelos_formateados


def guardar_resultado_amadeus(origen, destino, fecha_salida, fecha_regreso, data_api):

    try:
        with open('historico_precios.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            # Escribir encabezado si el archivo está vacío
            if file.tell() == 0:
                writer.writerow(
                    ['Origen', 'Destino', 'Fecha Salida', 'Fecha Regreso', 'Precio Mínimo', 'Moneda', 'Timestamp'])

            if data_api and "data" in data_api:
                ofertas = data_api.get("data", [])
                if ofertas:
                    precio_minimo = ofertas[0].get("price", {}).get("total", "N/A")
                    moneda = ofertas[0].get("price", {}).get("currency", "EUR")

                    writer.writerow([origen, destino, fecha_salida, fecha_regreso, precio_minimo, moneda,
                                     datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    except Exception as e:
        print(f"Error al guardar resultado: {e}")


def buscar_vuelos(origen, destino, fecha_salida, fecha_regreso):

    # Validar que tenemos credenciales
    if not API_KEY or not API_SECRET:
        return ["Error: Credenciales de Amadeus no configuradas"]

    # Realizar búsqueda
    resultado = buscar_vuelos_amadeus(origen, destino, fecha_salida, fecha_regreso)

    if not resultado:
        return ["Error: No se pudo conectar con la API de Amadeus"]

    # Verificar si hay errores en la respuesta
    if "errors" in resultado:
        errores = resultado.get("errors", [])
        mensajes_error = [f"{err.get('detail', 'Error desconocido')}" for err in errores]
        return mensajes_error if mensajes_error else ["Error en la búsqueda"]

    # Guardar resultado en CSV
    guardar_resultado_amadeus(origen, destino, fecha_salida, fecha_regreso, resultado)

    # Formatear y retornar vuelos
    vuelos = formatear_vuelos_amadeus(resultado)

    if not vuelos:
        return ["No se encontraron vuelos para los criterios ingresados."]

    return vuelos