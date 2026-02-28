import tkinter as tk
from tkinter import Text, messagebox, ttk
from tkcalendar import DateEntry
from controllers.flight_controller import FlightController
from utils.graficos import graficar_precios, graficar_aerolineas, graficar_distribucion, mostrar_grafico_en_ventana
import threading
from datetime import datetime

controller = FlightController()
busqueda_en_progreso = False


def filtrar_aeropuertos(event, combobox):
    valor = event.widget.get().strip()

    if valor == '':
        combobox['values'] = []
        return

    resultados = controller.filtrar_aeropuertos(valor)
    combobox['values'] = resultados

    if len(resultados) > 1:
        combobox.event_generate('<Down>')


def mostrar_resultados():
    global busqueda_en_progreso

    if busqueda_en_progreso:
        messagebox.showwarning("Búsqueda en progreso", "Por favor espera a que finalice la búsqueda actual")
        return

    try:
        origen = controller.extraer_codigo_iata(origen_combo.get())
        destino = controller.extraer_codigo_iata(destino_combo.get())
        fecha_salida = fecha_salida_entry.get_date().strftime("%Y-%m-%d")
        fecha_regreso = fecha_regreso_entry.get_date().strftime("%Y-%m-%d") if fecha_regreso_var.get() else ""
        adultos = adultos_var.get()
        moneda = moneda_var.get()

        if not origen or not destino:
            messagebox.showerror("Error", "Por favor selecciona origen y destino")
            return

        if len(origen) != 3 or len(destino) != 3:
            messagebox.showerror("Error", "Por favor selecciona aeropuertos válidos de la lista")
            return

        busqueda_en_progreso = True
        resetear_filtros_antes_busqueda()
        buscar_button.config(state=tk.DISABLED, text="Buscando...")
        resultados_text.config(state=tk.NORMAL)
        resultados_text.delete(1.0, tk.END)
        resultados_text.insert(tk.END, "Buscando vuelos, por favor espera...\n")

        thread = threading.Thread(
            target=lambda: ejecutar_busqueda(origen, destino, fecha_salida, fecha_regreso, adultos, moneda))
        thread.daemon = True
        thread.start()
    except Exception as e:
        messagebox.showerror("Error", f"Error al iniciar búsqueda: {str(e)}")
        busqueda_en_progreso = False


def actualizar_fecha_minima_regreso():
    try:
        fecha_salida = fecha_salida_entry.get_date()
        fecha_regreso_entry.config(mindate=fecha_salida)

        # Si la fecha de regreso es anterior a la fecha de salida, ajustarla
        if fecha_regreso_var.get():
            fecha_regreso_actual = fecha_regreso_entry.get_date()
            if fecha_regreso_actual < fecha_salida:
                fecha_regreso_entry.set_date(fecha_salida)
    except:
        pass


def toggle_fecha_regreso():
    if fecha_regreso_var.get():
        fecha_regreso_entry.config(state='normal')
        actualizar_fecha_minima_regreso()
    else:
        fecha_regreso_entry.config(state='disabled')


def ejecutar_busqueda(origen, destino, fecha_salida, fecha_regreso, adultos=1, moneda="EUR"):
    global busqueda_en_progreso
    try:
        resultado = controller.ejecutar_busqueda(origen, destino, fecha_salida, fecha_regreso, adultos, moneda)

        root.after(0, lambda: actualizar_resultados_ui(resultado))
    except Exception as e:
        root.after(0, lambda: mostrar_error_ui(f"Error inesperado: {str(e)}"))
    finally:
        busqueda_en_progreso = False
        root.after(0, lambda: buscar_button.config(state=tk.NORMAL, text="Buscar Vuelos"))


def actualizar_resultados_ui(resultado):
    resultados_text.config(state=tk.NORMAL)
    resultados_text.delete(1.0, tk.END)

    if resultado["error"]:
        for mensaje in resultado["mensaje"]:
            resultados_text.insert(tk.END, f"{mensaje}\n")
    elif not resultado["vuelos"]:
        resultados_text.insert(tk.END, "No se encontraron vuelos para los criterios ingresados.")
    else:
        habilitar_filtros()
        mostrar_vuelos_filtrados()

    resultados_text.config(state=tk.DISABLED)


def mostrar_error_ui(error_msg):
    resultados_text.config(state=tk.NORMAL)
    resultados_text.delete(1.0, tk.END)
    resultados_text.insert(tk.END, f"Error en la búsqueda:\n{error_msg}")
    resultados_text.config(state=tk.DISABLED)


def aplicar_filtros():
    mostrar_vuelos_filtrados()


def mostrar_grafico_precios():
    if not controller.vuelos_completos:
        messagebox.showwarning("Sin datos", "No hay vuelos para graficar")
        return

    try:
        moneda = controller.busqueda_actual.get("moneda", "EUR")
        figura = graficar_precios(controller.vuelos_completos, moneda)
        mostrar_grafico_en_ventana(figura, "Tendencia de Precios")
    except Exception as e:
        messagebox.showerror("Error", f"Error al generar gráfico: {str(e)}")


def mostrar_grafico_aerolineas():
    if not controller.vuelos_completos:
        messagebox.showwarning("Sin datos", "No hay vuelos para graficar")
        return

    try:
        moneda = controller.busqueda_actual.get("moneda", "EUR")
        figura = graficar_aerolineas(controller.vuelos_completos, moneda)
        mostrar_grafico_en_ventana(figura, "Comparación de Aerolíneas")
    except Exception as e:
        messagebox.showerror("Error", f"Error al generar gráfico: {str(e)}")


def mostrar_grafico_distribucion():
    """Muestra el gráfico de distribución de precios"""
    if not controller.vuelos_completos:
        messagebox.showwarning("Sin datos", "No hay vuelos para graficar")
        return

    try:
        moneda = controller.busqueda_actual.get("moneda", "EUR")
        figura = graficar_distribucion(controller.vuelos_completos, moneda)
        mostrar_grafico_en_ventana(figura, "Distribución de Precios")
    except Exception as e:
        messagebox.showerror("Error", f"Error al generar gráfico: {str(e)}")


def mostrar_vuelos_filtrados():
    if not controller.vuelos_completos:
        return

    try:
        precio_max = precio_max_var.get() if precio_habilitado_var.get() else None
        duracion_max = duracion_max_var.get() if duracion_habilitado_var.get() else None
        escalas_max = escalas_max_var.get() if escalas_habilitado_var.get() else None
        hora_salida_min = hora_salida_min_var.get() if horario_habilitado_var.get() and hora_salida_min_var.get() else None
        hora_salida_max = hora_salida_max_var.get() if horario_habilitado_var.get() and hora_salida_max_var.get() else None

        vuelos_filtrados = controller.obtener_vuelos_filtrados(precio_max, duracion_max, escalas_max, hora_salida_min,
                                                               hora_salida_max)
        resultado_formato = controller.formatear_vuelos_para_display(vuelos_filtrados)

        resultados_text.config(state=tk.NORMAL)
        resultados_text.delete(1.0, tk.END)
        resultados_text.insert(tk.END, resultado_formato["texto"])
        resultados_text.config(state=tk.DISABLED)
    except Exception as e:
        messagebox.showerror("Error", f"Error al filtrar vuelos: {str(e)}")


def habilitar_filtros():
    precio_check.config(state=tk.NORMAL)
    duracion_check.config(state=tk.NORMAL)
    escalas_check.config(state=tk.NORMAL)
    horario_check.config(state=tk.NORMAL)
    aplicar_filtros_button.config(state=tk.NORMAL)
    limpiar_filtros_button.config(state=tk.NORMAL)
    ordenar_precio_button.config(state=tk.NORMAL)
    ordenar_duracion_button.config(state=tk.NORMAL)
    ordenar_escalas_button.config(state=tk.NORMAL)
    grafico_precios_button.config(state=tk.NORMAL)
    grafico_aerolineas_button.config(state=tk.NORMAL)
    grafico_distribucion_button.config(state=tk.NORMAL)


def limpiar_filtros():
    precio_habilitado_var.set(False)
    duracion_habilitado_var.set(False)
    escalas_habilitado_var.set(False)
    horario_habilitado_var.set(False)
    precio_max_var.set(2000)
    duracion_max_var.set(24)
    escalas_max_var.set(2)
    hora_salida_min_var.set("00:00")
    hora_salida_max_var.set("23:59")
    toggle_filtro_precio()
    toggle_filtro_duracion()
    toggle_filtro_escalas()
    toggle_filtro_horario()
    mostrar_vuelos_filtrados()


def toggle_filtro_precio():
    if precio_habilitado_var.get():
        precio_scale.config(state=tk.NORMAL)
    else:
        precio_scale.config(state=tk.DISABLED)


def toggle_filtro_duracion():
    if duracion_habilitado_var.get():
        duracion_scale.config(state=tk.NORMAL)
    else:
        duracion_scale.config(state=tk.DISABLED)


def toggle_filtro_escalas():
    if escalas_habilitado_var.get():
        escalas_spinbox.config(state=tk.NORMAL)
    else:
        escalas_spinbox.config(state=tk.DISABLED)


def toggle_filtro_horario():
    estado = tk.NORMAL if horario_habilitado_var.get() else tk.DISABLED
    hora_min_entry.config(state=estado)
    hora_max_entry.config(state=estado)


def resetear_filtros_antes_busqueda():
    precio_habilitado_var.set(False)
    duracion_habilitado_var.set(False)
    escalas_habilitado_var.set(False)
    horario_habilitado_var.set(False)
    precio_max_var.set(2000)
    duracion_max_var.set(24)
    escalas_max_var.set(2)
    hora_salida_min_var.set("00:00")
    hora_salida_max_var.set("23:59")

    precio_check.config(state=tk.DISABLED)
    duracion_check.config(state=tk.DISABLED)
    escalas_check.config(state=tk.DISABLED)
    horario_check.config(state=tk.DISABLED)
    precio_scale.config(state=tk.DISABLED)
    duracion_scale.config(state=tk.DISABLED)
    escalas_spinbox.config(state=tk.DISABLED)
    hora_min_entry.config(state=tk.DISABLED)
    hora_max_entry.config(state=tk.DISABLED)
    aplicar_filtros_button.config(state=tk.DISABLED)
    limpiar_filtros_button.config(state=tk.DISABLED)
    ordenar_precio_button.config(state=tk.DISABLED)
    ordenar_duracion_button.config(state=tk.DISABLED)
    ordenar_escalas_button.config(state=tk.DISABLED)


def iniciar_interfaz():
    global root, origen_combo, destino_combo, fecha_salida_entry, fecha_regreso_entry, fecha_regreso_var, resultados_text, buscar_button
    global precio_habilitado_var, duracion_habilitado_var, escalas_habilitado_var, horario_habilitado_var
    global precio_max_var, duracion_max_var, escalas_max_var, hora_salida_min_var, hora_salida_max_var
    global precio_scale, duracion_scale, escalas_spinbox, hora_min_entry, hora_max_entry
    global precio_check, duracion_check, escalas_check, horario_check
    global aplicar_filtros_button, limpiar_filtros_button
    global adultos_var, moneda_var, ordenar_precio_button, ordenar_duracion_button, ordenar_escalas_button
    global grafico_precios_button, grafico_aerolineas_button, grafico_distribucion_button
    global filtros_inner, herramientas_inner, filtros_visible, herramientas_visible

    root = tk.Tk()
    root.title("Comparador de Vuelos - Amadeus")
    root.geometry("950x750")
    root.configure(bg="#f0f0f0")

    filtros_visible = tk.BooleanVar(value=True)
    herramientas_visible = tk.BooleanVar(value=True)

    control_frame = tk.Frame(root, bg="#ffffff", relief=tk.RAISED, bd=2)
    control_frame.pack(fill=tk.X, padx=10, pady=10)

    titulo = tk.Label(control_frame, text="Buscador de Vuelos", font=("Arial", 16, "bold"), bg="#ffffff")
    titulo.pack(pady=10)

    inputs_frame = tk.Frame(control_frame, bg="#ffffff")
    inputs_frame.pack(fill=tk.X, padx=15, pady=10)
    tk.Label(inputs_frame, text="Origen:", font=("Arial", 10), bg="#ffffff").grid(row=0, column=0,
                                                                                  sticky="w", pady=5)
    origen_combo = ttk.Combobox(inputs_frame, values=[], font=("Arial", 10), width=30)
    origen_combo.grid(row=0, column=1, padx=5, sticky="w")
    origen_combo.set("")
    origen_combo.bind('<KeyRelease>', lambda event: filtrar_aeropuertos(event, origen_combo))
    tk.Label(inputs_frame, text="Escribe 3+ letras para buscar aeropuertos", font=("Arial", 8, "italic"), fg="gray",
             bg="#ffffff").grid(row=0,
                                column=2,
                                sticky="w")
    tk.Label(inputs_frame, text="Destino:", font=("Arial", 10), bg="#ffffff").grid(row=1, column=0,
                                                                                   sticky="w", pady=5)
    destino_combo = ttk.Combobox(inputs_frame, values=[], font=("Arial", 10), width=30)
    destino_combo.grid(row=1, column=1, padx=5, sticky="w")
    destino_combo.set("")
    destino_combo.bind('<KeyRelease>', lambda event: filtrar_aeropuertos(event, destino_combo))
    tk.Label(inputs_frame, text="Escribe 3+ letras para buscar aeropuertos", font=("Arial", 8, "italic"), fg="gray",
             bg="#ffffff").grid(row=1,
                                column=2,
                                sticky="w")
    tk.Label(inputs_frame, text="Fecha Salida:", font=("Arial", 10), bg="#ffffff").grid(row=2, column=0,
                                                                                        sticky="w", pady=5)
    fecha_salida_entry = DateEntry(inputs_frame, font=("Arial", 10), width=15,
                                   background='darkblue', foreground='white',
                                   borderwidth=2, date_pattern='yyyy-mm-dd',
                                   mindate=datetime.now())
    fecha_salida_entry.grid(row=2, column=1, padx=5, sticky="w")
    fecha_salida_entry.bind("<<DateEntrySelected>>", lambda e: actualizar_fecha_minima_regreso())
    tk.Label(inputs_frame, text="Selecciona con el calendario", font=("Arial", 8, "italic"), fg="gray",
             bg="#ffffff").grid(row=2,
                                column=2,
                                sticky="w")

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

    tk.Label(regreso_frame, text="Opcional: marca para viaje de ida y vuelta",
             font=("Arial", 8, "italic"), fg="gray", bg="#ffffff").pack(side=tk.LEFT, padx=5)

    adultos_var = tk.IntVar(value=1)

    adultos_frame = tk.Frame(inputs_frame, bg="#ffffff")
    adultos_frame.grid(row=4, column=0, columnspan=3, sticky="w", pady=5)

    tk.Label(adultos_frame, text="Adultos:", font=("Arial", 10), bg="#ffffff").pack(side=tk.LEFT, padx=(0, 5))

    adultos_spinbox = tk.Spinbox(adultos_frame, from_=1, to=9, textvariable=adultos_var,
                                 width=5, font=("Arial", 10))
    adultos_spinbox.pack(side=tk.LEFT, padx=5)

    tk.Label(adultos_frame, text="El precio total se calculará automáticamente",
             font=("Arial", 8, "italic"), fg="gray", bg="#ffffff").pack(side=tk.LEFT, padx=5)

    moneda_var = tk.StringVar(value="EUR")

    moneda_frame = tk.Frame(inputs_frame, bg="#ffffff")
    moneda_frame.grid(row=5, column=0, columnspan=3, sticky="w", pady=5)

    tk.Label(moneda_frame, text="Moneda:", font=("Arial", 10), bg="#ffffff").pack(side=tk.LEFT, padx=(0, 5))

    moneda_combo = ttk.Combobox(moneda_frame, textvariable=moneda_var, values=["EUR", "USD", "GBP"],
                                width=8, font=("Arial", 10), state="readonly")
    moneda_combo.pack(side=tk.LEFT, padx=5)

    tk.Label(moneda_frame, text="Selecciona la moneda para los precios",
             font=("Arial", 8, "italic"), fg="gray", bg="#ffffff").pack(side=tk.LEFT, padx=5)

    buscar_button = tk.Button(root, text="Buscar Vuelos", command=mostrar_resultados,
                              font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
                              padx=20, pady=10, cursor="hand2")
    buscar_button.pack(pady=10)

    def toggle_filtros():
        if filtros_visible.get():
            filtros_inner.pack_forget()
            filtros_visible.set(False)
            toggle_filtros_btn.config(text="▼ Mostrar Filtros")
        else:
            filtros_inner.pack(fill=tk.X, padx=10, pady=10)
            filtros_visible.set(True)
            toggle_filtros_btn.config(text="▲ Ocultar Filtros")

    def toggle_herramientas():
        if herramientas_visible.get():
            herramientas_inner.pack_forget()
            herramientas_visible.set(False)
            toggle_herramientas_btn.config(text="▼ Mostrar Herramientas")
        else:
            herramientas_inner.pack(fill=tk.X, padx=10, pady=10)
            herramientas_visible.set(True)
            toggle_herramientas_btn.config(text="▲ Ocultar Herramientas")

    filtros_frame = tk.Frame(root, bg="#ffffff", relief=tk.RAISED, bd=2)
    filtros_frame.pack(fill=tk.X, padx=10, pady=5)

    filtros_header = tk.Frame(filtros_frame, bg="#ffffff")
    filtros_header.pack(fill=tk.X, padx=5, pady=5)

    tk.Label(filtros_header, text="Filtros de Búsqueda", font=("Arial", 11, "bold"), bg="#ffffff").pack(side=tk.LEFT)

    toggle_filtros_btn = tk.Button(filtros_header, text="▲ Ocultar Filtros",
                                   command=toggle_filtros, font=("Arial", 8),
                                   bg="#e0e0e0", cursor="hand2", padx=5, pady=2)
    toggle_filtros_btn.pack(side=tk.RIGHT)

    precio_habilitado_var = tk.BooleanVar(value=False)
    duracion_habilitado_var = tk.BooleanVar(value=False)
    escalas_habilitado_var = tk.BooleanVar(value=False)
    precio_max_var = tk.IntVar(value=2000)
    duracion_max_var = tk.IntVar(value=24)
    escalas_max_var = tk.IntVar(value=2)

    filtros_inner = tk.Frame(filtros_frame, bg="#ffffff")
    filtros_inner.pack(fill=tk.X, padx=10, pady=10)

    precio_frame = tk.Frame(filtros_inner, bg="#ffffff")
    precio_frame.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    precio_check = tk.Checkbutton(precio_frame, text="Precio máximo:", variable=precio_habilitado_var,
                                  font=("Arial", 10), bg="#ffffff", state=tk.DISABLED,
                                  command=toggle_filtro_precio)
    precio_check.pack(side=tk.LEFT)

    precio_scale = tk.Scale(precio_frame, from_=50, to=5000, orient=tk.HORIZONTAL,
                            variable=precio_max_var, length=200, font=("Arial", 9),
                            bg="#ffffff", state=tk.DISABLED)
    precio_scale.pack(side=tk.LEFT, padx=5)

    tk.Label(precio_frame, text="EUR", font=("Arial", 10), bg="#ffffff").pack(side=tk.LEFT)

    duracion_frame = tk.Frame(filtros_inner, bg="#ffffff")
    duracion_frame.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    duracion_check = tk.Checkbutton(duracion_frame, text="Duración máxima:", variable=duracion_habilitado_var,
                                    font=("Arial", 10), bg="#ffffff", state=tk.DISABLED,
                                    command=toggle_filtro_duracion)
    duracion_check.pack(side=tk.LEFT)

    duracion_scale = tk.Scale(duracion_frame, from_=1, to=48, orient=tk.HORIZONTAL,
                              variable=duracion_max_var, length=200, font=("Arial", 9),
                              bg="#ffffff", state=tk.DISABLED)
    duracion_scale.pack(side=tk.LEFT, padx=5)

    tk.Label(duracion_frame, text="horas", font=("Arial", 10), bg="#ffffff").pack(side=tk.LEFT)

    escalas_frame = tk.Frame(filtros_inner, bg="#ffffff")
    escalas_frame.grid(row=1, column=0, padx=10, pady=5, sticky="w")

    escalas_check = tk.Checkbutton(escalas_frame, text="Escalas máximas:", variable=escalas_habilitado_var,
                                   font=("Arial", 10), bg="#ffffff", state=tk.DISABLED,
                                   command=toggle_filtro_escalas)
    escalas_check.pack(side=tk.LEFT)

    escalas_spinbox = tk.Spinbox(escalas_frame, from_=0, to=5, textvariable=escalas_max_var,
                                 width=5, font=("Arial", 10), state=tk.DISABLED)
    escalas_spinbox.pack(side=tk.LEFT, padx=5)

    horario_habilitado_var = tk.BooleanVar(value=False)
    hora_salida_min_var = tk.StringVar(value="00:00")
    hora_salida_max_var = tk.StringVar(value="23:59")

    horario_frame = tk.Frame(filtros_inner, bg="#ffffff")
    horario_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w")

    horario_check = tk.Checkbutton(horario_frame, text="Horario de salida:", variable=horario_habilitado_var,
                                   font=("Arial", 10), bg="#ffffff", state=tk.DISABLED,
                                   command=toggle_filtro_horario)
    horario_check.pack(side=tk.LEFT)

    tk.Label(horario_frame, text="Desde:", font=("Arial", 9), bg="#ffffff").pack(side=tk.LEFT, padx=(10, 5))

    hora_min_entry = tk.Entry(horario_frame, textvariable=hora_salida_min_var, width=6, font=("Arial", 10),
                              state=tk.DISABLED)
    hora_min_entry.pack(side=tk.LEFT, padx=5)

    tk.Label(horario_frame, text="(HH:MM)", font=("Arial", 8, "italic"), fg="gray", bg="#ffffff").pack(side=tk.LEFT,
                                                                                                       padx=2)

    tk.Label(horario_frame, text="Hasta:", font=("Arial", 9), bg="#ffffff").pack(side=tk.LEFT, padx=(10, 5))

    hora_max_entry = tk.Entry(horario_frame, textvariable=hora_salida_max_var, width=6, font=("Arial", 10),
                              state=tk.DISABLED)
    hora_max_entry.pack(side=tk.LEFT, padx=5)

    tk.Label(horario_frame, text="(HH:MM)", font=("Arial", 8, "italic"), fg="gray", bg="#ffffff").pack(side=tk.LEFT,
                                                                                                       padx=2)

    botones_filtros_frame = tk.Frame(filtros_inner, bg="#ffffff")
    botones_filtros_frame.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    aplicar_filtros_button = tk.Button(botones_filtros_frame, text="Aplicar Filtros",
                                       command=aplicar_filtros, font=("Arial", 10, "bold"),
                                       bg="#2196F3", fg="white", padx=15, pady=5,
                                       cursor="hand2", state=tk.DISABLED)
    aplicar_filtros_button.pack(side=tk.LEFT, padx=5)

    limpiar_filtros_button = tk.Button(botones_filtros_frame, text="Limpiar Filtros",
                                       command=limpiar_filtros, font=("Arial", 10),
                                       bg="#FF9800", fg="white", padx=15, pady=5,
                                       cursor="hand2", state=tk.DISABLED)
    limpiar_filtros_button.pack(side=tk.LEFT, padx=5)

    herramientas_frame = tk.Frame(root, bg="#ffffff", relief=tk.RAISED, bd=2)
    herramientas_frame.pack(fill=tk.X, padx=10, pady=5)

    herramientas_header = tk.Frame(herramientas_frame, bg="#ffffff")
    herramientas_header.pack(fill=tk.X, padx=5, pady=5)

    tk.Label(herramientas_header, text="Herramientas", font=("Arial", 11, "bold"), bg="#ffffff").pack(side=tk.LEFT)

    toggle_herramientas_btn = tk.Button(herramientas_header, text="▲ Ocultar Herramientas",
                                        command=toggle_herramientas, font=("Arial", 8),
                                        bg="#e0e0e0", cursor="hand2", padx=5, pady=2)
    toggle_herramientas_btn.pack(side=tk.RIGHT)

    herramientas_inner = tk.Frame(herramientas_frame, bg="#ffffff")
    herramientas_inner.pack(fill=tk.X, padx=10, pady=10)

    tk.Label(herramientas_inner, text="Ordenar por:", font=("Arial", 10, "bold"), bg="#ffffff").pack(side=tk.LEFT,
                                                                                                     padx=(0, 10))

    ordenar_precio_button = tk.Button(herramientas_inner, text="Precio",
                                      command=lambda: [controller.ordenar_vuelos("precio"), mostrar_vuelos_filtrados()],
                                      font=("Arial", 9), bg="#E3F2FD", fg="#1976D2",
                                      padx=10, pady=3, cursor="hand2", state=tk.DISABLED)
    ordenar_precio_button.pack(side=tk.LEFT, padx=2)

    ordenar_duracion_button = tk.Button(herramientas_inner, text="Duración",
                                        command=lambda: [controller.ordenar_vuelos("duracion"),
                                                         mostrar_vuelos_filtrados()],
                                        font=("Arial", 9), bg="#E8F5E9", fg="#388E3C",
                                        padx=10, pady=3, cursor="hand2", state=tk.DISABLED)
    ordenar_duracion_button.pack(side=tk.LEFT, padx=2)

    ordenar_escalas_button = tk.Button(herramientas_inner, text="Escalas",
                                       command=lambda: [controller.ordenar_vuelos("escalas"),
                                                        mostrar_vuelos_filtrados()],
                                       font=("Arial", 9), bg="#FFF3E0", fg="#F57C00",
                                       padx=10, pady=3, cursor="hand2", state=tk.DISABLED)
    ordenar_escalas_button.pack(side=tk.LEFT, padx=2)

    tk.Label(herramientas_inner, text="|", font=("Arial", 12), bg="#ffffff", fg="#cccccc").pack(side=tk.LEFT, padx=10)

    tk.Label(herramientas_inner, text="Gráficos:", font=("Arial", 10, "bold"), bg="#ffffff").pack(side=tk.LEFT,
                                                                                                  padx=(0, 10))

    grafico_precios_button = tk.Button(herramientas_inner, text="Tendencia de Precios",
                                       command=mostrar_grafico_precios,
                                       font=("Arial", 9), bg="#F3E5F5", fg="#7B1FA2",
                                       padx=10, pady=3, cursor="hand2", state=tk.DISABLED)
    grafico_precios_button.pack(side=tk.LEFT, padx=2)

    grafico_aerolineas_button = tk.Button(herramientas_inner, text="Comparar Aerolíneas",
                                          command=mostrar_grafico_aerolineas,
                                          font=("Arial", 9), bg="#E0F2F1", fg="#00695C",
                                          padx=10, pady=3, cursor="hand2", state=tk.DISABLED)
    grafico_aerolineas_button.pack(side=tk.LEFT, padx=2)

    grafico_distribucion_button = tk.Button(herramientas_inner, text="Distribución",
                                            command=mostrar_grafico_distribucion,
                                            font=("Arial", 9), bg="#FFF9C4", fg="#F57F17",
                                            padx=10, pady=3, cursor="hand2", state=tk.DISABLED)
    grafico_distribucion_button.pack(side=tk.LEFT, padx=2)

    resultado_frame = tk.Frame(root, bg="#ffffff", relief=tk.SUNKEN, bd=2)
    resultado_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    tk.Label(resultado_frame, text="Resultados:", font=("Arial", 10, "bold"), bg="#ffffff").pack(anchor="w", padx=5,
                                                                                                 pady=5)

    scrollbar = tk.Scrollbar(resultado_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    resultados_text = Text(resultado_frame, height=20, width=80, font=("Arial", 9),
                           yscrollcommand=scrollbar.set, bg="#fafafa", wrap=tk.WORD)
    resultados_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    resultados_text.config(state=tk.DISABLED)
    scrollbar.config(command=resultados_text.yview)

    footer = tk.Label(root, text="Adultos: 1-9 | Filtros | Ordenar | Estadísticas automáticas",
                      font=("Arial", 8, "italic"), fg="gray", bg="#f0f0f0")
    footer.pack(pady=5)

    root.mainloop()