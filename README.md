# Comparador de Vuelos

## Descripción
El Comparador de Vuelos es una herramienta moderna que permite a los usuarios buscar y comparar precios de vuelos en tiempo real utilizando la API de **Amadeus**.
Con esta aplicación intuitiva, los usuarios pueden ingresar su origen, destino y fechas de viaje para obtener una lista de opciones de vuelos disponibles con sus respectivos precios, duraciones y aerolíneas. Los resultados se guardan automáticamente en un archivo CSV para futuras referencias.

## Características
- Búsqueda de vuelos en tiempo real con Amadeus (400+ aerolíneas)  
- Interfaz gráfica moderna y fácil de usar (Tkinter)  
- **Ventana optimizada** (950x750 píxeles) con área de resultados ampliada
- **Paneles plegables** - Los filtros y herramientas se pueden ocultar para maximizar el espacio de resultados
- **Resultados legibles** - Fuente Arial 9 para mejor visualización
- Soporte para viajes de ida y vuelta con múltiples adultos (1-9)  
- **Búsqueda dinámica de aeropuertos** - Escribe al menos 3 letras y obtén sugerencias en tiempo real desde la API de Amadeus  
- **Solo aeropuertos disponibles** - Solo muestra aeropuertos donde puedes comprar vuelos a través de Amadeus  
- **Sistema de filtros avanzado**  
   - Filtrar por precio máximo (50-5000 EUR)  
   - Filtrar por duración máxima (1-48 horas)  
   - Filtrar por número de escalas (0-5)  
   - Aplicar múltiples filtros simultáneamente  
   - Ver resultados filtrados en tiempo real sin nuevas llamadas a la API
- **Herramientas de ordenamiento** - Ordena vuelos por precio, duración o número de escalas
- **Estadísticas automáticas** - Precio min/max/promedio y duración por búsqueda
- Selectores de fecha con calendario integrado (sin fechas pasadas)  
- **Historial detallado en CSV** con:  
   - Precio mínimo y máximo por persona  
   - Precio total (mínimo y máximo)  
   - Indicador de escalas obligatorias  
   - Número de adultos y timestamp
- **Arquitectura MVC** - Lógica de negocio separada en `flight_controller.py` para mejor mantenimiento
- **Búsquedas consecutivas sin reiniciar** - Sistema de reseteo automático de filtros
- Prevención de búsquedas concurrentes con indicador de progreso
- Búsqueda asincrónica sin bloqueos en la interfaz  
- Autenticación OAuth2 con cacheo automático de tokens  
- Caché inteligente de búsquedas de aeropuertos para mejorar rendimiento  

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
   - Se requieren al menos 3 letras para iniciar la búsqueda
2. **Selecciona el aeropuerto de destino**: Repite el proceso para el destino
3. **Selecciona la fecha de salida**: Haz clic en el calendario para elegir la fecha
   - No puedes seleccionar fechas pasadas
4. **Opcionalmente, marca "Incluir vuelta"** y selecciona la fecha de regreso
5. **Selecciona el número de adultos** (1-9) - El precio total se calculará automáticamente
6. Haz clic en **"Buscar Vuelos"**
7. **Usa los filtros** para refinar los resultados:
   - **Precio máximo**: Solo muestra vuelos dentro de tu presupuesto
   - **Duración máxima**: Filtra por tiempo total de viaje
   - **Escalas máximas**: Elige entre vuelos directos (0) o con escalas (1-5)
   - Activa/desactiva cada filtro según tus necesidades
   - Haz clic en "Aplicar Filtros" para ver los cambios
   - Haz clic en "Limpiar Filtros" para volver a ver todos los resultados
8. **Usa las herramientas de ordenamiento** para organizar resultados por precio, duración o escalas
9. **Oculta/muestra paneles** con los botones de los filtros y herramientas para maximizar el área de resultados
10. Realiza nuevas búsquedas sin reiniciar la aplicación

### Consejos de Uso:
- Escribe al menos 3 letras para comenzar la búsqueda de aeropuertos
- Puedes escribir el nombre de la ciudad (ej: "Madrid") o el código IATA (ej: "MAD")
- Los resultados se cachean para mejorar el rendimiento
- Si no encuentras tu aeropuerto, intenta escribir el nombre de la ciudad principal

### Ejemplos de Búsqueda:
- Escribir "Madrid" muestra: MAD - ADOLFO SUAREZ BARAJAS, MADRID (SPAIN)
- Escribir "LON" muestra: LHR, LGW, STN, LCY (todos los aeropuertos de Londres)
- Escribir "New York" muestra: JFK, EWR, LGA (aeropuertos del área de Nueva York)

**Casos de uso comunes:**
- **Viaje económico**: Activa filtro de precio (ej: máx 300 EUR) + máx 2 escalas
- **Viaje rápido**: Activa filtro de duración (ej: máx 8 horas) + solo directo (0 escalas)
- **Viaje flexible**: Usa filtros combinados para encontrar el mejor equilibrio precio/tiempo

## Estructura del Proyecto
```
Comparador/
├── __init__.py              # Inicialización del paquete principal
├── main.py                  # Punto de entrada del programa
├── controllers/             # Controladores (Lógica de negocio)
│   ├── __init__.py
│   └── flight_controller.py # Controlador de vuelos
├── handlers/                # Manejadores de API y servicios
│   ├── __init__.py
│   └── api_handler.py      # Integración con Amadeus API
├── ui/                      # Interfaz de usuario
│   ├── __init__.py
│   └── gui.py              # Interfaz gráfica Tkinter
├── requirements.txt         # Dependencias del proyecto
├── historico_precios.csv    # Historial detallado de búsquedas (generado automáticamente)
└── README.md                # Documentación del proyecto
```

### Detalles de los módulos:
- **controllers/flight_controller.py**: Controlador MVC con lógica de negocio (búsqueda, filtrado, ordenamiento, estadísticas)
- **handlers/api_handler.py**: OAuth2, búsqueda de vuelos/aeropuertos, formateo de datos, guardado CSV
- **ui/gui.py**: Interfaz Tkinter con paneles plegables, filtros y controles
- **historico_precios.csv**: Incluye precio min/max por persona, precio total, escalas obligatorias, número de adultos

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
   - Los filtros y herramientas se resetean automáticamente
   - Se previenen búsquedas concurrentes
5. **Filtrado de Resultados**:
   - Los vuelos se formatean en una estructura de datos con información detallada
   - Se habilitan los controles de filtrado y ordenamiento
   - Puedes aplicar filtros de precio, duración y escalas
   - El filtrado es local (sin nuevas llamadas a la API) e instantáneo
6. **Respuesta Formateada**: Los resultados se muestran con:
   - Precio por persona y precio total (según número de adultos)
   - Estadísticas automáticas (precio y duración min/max/promedio)
   - Duración del viaje
   - Detalles de los segmentos (horarios, números de vuelo, aerolínea)
7. **Guardado en CSV**: Se almacena información completa:
   - Precios mínimo y máximo por persona
   - Precio total calculado
   - Indicador de escalas obligatorias (Sí/No)
   - Número de adultos y timestamp

## Notas Importantes
- La API de Amadeus proporciona datos de **400+ aerolíneas**
- Los precios mostrados son estimados y pueden variar
- El token de acceso OAuth2 se cachea automáticamente durante 30 minutos
- Los datos de cada búsqueda se guardan en `historico_precios.csv` con información completa
- La moneda por defecto es EUR (puede configurarse)
- Puedes realizar múltiples búsquedas consecutivas sin reiniciar la aplicación
- Los paneles de filtros y herramientas son plegables para maximizar el espacio de visualización

## Troubleshooting
- **Error de autenticación**: Verifica que tus API Key y API Secret sean correctos y que uses el entorno de test (test.api.amadeus.com)
- **No aparecen aeropuertos al escribir**: 
  * Asegúrate de escribir al menos 3 letras
  * Verifica tu conexión a internet
  * Revisa que tus credenciales de Amadeus sean válidas
- **Aeropuerto no encontrado**: La API de Amadeus solo muestra aeropuertos donde se pueden comprar vuelos. Intenta con el nombre de la ciudad principal más cercana
- **Error 400 - Invalid location codes**: Asegúrate de seleccionar un aeropuerto de la lista desplegable, no escribir manualmente
- **Error 400 - Invalid date**: Las fechas pasadas están deshabilitadas en el calendario
- **No se encuentran vuelos**: Es posible que no haya disponibilidad. Intenta en otros aeropuertos o fechas
- **Búsqueda lenta**: Los resultados se cachean. La segunda búsqueda del mismo término será instantánea
- **Los filtros no aparecen**: Los filtros solo se habilitan después de realizar una búsqueda con resultados exitosos
- **"No hay vuelos que cumplan los filtros"**: Los filtros son muy restrictivos. Haz clic en "Limpiar Filtros" y ajústalos gradualmente
- **La ventana es demasiado pequeña**: Usa los botones para ocultar los paneles de Filtros y Herramientas y maximizar el área de resultados
- **No puedo hacer otra búsqueda**: Espera a que finalice la búsqueda actual. El sistema previene búsquedas concurrentes

## Mejoras Futuras
- Soporte para múltiples monedas
- Filtro por aerolínea específica
- Filtro por horario de salida/llegada específico
- Filtro por tipo de cabina (Economy, Business, First)
- Guardar configuraciones de filtros favoritas
- Gráficos de tendencias de precios
- Notificaciones de precio más bajo
- Exportación a PDF
- Comparación de rutas
- Integración con otras APIs de viajes
- Modo oscuro para la interfaz

## Recursos Útiles
- Documentación API Amadeus: https://developers.amadeus.com/self-service
- Códigos IATA: https://www.iata.org/en/publications/directories/code-search/
- Amadeus GitHub: https://github.com/amadeus4dev
- Comunidad Amadeus Discord: https://discord.gg/cVrFBqx

## Licencia
Este proyecto es de código abierto y está disponible bajo la licencia MIT.