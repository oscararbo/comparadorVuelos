# Comparador de Vuelos

## Descripción
El Comparador de Vuelos es una herramienta que permite a los usuarios buscar y comparar precios de vuelos de diferentes aerolíneas a través de sus APIs.
Con esta aplicación, los usuarios pueden ingresar su origen, destino, fechas de viaje y obtener una lista de opciones de vuelos disponibles con sus respectivos precios. Además, los resultados se guardan en un archivo CSV para futuras referencias.

## Instalación
1. Clona el repositorio:
  ```bash
    git clone
  ```  
2. Navega al directorio del proyecto
3. Asegúrate de tener Python 3 instalado en tu sistema
4. Crea un entorno virtual (opcional pero recomendado):
  ```bash
    python -m venv env
    source env/bin/activate  # En Windows: env\Scripts\activate
  ```
5. Instala las dependencias:
  ```bash
    pip install -r requirements.txt
  ```

## Uso
Ejecuta el script principal:
  ```bash
    python main.py
  ```
Sigue las instrucciones en pantalla para ingresar los detalles de tu vuelo (origen, destino, fechas) y el programa te mostrará los resultados encontrados.

## Estructura del Proyecto
- `main.py`: Punto de entrada del programa, maneja la interacción con el usuario.
- `api_handler.py`: Contiene funciones para interactuar con las APIs de aerolíneas y guardar los precios en un archivo CSV.
- `data_processor.py`: Funciones para procesar y formatear los datos obtenidos de las APIs. Actualmente, esta función simplemente devuelve los datos sin cambios, pero se puede expandir para incluir lógica de procesamiento adicional. 
- `gui.py`: Implementa la interfaz gráfica utilizando Tkinter para facilitar la interacción del usuario.
- `requirements.txt`: Lista de dependencias necesarias para ejecutar el proyecto.