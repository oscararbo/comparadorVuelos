"""
Comparador de Vuelos - Aplicación para buscar y comparar vuelos usando Amadeus API
"""

__version__ = "1.0.0"
__author__ = "Oscar"

from controllers.flight_controller import FlightController
from ui.gui import iniciar_interfaz

__all__ = ['FlightController', 'iniciar_interfaz']
