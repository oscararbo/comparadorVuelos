# Comparador de Vuelos 🛫

## Descripción
El Comparador de Vuelos es una herramienta moderna que permite a los usuarios buscar y comparar precios de vuelos en tiempo real utilizando la API de **Amadeus**.
Con esta aplicación intuitiva, los usuarios pueden ingresar su origen, destino y fechas de viaje para obtener una lista de opciones de vuelos disponibles con sus respectivos precios, duraciones y aerolíneas. Los resultados se guardan automáticamente en un archivo CSV para futuras referencias.

## Características
✅ Búsqueda de vuelos en tiempo real con Amadeus (400+ aerolíneas)  
✅ Interfaz gráfica moderna y fácil de usar (Tkinter)  
✅ Soporte para viajes de ida y vuelta  
✅ Historial de búsquedas guardado en CSV  
✅ Información detallada: precios, duraciones, números de vuelo y aerolíneas  
✅ Búsqueda asincrónica sin bloqueos en la interfaz  
✅ Autenticación OAuth2 con cacheo automático de tokens  

## Requisitos Previos
- Python 3.7+
- Una API Key y API Secret de Amadeus (obtén los en: https://developers.amadeus.com/)

## Obtener Credenciales de Amadeus
1. Visita https://developers.amadeus.com/
2. Haz clic en **Register** o **Sign In**
3. Una vez registrado, ve a **My Workspace** o **My Apps**
4. Crea una nueva aplicación (app) si no tienes una
5. Copia tu **API Key** (Client ID) y **API Secret** (Client Secret)
6. Abre `api_handler.py` y reemplaza estos valores:
   ```python
   API_KEY = "YOUR_API_KEY_HERE"      # Reemplaza con tu API Key
   API_SECRET = "YOUR_API_SECRET_HERE"  # Reemplaza con tu API Secret
   ```

## Instalación
1. Clona el repositorio:
  ```bash
    git clone <repo-url>
  ```  
2. Navega al directorio del proyecto:
  ```bash
    cd Comparador
  ```
3. Asegúrate de tener Python 3.7+ instalado en tu sistema
4. Crea un entorno virtual (recomendado):
  ```bash
    python -m venv env
  ```
5. Activa el entorno virtual:
  - **En Windows:**
    ```bash
      env\Scripts\activate
    ```
  - **En macOS/Linux:**
    ```bash
      source env/bin/activate
    ```
6. Instala las dependencias:
  ```bash
    pip install -r requirements.txt
  ```

## Configuración
**Importante:** Antes de ejecutar la aplicación, debes configurar tus credenciales:

1. Abre `api_handler.py`
2. Reemplaza estos valores con tus credenciales de Amadeus:
   ```python
   API_KEY = "mN5fRmRwBqt3jm20HlkG7e0KG1zmoIeW"
   API_SECRET = "H9XWSheVPuSq1lwa"
   ```
3. Guarda el archivo

## Uso
Ejecuta el script principal:
  ```bash
    python main.py
  ```

### Instrucciones de la Aplicación:
1. Ingresa el **código IATA** del aeropuerto de origen (ej: MAD para Madrid, BCN para Barcelona)
2. Ingresa el **código IATA** del aeropuerto de destino
3. Ingresa la **fecha de salida** en formato YYYY-MM-DD (ej: 2024-12-25)
4. Opcionalmente, ingresa la **fecha de regreso** (si dejas este campo vacío, buscará solo vuelos de ida)
5. Haz clic en **"Buscar Vuelos"**
6. ¡Obtén los resultados con los mejores precios disponibles!

### Códigos IATA Populares:
- MAD: Madrid-Barajas
- BCN: Barcelona-El Prat
- SVQ: Sevilla
- ALC: Alicante
- VLC: Valencia
- BIO: Bilbao
- IBZ: Ibiza
- AGP: Málaga
- PMI: Palma de Mallorca
- TFS: Tenerife Sur
- CDG: París-Charles de Gaulle
- LHR: Londres-Heathrow

## Estructura del Proyecto
- `main.py`: Punto de entrada del programa
- `api_handler.py`: Lógica de integración con API de Amadeus (OAuth2, búsqueda de vuelos)
- `data_processor.py`: Funciones para procesar datos (extensible para análisis adicionales)
- `gui.py`: Interfaz gráfica moderna con Tkinter
- `requirements.txt`: Dependencias del proyecto
- `historico_precios.csv`: Base de datos con histórico de búsquedas (generado automáticamente)

## Cómo funciona la API de Amadeus
1. **Autenticación OAuth2**: La aplicación se autentica usando tus credenciales (API Key y API Secret)
2. **Cacheo de Token**: El token de acceso se cachea durante 30 minutos para optimizar rendimiento
3. **Búsqueda de Vuelos**: Se realiza una búsqueda GET a `/v2/shopping/flight-offers` con los parámetros:
   - Código IATA de origen y destino
   - Fechas de salida (y regreso si aplica)
   - Número de adultos
4. **Respuesta Formateada**: Los resultados se muestran con:
   - Precio total en EUR
   - Duración del viaje
   - Detalles de los segmentos (horarios, números de vuelo, aerolínea)

## Notas Importantes
- La API de Amadeus proporciona datos de **400+ aerolíneas**
- Los precios mostrados son estimados y pueden variar
- El token de acceso OAuth2 se cachea automáticamente durante 30 minutos
- Los datos se guardan en `historico_precios.csv` para análisis histórico
- La moneda por defecto es EUR (puede configurarse)

## Troubleshooting
- **Error de autenticación**: Verifica que tus API Key y API Secret sean correctos
- **Error 400 - Invalid location codes**: Verifica que uses códigos IATA válidos (3 caracteres)
- **Error 400 - Invalid date**: Asegúrate de que las fechas estén en formato YYYY-MM-DD y sean en el futuro
- **No se encuentran vuelos**: Es posible que no haya disponibilidad. Intenta en otros aeropuertos o fechas

## Mejoras Futuras
- Soporte para múltiples monedas
- Filtros avanzados (aerolínea, precio máximo, escalas máximas, duración)
- Gráficos de tendencias de precios
- Notificaciones de precio más bajo
- Exportación a PDF
- Comparación de rutas

## Recursos Útiles
- Documentación API Amadeus: https://developers.amadeus.com/self-service
- Códigos IATA: https://www.iata.org/en/publications/directories/code-search/
- Amadeus GitHub: https://github.com/amadeus4dev
- Comunidad Amadeus Discord: https://discord.gg/cVrFBqx

## Licencia
Este proyecto es de código abierto y está disponible bajo la licencia MIT.