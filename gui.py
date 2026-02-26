import tkinter as tk
from tkinter import Text, messagebox, ttk
from tkcalendar import DateEntry
from api_handler import buscar_vuelos, buscar_aeropuertos_amadeus
import threading
from datetime import datetime

# Lista de aeropuertos comunes
AEROPUERTOS = [
    "MAD - Madrid (Barajas)",
    "BCN - Barcelona (El Prat)",
    "SVQ - Sevilla",
    "ALC - Alicante",
    "VLC - Valencia",
    "BIO - Bilbao",
    "IBZ - Ibiza",
    "AGP - Málaga (Costa del Sol)",
    "PMI - Palma de Mallorca",
    "TFS - Tenerife Sur",
    "TFN - Tenerife Norte",
    "LPA - Gran Canaria",
    "CDG - París (Charles de Gaulle)",
    "ORY - París (Orly)",
    "LHR - Londres (Heathrow)",
    "LGW - Londres (Gatwick)",
    "STN - Londres (Stansted)",
    "AMS - Ámsterdam (Schiphol)",
    "FCO - Roma (Fiumicino)",
    "CIA - Roma (Ciampino)",
    "MXP - Milán (Malpensa)",
    "LIN - Milán (Linate)",
    "VCE - Venecia (Marco Polo)",
    "FLR - Florencia",
    "NAP - Nápoles",
    "MUC - Múnich",
    "FRA - Frankfurt",
    "BER - Berlín",
    "DUS - Düsseldorf",
    "ZRH - Zúrich",
    "GVA - Ginebra",
    "VIE - Viena",
    "PRG - Praga",
    "BUD - Budapest",
    "WAW - Varsovia",
    "ATH - Atenas",
    "LIS - Lisboa",
    "OPO - Oporto",
    "DUB - Dublín",
    "BRU - Bruselas",
    "CPH - Copenhague",
    "OSL - Oslo",
    "ARN - Estocolmo",
    "HEL - Helsinki",
    "IST - Estambul",
    "JFK - Nueva York (JFK)",
    "LAX - Los Ángeles",
    "MIA - Miami",
    "ORD - Chicago",
    "MEX - Ciudad de México",
    "BOG - Bogotá",
    "LIM - Lima",
    "SCL - Santiago de Chile",
    "GRU - São Paulo",
    "EZE - Buenos Aires"
]


def filtrar_aeropuertos(event, combobox, lista_completa=None):
    """Filtra aeropuertos usando la API de Amadeus en tiempo real"""
    valor = event.widget.get().strip()
    
    # Si está vacío, limpiar resultados
    if valor == '':
        combobox['values'] = []
        return
    
    # Buscar en Amadeus API con el texto introducido
    resultados = buscar_aeropuertos_amadeus(valor)
    
    # Si no hay resultados de la API y hay lista de respaldo, usar filtro local
    if not resultados and lista_completa:
        valor_upper = valor.upper()
        resultados = [item for item in lista_completa if valor_upper in item.upper()]
    
    combobox['values'] = resultados
    
    # Si hay solo un resultado, no mostrar dropdown (esperar más input)
    if len(resultados) > 1:
        combobox.event_generate('<Down>')


def extraer_codigo_iata(seleccion):
    """Extrae el código IATA de la selección (ej: 'MAD - Madrid' -> 'MAD')"""
    if seleccion:
        return seleccion.split(' - ')[0].strip()
    return ""

def mostrar_resultados():
    # Extraer códigos IATA de las selecciones
    origen = extraer_codigo_iata(origen_combo.get())
    destino = extraer_codigo_iata(destino_combo.get())
    fecha_salida = fecha_salida_entry.get_date().strftime("%Y-%m-%d")
    # Si no hay fecha de regreso, usar cadena vacía
    fecha_regreso = fecha_regreso_entry.get_date().strftime("%Y-%m-%d") if fecha_regreso_var.get() else ""

    # Validar campos
    if not origen or not destino:
        messagebox.showerror("Error", "Por favor selecciona origen y destino")
        return

    if len(origen) != 3 or len(destino) != 3:
        messagebox.showerror("Error", "Por favor selecciona aeropuertos válidos de la lista")
        return

    # Deshabilitar botón durante la búsqueda
    buscar_button.config(state=tk.DISABLED, text="Buscando...")
    resultados_text.config(state=tk.NORMAL)
    resultados_text.delete(1.0, tk.END)
    resultados_text.insert(tk.END, "Buscando vuelos, por favor espera...\n")

    # Ejecutar búsqueda en un hilo para no bloquear la GUI
    thread = threading.Thread(target=lambda: ejecutar_busqueda(origen, destino, fecha_salida, fecha_regreso))
    thread.daemon = True
    thread.start()


def toggle_fecha_regreso():
    """Habilita/deshabilita el selector de fecha de regreso"""
    if fecha_regreso_var.get():
        fecha_regreso_entry.config(state='normal')
    else:
        fecha_regreso_entry.config(state='disabled')

def ejecutar_busqueda(origen, destino, fecha_salida, fecha_regreso):
    try:
        resultados = buscar_vuelos(origen, destino, fecha_salida, fecha_regreso)

        # Mostrar resultados en el hilo principal
        resultados_text.config(state=tk.NORMAL)
        resultados_text.delete(1.0, tk.END)

        if resultados:
            for vuelo in resultados:
                resultados_text.insert(tk.END, f"{vuelo}\n")
                resultados_text.insert(tk.END, "-" * 60 + "\n")
        else:
            resultados_text.insert(tk.END, "No se encontraron vuelos para los criterios ingresados.")

        resultados_text.config(state=tk.DISABLED)
    except Exception as e:
        resultados_text.config(state=tk.NORMAL)
        resultados_text.delete(1.0, tk.END)
        resultados_text.insert(tk.END, f"Error en la búsqueda:\n{str(e)}")
        resultados_text.config(state=tk.DISABLED)
    finally:
        buscar_button.config(state=tk.NORMAL, text="Buscar Vuelos")


def iniciar_interfaz():
    global root, origen_combo, destino_combo, fecha_salida_entry, fecha_regreso_entry, fecha_regreso_var, resultados_text, buscar_button

    root = tk.Tk()
    root.title("Comparador de Vuelos - Amadeus")
    root.geometry("900x750")
    root.configure(bg="#f0f0f0")

    # Frame superior para controles
    control_frame = tk.Frame(root, bg="#ffffff", relief=tk.RAISED, bd=2)
    control_frame.pack(fill=tk.X, padx=10, pady=10)

    # Título
    titulo = tk.Label(control_frame, text="✈ Buscador de Vuelos", font=("Arial", 16, "bold"), bg="#ffffff")
    titulo.pack(pady=10)

    # Frame para inputs
    inputs_frame = tk.Frame(control_frame, bg="#ffffff")
    inputs_frame.pack(fill=tk.X, padx=15, pady=10)

    # Origen
    tk.Label(inputs_frame, text="Origen:", font=("Arial", 10), bg="#ffffff").grid(row=0, column=0,
                                                                                  sticky="w", pady=5)
    origen_combo = ttk.Combobox(inputs_frame, values=[], font=("Arial", 10), width=30)
    origen_combo.grid(row=0, column=1, padx=5, sticky="w")
    origen_combo.set("")  # Iniciar vacío
    origen_combo.bind('<KeyRelease>', lambda event: filtrar_aeropuertos(event, origen_combo, AEROPUERTOS))
    tk.Label(inputs_frame, text="🔍 Escribe para buscar aeropuertos", font=("Arial", 8, "italic"), fg="gray", bg="#ffffff").grid(row=0,
                                                                                                                column=2,
                                                                                                                sticky="w")

    # Destino
    tk.Label(inputs_frame, text="Destino:", font=("Arial", 10), bg="#ffffff").grid(row=1, column=0,
                                                                                   sticky="w", pady=5)
    destino_combo = ttk.Combobox(inputs_frame, values=[], font=("Arial", 10), width=30)
    destino_combo.grid(row=1, column=1, padx=5, sticky="w")
    destino_combo.set("")  # Iniciar vacío
    destino_combo.bind('<KeyRelease>', lambda event: filtrar_aeropuertos(event, destino_combo, AEROPUERTOS))
    tk.Label(inputs_frame, text="🔍 Escribe para buscar aeropuertos", font=("Arial", 8, "italic"), fg="gray", bg="#ffffff").grid(row=1,
                                                                                                                column=2,
                                                                                                                sticky="w")

    # Fecha de Salida
    tk.Label(inputs_frame, text="Fecha Salida:", font=("Arial", 10), bg="#ffffff").grid(row=2, column=0,
                                                                                       sticky="w", pady=5)
    fecha_salida_entry = DateEntry(inputs_frame, font=("Arial", 10), width=15,
                                    background='darkblue', foreground='white',
                                    borderwidth=2, date_pattern='yyyy-mm-dd',
                                    mindate=datetime.now())
    fecha_salida_entry.grid(row=2, column=1, padx=5, sticky="w")
    tk.Label(inputs_frame, text="📅 Selecciona con el calendario", font=("Arial", 8, "italic"), fg="gray", bg="#ffffff").grid(row=2,
                                                                                                             column=2,
                                                                                                             sticky="w")

    # Fecha de Regreso (opcional)
    fecha_regreso_var = tk.BooleanVar(value=False)
    
    regreso_frame = tk.Frame(inputs_frame, bg="#ffffff")
    regreso_frame.grid(row=3, column=0, columnspan=3, sticky="w", pady=5)
    
    tk.Checkbutton(regreso_frame, text="Incluir vuelta", variable=fecha_regreso_var,
                   font=("Arial", 10), bg="#ffffff",
                   command=lambda: toggle_fecha_regreso()).pack(side=tk.LEFT)
    
    fecha_regreso_entry = DateEntry(regreso_frame, font=("Arial", 10), width=15,
                                     background='darkblue', foreground='white',
                                     borderwidth=2, date_pattern='yyyy-mm-dd',
                                     mindate=datetime.now(), state='disabled')
    fecha_regreso_entry.pack(side=tk.LEFT, padx=10)
    
    tk.Label(regreso_frame, text="📅 Opcional: marca para viaje de ida y vuelta", 
             font=("Arial", 8, "italic"), fg="gray", bg="#ffffff").pack(side=tk.LEFT, padx=5)

    # Botón de búsqueda
    buscar_button = tk.Button(root, text="Buscar Vuelos", command=mostrar_resultados,
                              font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
                              padx=20, pady=10, cursor="hand2")
    buscar_button.pack(pady=10)

    # Frame para resultados
    resultado_frame = tk.Frame(root, bg="#ffffff", relief=tk.SUNKEN, bd=2)
    resultado_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    tk.Label(resultado_frame, text="Resultados:", font=("Arial", 10, "bold"), bg="#ffffff").pack(anchor="w", padx=5,
                                                                                                 pady=5)

    # Área de texto con scrollbar
    scrollbar = tk.Scrollbar(resultado_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    resultados_text = Text(resultado_frame, height=20, width=80, font=("Courier", 9),
                           yscrollcommand=scrollbar.set, bg="#fafafa")
    resultados_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    resultados_text.config(state=tk.DISABLED)
    scrollbar.config(command=resultados_text.yview)

    # Footer
    footer = tk.Label(root, text="🔑 Amadeus API (Test) | 🔍 Escribe en origen/destino para filtrar | 📅 Selecciona fechas en calendario",
                      font=("Arial", 8, "italic"), fg="gray", bg="#f0f0f0")
    footer.pack(pady=5)

    # Iniciar el bucle principal de la interfaz
    root.mainloop()