# Comparador de Vuelos 🛫

## Descripción
El Comparador de Vuelos es una herramienta moderna que permite a los usuarios buscar y comparar precios de vuelos en tiempo real utilizando la API de **Amadeus**.
Con esta aplicación intuitiva, los usuarios pueden ingresar su origen, destino y fechas de viaje para obtener una lista de opciones de vuelos disponibles con sus respectivos precios, duraciones y aerolíneas. Los resultados se guardan automáticamente en un archivo CSV para futuras referencias.

## Características
✅ Búsqueda de vuelos en tiempo real con Amadeus (400+ aerolíneas)  
✅ Interfaz gráfica moderna y fácil de usar (Tkinter)  
✅ Soporte para viajes de ida y vuelta  
✅ **Búsqueda dinámica de aeropuertos** - Escribe y obtén sugerencias en tiempo real desde la API de Amadeus  
✅ **Solo aeropuertos disponibles** - Solo muestra aeropuertos donde puedes comprar vuelos a través de Amadeus  
✅ Selectores de fecha con calendario integrado  
✅ Historial de búsquedas guardado en CSV  
✅ Información detallada: precios, duraciones, números de vuelo y aerolíneas  
✅ Búsqueda asincrónica sin bloqueos en la interfaz  
✅ Autenticación OAuth2 con cacheo automático de tokens  
✅ Caché inteligente de búsquedas de aeropuertos para mejorar rendimiento  

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
1. **Selecciona el aeropuerto de origen**: Comienza a escribir el nombre de la ciudad o aeropuerto (ej: "Madrid", "Barcelona", "New York")
   - La aplicación buscará automáticamente aeropuertos disponibles en la API de Amadeus
   - Solo se muestran aeropuertos donde realmente puedes comprar vuelos
2. **Selecciona el aeropuerto de destino**: Repite el proceso para el destino
3. **Selecciona la fecha de salida**: Haz clic en el calendario para elegir la fecha
   - No puedes seleccionar fechas pasadas
4. **Opcionalmente, marca "Incluir vuelta"** y selecciona la fecha de regreso
5. Haz clic en **"Buscar Vuelos"**
6. ¡Obtén los resultados con los mejores precios disponibles!

### Consejos de Uso:
- Escribe al menos 2 caracteres para comenzar la búsqueda de aeropuertos
- Puedes escribir el nombre de la ciudad (ej: "Madrid") o el código IATA (ej: "MAD")
- Los resultados se cachean para mejorar el rendimiento
- Si no encuentras tu aeropuerto, intenta escribir el nombre de la ciudad principal

### Ejemplos de Búsqueda:
- Escribir "Madrid" muestra: MAD - ADOLFO SUAREZ BARAJAS, MADRID (SPAIN)
- Escribir "LON" muestra: LHR, LGW, STN, LCY (todos los aeropuertos de Londres)
- Escribir "New York" muestra: JFK, EWR, LGA (aeropuertos del área de Nueva York)

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
3. **Búsqueda de Aeropuertos**: Cuando escribes en los campos de origen/destino:
   - Se realiza una búsqueda en `/v1/reference-data/locations` con tu texto como keyword
   - Solo se muestran aeropuertos y ciudades disponibles en Amadeus (subType=AIRPORT,CITY)
   - Los resultados se cachean para evitar llamadas repetidas
4. **Búsqueda de Vuelos**: Al hacer clic en "Buscar Vuelos":
   - Se realiza una búsqueda GET a `/v2/shopping/flight-offers` con los parámetros:
     * Código IATA de origen y destino
     * Fechas de salida (y regreso si aplica)
     * Número de adultos
5. **Respuesta Formateada**: Los resultados se muestran con:
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
- **Error de autenticación**: Verifica que tus API Key y API Secret sean correctos y que uses el entorno de test (test.api.amadeus.com)
- **No aparecen aeropuertos al escribir**: 
  * Asegúrate de escribir al menos 2 caracteres
  * Verifica tu conexión a internet
  * Revisa que tus credenciales de Amadeus sean válidas
- **Aeropuerto no encontrado**: La API de Amadeus solo muestra aeropuertos donde se pueden comprar vuelos. Intenta con el nombre de la ciudad principal más cercana
- **Error 400 - Invalid location codes**: Asegúrate de seleccionar un aeropuerto de la lista desplegable, no escribir manualmente
- **Error 400 - Invalid date**: Las fechas pasadas están deshabilitadas en el calendario
- **No se encuentran vuelos**: Es posible que no haya disponibilidad. Intenta en otros aeropuertos o fechas
- **Búsqueda lenta**: Los resultados se cachean. La segunda búsqueda del mismo término será instantánea

## Mejoras Futuras
- Soporte para múltiples monedas
- Filtros avanzados (aerolínea, precio máximo, escalas máximas, duración)
- Gráficos de tendencias de precios
- Notificaciones de precio más bajo
- Exportación a PDF
- Comparación de rutas
- Número de pasajeros configurable
- Clases de cabina (Economy, Business, First)

## Recursos Útiles
- Documentación API Amadeus: https://developers.amadeus.com/self-service
- Códigos IATA: https://www.iata.org/en/publications/directories/code-search/
- Amadeus GitHub: https://github.com/amadeus4dev
- Comunidad Amadeus Discord: https://discord.gg/cVrFBqx

## Licencia
Este proyecto es de código abierto y está disponible bajo la licencia MIT.