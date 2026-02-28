from handlers.api_handler import buscar_vuelos, buscar_aeropuertos_amadeus, filtrar_vuelos


class FlightController:
    def __init__(self):
        self.vuelos_completos = []
        self.busqueda_actual = {}
    
    def filtrar_aeropuertos(self, keyword):
        """Filtra aeropuertos usando la API de Amadeus en tiempo real"""
        if not keyword or keyword.strip() == '' or len(keyword.strip()) < 3:
            return []
        
        return buscar_aeropuertos_amadeus(keyword.strip())
    
    def extraer_codigo_iata(self, seleccion):
        """Extrae el código IATA de la selección (ej: 'MAD - Madrid' -> 'MAD')"""
        if seleccion:
            return seleccion.split(' - ')[0].strip()
        return ""
    

    
    def ordenar_vuelos(self, criterio):
        """Ordena los vuelos según el criterio seleccionado"""
        if not self.vuelos_completos:
            return
        
        if criterio == "precio":
            self.vuelos_completos.sort(key=lambda v: v["precio"])
        elif criterio == "duracion":
            self.vuelos_completos.sort(key=lambda v: v["duracion_total_minutos"])
        elif criterio == "escalas":
            self.vuelos_completos.sort(key=lambda v: v["num_escalas"])
    
    def calcular_estadisticas(self, vuelos):
        """Calcula estadísticas de los vuelos"""
        if not vuelos:
            return None
        
        precios = [v["precio"] for v in vuelos]
        duraciones = [v["duracion_total_minutos"] for v in vuelos]
        
        return {
            "precio_min": min(precios),
            "precio_max": max(precios),
            "precio_promedio": sum(precios) / len(precios),
            "duracion_min": min(duraciones),
            "duracion_max": max(duraciones),
            "duracion_promedio": sum(duraciones) / len(duraciones),
            "total_vuelos": len(vuelos)
        }
    
    def ejecutar_busqueda(self, origen, destino, fecha_salida, fecha_regreso, adultos=1):
        """Ejecuta la búsqueda de vuelos y devuelve el resultado"""
        resultado = buscar_vuelos(origen, destino, fecha_salida, fecha_regreso, adultos)
        
        self.busqueda_actual = {
            "origen": origen,
            "destino": destino,
            "fecha_salida": fecha_salida,
            "fecha_regreso": fecha_regreso,
            "adultos": adultos
        }
        
        if not resultado["error"] and resultado["vuelos"]:
            self.vuelos_completos = resultado["vuelos"]
        else:
            self.vuelos_completos = []
        
        return resultado
    
    def obtener_vuelos_filtrados(self, precio_max=None, duracion_max=None, escalas_max=None):
        """Obtiene los vuelos aplicando los filtros actuales"""
        if not self.vuelos_completos:
            return []
        
        return filtrar_vuelos(
            self.vuelos_completos,
            precio_max=precio_max,
            duracion_max=duracion_max * 60 if duracion_max else None,
            escalas_max=escalas_max
        )
    
    def formatear_vuelos_para_display(self, vuelos_filtrados):
        """Formatea los vuelos para mostrarlos en la interfaz"""
        if not vuelos_filtrados:
            return {
                "texto": f"No hay vuelos que cumplan los filtros seleccionados.\nTotal de vuelos disponibles: {len(self.vuelos_completos)}\n",
                "hay_vuelos": False
            }
        
        adultos = self.busqueda_actual.get('adultos', 1)
        stats = self.calcular_estadisticas(vuelos_filtrados)
        
        texto = f"\nESTADÍSTICAS - Mostrando {len(vuelos_filtrados)} de {len(self.vuelos_completos)} vuelos\n"
        texto += "=" * 60 + "\n"
        
        if stats:
            texto += f"Precio (por persona): Mín: {stats['precio_min']:.2f}€ | "
            texto += f"Máx: {stats['precio_max']:.2f}€ | "
            texto += f"Promedio: {stats['precio_promedio']:.2f}€\n"
            
            if adultos > 1:
                texto += f"Precio total ({adultos} adultos): Mín: {stats['precio_min']*adultos:.2f}€ | "
                texto += f"Máx: {stats['precio_max']*adultos:.2f}€ | "
                texto += f"Promedio: {stats['precio_promedio']*adultos:.2f}€\n"
            
            dur_min_h = stats['duracion_min'] // 60
            dur_min_m = stats['duracion_min'] % 60
            dur_max_h = stats['duracion_max'] // 60
            dur_max_m = stats['duracion_max'] % 60
            dur_avg_h = int(stats['duracion_promedio']) // 60
            dur_avg_m = int(stats['duracion_promedio']) % 60
            
            texto += f"Duración: Mín: {dur_min_h}h {dur_min_m}m | "
            texto += f"Máx: {dur_max_h}h {dur_max_m}m | "
            texto += f"Promedio: {dur_avg_h}h {dur_avg_m}m\n"
        
        texto += "=" * 60 + "\n\n"
        
        for vuelo in vuelos_filtrados:
            precio_unitario = vuelo["precio"]
            precio_total = precio_unitario * adultos
            
            texto_vuelo = f"Precio: {precio_unitario:.2f} EUR"
            if adultos > 1:
                texto_vuelo += f" | Precio Total ({adultos} adultos): {precio_total:.2f} EUR"
            texto_vuelo += f"\nEscalas: {vuelo['num_escalas']}\n"
            
            for idx, itin in enumerate(vuelo["itineraries"], 1):
                horas = itin["duracion_minutos"] // 60
                mins = itin["duracion_minutos"] % 60
                texto_vuelo += f"Tramo {idx} - Duración: {horas}h {mins}m\n"
                
                for seg in itin["segmentos"]:
                    texto_vuelo += f"  {seg['origen']} → {seg['destino']} | "
                    texto_vuelo += f"{seg['aerolinea']}{seg['numero_vuelo']} | "
                    texto_vuelo += f"Sal: {seg['hora_salida']} → Lleg: {seg['hora_llegada']}\n"
            
            texto += texto_vuelo
            texto += "-" * 60 + "\n"
        
        return {
            "texto": texto,
            "hay_vuelos": True
        }
