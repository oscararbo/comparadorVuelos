import requests
import csv
from datetime import datetime
import base64

API_KEY = "mN5fRmRwBqt3jm20HlkG7e0KG1zmoIeW"
API_SECRET = "H9XWSheVPuSq1lwa"

AUTH_URL = "https://test.api.amadeus.com/v1/security/oauth2/token"
FLIGHT_SEARCH_URL = "https://test.api.amadeus.com/v2/shopping/flight-offers"
AIRPORT_SEARCH_URL = "https://test.api.amadeus.com/v1/reference-data/locations"

_access_token = None
_token_expiry = None

_airport_cache = {}


def obtener_access_token():
    global _access_token, _token_expiry

    if _access_token and _token_expiry and datetime.now().timestamp() < _token_expiry:
        return _access_token

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


def buscar_aeropuertos_amadeus(keyword):
    """
    Busca aeropuertos y ciudades en Amadeus API
    Retorna lista de aeropuertos que Amadeus soporta
    """
    global _airport_cache
    
    keyword_upper = keyword.upper()
    if keyword_upper in _airport_cache:
        return _airport_cache[keyword_upper]
    
    if len(keyword) < 2:
        return []
    
    token = obtener_access_token()
    if not token:
        return []
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    params = {
        "subType": "AIRPORT,CITY",
        "keyword": keyword,
        "page[limit]": 20
    }
    
    try:
        response = requests.get(AIRPORT_SEARCH_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        resultados = []
        for location in data.get("data", []):
            iata_code = location.get("iataCode")
            name = location.get("name")
            city = location.get("address", {}).get("cityName", "")
            country = location.get("address", {}).get("countryName", "")
            
            if iata_code and name:
                label = f"{iata_code} - {name}"
                if city and city not in name:
                    label += f", {city}"
                if country:
                    label += f" ({country})"
                
                resultados.append(label)
        
        _airport_cache[keyword_upper] = resultados
        return resultados
        
    except requests.RequestException as e:
        print(f"Error al buscar aeropuertos: {e}")
        return []


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
    """
    Retorna una lista de diccionarios con la información estructurada de cada vuelo
    """
    vuelos_formateados = []

    if not data_api or "data" not in data_api:
        return vuelos_formateados

    for offer in data_api.get("data", []):
        try:
            precio = float(offer.get("price", {}).get("total", 0))
            moneda = offer.get("price", {}).get("currency", "EUR")

            duracion_total_minutos = 0
            itineraries = []
            num_escalas = 0

            for itin in offer.get("itineraries", []):
                duracion_str = itin.get("duration", "PT0H0M")
                minutos = parsear_duracion_iso(duracion_str)
                duracion_total_minutos += minutos
                
                segments = itin.get("segments", [])
                num_escalas += len(segments) - 1
                
                segmentos_itin = []
                for segment in segments:
                    hora_salida = segment.get("departure", {}).get("at", "N/A")
                    hora_llegada = segment.get("arrival", {}).get("at", "N/A")
                    
                    segmentos_itin.append({
                        "origen": segment.get('departure', {}).get('iataCode', '???'),
                        "destino": segment.get('arrival', {}).get('iataCode', '???'),
                        "aerolinea": segment.get("carrierCode", "N/A"),
                        "numero_vuelo": segment.get("number", "N/A"),
                        "hora_salida": hora_salida[:16] if hora_salida != "N/A" else "N/A",
                        "hora_llegada": hora_llegada[:16] if hora_llegada != "N/A" else "N/A",
                        "duracion": segment.get("duration", "N/A")
                    })
                
                itineraries.append({
                    "segmentos": segmentos_itin,
                    "duracion": duracion_str,
                    "duracion_minutos": minutos
                })

            vuelo_estructurado = {
                "precio": precio,
                "moneda": moneda,
                "duracion_total_minutos": duracion_total_minutos,
                "num_escalas": num_escalas,
                "itineraries": itineraries,
                "offer_completo": offer
            }

            vuelos_formateados.append(vuelo_estructurado)

        except Exception as e:
            print(f"Error al formatear vuelo: {e}")
            continue

    return vuelos_formateados


def parsear_duracion_iso(duracion_str):
    """
    Convierte duración ISO 8601 (ej: 'PT10H30M') a minutos totales
    """
    import re
    if not duracion_str or duracion_str == "N/A":
        return 0
    
    horas = 0
    minutos = 0
    
    match_h = re.search(r'(\d+)H', duracion_str)
    if match_h:
        horas = int(match_h.group(1))
    
    match_m = re.search(r'(\d+)M', duracion_str)
    if match_m:
        minutos = int(match_m.group(1))
    
    return horas * 60 + minutos


def formatear_vuelo_para_display(vuelo):
    """
    Convierte un vuelo estructurado a string para mostrar en la GUI
    """
    try:
        precio = vuelo["precio"]
        moneda = vuelo["moneda"]
        escalas = vuelo["num_escalas"]
        
        vuelo_str = f"Precio: {precio} {moneda}\n"
        vuelo_str += f"Escalas: {escalas}\n"
        
        for idx, itin in enumerate(vuelo["itineraries"], 1):
            horas = itin["duracion_minutos"] // 60
            mins = itin["duracion_minutos"] % 60
            vuelo_str += f"Tramo {idx} - Duración: {horas}h {mins}m\n"
            
            for seg in itin["segmentos"]:
                vuelo_str += f"  {seg['origen']} → {seg['destino']} | "
                vuelo_str += f"{seg['aerolinea']}{seg['numero_vuelo']} | "
                vuelo_str += f"Sal: {seg['hora_salida']} → Lleg: {seg['hora_llegada']}\n"
        
        return vuelo_str
    except Exception as e:
        return f"Error al mostrar vuelo: {e}\n"


def filtrar_vuelos(vuelos, precio_max=None, duracion_max=None, escalas_max=None, hora_salida_min=None, hora_salida_max=None):
    """
    Filtra una lista de vuelos según los criterios especificados
    
    Args:
        vuelos: Lista de vuelos estructurados
        precio_max: Precio máximo en la moneda del vuelo
        duracion_max: Duración máxima total en minutos
        escalas_max: Número máximo de escalas
        hora_salida_min: Hora mínima de salida (formato HH:MM)
        hora_salida_max: Hora máxima de salida (formato HH:MM)
    
    Returns:
        Lista de vuelos filtrados
    """
    vuelos_filtrados = []
    
    for vuelo in vuelos:
        if precio_max is not None and vuelo["precio"] > precio_max:
            continue
        
        if duracion_max is not None and vuelo["duracion_total_minutos"] > duracion_max:
            continue
        
        if escalas_max is not None and vuelo["num_escalas"] > escalas_max:
            continue
        
        if hora_salida_min or hora_salida_max:
            try:
                primer_segmento = vuelo["itineraries"][0]["segmentos"][0]
                hora_salida_str = primer_segmento["hora_salida"]
                
                if hora_salida_str != "N/A" and len(hora_salida_str) >= 11:
                    hora_salida = hora_salida_str.split('T')[1] if 'T' in hora_salida_str else hora_salida_str[11:]
                    hora_salida = hora_salida[:5]
                    
                    if hora_salida_min and hora_salida < hora_salida_min:
                        continue
                    if hora_salida_max and hora_salida > hora_salida_max:
                        continue
            except (IndexError, KeyError):
                pass
        
        vuelos_filtrados.append(vuelo)
    
    return vuelos_filtrados


def guardar_resultado_amadeus(origen, destino, fecha_salida, fecha_regreso, data_api, adultos=1):
    try:
        with open('historico_precios.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            if file.tell() == 0:
                writer.writerow([
                    'Origen', 'Destino', 'Fecha Salida', 'Fecha Regreso', 'Adultos',
                    'Precio Min/Persona', 'Precio Max/Persona', 'Precio Total Min', 'Precio Total Max',
                    'Escala Obligatoria', 'Moneda', 'Timestamp'
                ])

            if data_api and "data" in data_api:
                ofertas = data_api.get("data", [])
                if ofertas:
                    precios = [float(oferta.get("price", {}).get("total", 0)) for oferta in ofertas if oferta.get("price", {}).get("total")]
                    
                    if precios:
                        precio_min = min(precios)
                        precio_max = max(precios)
                        precio_total_min = precio_min * adultos
                        precio_total_max = precio_max * adultos
                        
                        escalas = [len(oferta.get("itineraries", [{}])[0].get("segments", [])) - 1 
                                 for oferta in ofertas if oferta.get("itineraries")]
                        escala_obligatoria = "Sí" if escalas and all(e > 0 for e in escalas) else "No"
                        
                        moneda = ofertas[0].get("price", {}).get("currency", "EUR")

                        writer.writerow([
                            origen, destino, fecha_salida, fecha_regreso, adultos,
                            f"{precio_min:.2f}", f"{precio_max:.2f}", 
                            f"{precio_total_min:.2f}", f"{precio_total_max:.2f}",
                            escala_obligatoria, moneda,
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        ])
    except Exception as e:
        print(f"Error al guardar resultado: {e}")


def buscar_vuelos(origen, destino, fecha_salida, fecha_regreso, adultos=1):
    if not API_KEY or not API_SECRET:
        return {"error": True, "mensaje": ["Error: Credenciales de Amadeus no configuradas"], "vuelos": []}

    resultado = buscar_vuelos_amadeus(origen, destino, fecha_salida, fecha_regreso, adultos)

    if not resultado:
        return {"error": True, "mensaje": ["Error: No se pudo conectar con la API de Amadeus"], "vuelos": []}

    if "errors" in resultado:
        errores = resultado.get("errors", [])
        mensajes_error = [f"{err.get('detail', 'Error desconocido')}" for err in errores]
        return {"error": True, "mensaje": mensajes_error if mensajes_error else ["Error en la búsqueda"], "vuelos": []}

    guardar_resultado_amadeus(origen, destino, fecha_salida, fecha_regreso, resultado, adultos)

    vuelos = formatear_vuelos_amadeus(resultado)

    if not vuelos:
        return {"error": False, "mensaje": ["No se encontraron vuelos para los criterios ingresados."], "vuelos": []}

    return {"error": False, "mensaje": [], "vuelos": vuelos}
