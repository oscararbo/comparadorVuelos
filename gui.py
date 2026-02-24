import tkinter as tk
from tkinter import Text, messagebox, ttk
from api_handler import buscar_vuelos
import threading


def mostrar_resultados():
    origen = origen_entry.get().strip().upper()
    destino = destino_entry.get().strip().upper()
    fecha_salida = fecha_salida_entry.get().strip()
    fecha_regreso = fecha_regreso_entry.get().strip()

    # Validar campos
    if not origen or not destino or not fecha_salida:
        messagebox.showerror("Error", "Por favor completa todos los campos requeridos")
        return

    if len(origen) != 3 or len(destino) != 3:
        messagebox.showerror("Error", "Los códigos de aeropuerto deben tener 3 caracteres (ej: MAD, BCN)")
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
    global root, origen_entry, destino_entry, fecha_salida_entry, fecha_regreso_entry, resultados_text, buscar_button

    root = tk.Tk()
    root.title("Comparador de Vuelos - Skyscanner")
    root.geometry("800x700")
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
    tk.Label(inputs_frame, text="Origen (código IATA):", font=("Arial", 10), bg="#ffffff").grid(row=0, column=0,
                                                                                                sticky="w", pady=5)
    origen_entry = tk.Entry(inputs_frame, font=("Arial", 10), width=15)
    origen_entry.grid(row=0, column=1, padx=5, sticky="w")
    tk.Label(inputs_frame, text="Ej: MAD, BCN, SVQ", font=("Arial", 8, "italic"), fg="gray", bg="#ffffff").grid(row=0,
                                                                                                                column=2,
                                                                                                                sticky="w")

    # Destino
    tk.Label(inputs_frame, text="Destino (código IATA):", font=("Arial", 10), bg="#ffffff").grid(row=1, column=0,
                                                                                                 sticky="w", pady=5)
    destino_entry = tk.Entry(inputs_frame, font=("Arial", 10), width=15)
    destino_entry.grid(row=1, column=1, padx=5, sticky="w")
    tk.Label(inputs_frame, text="Ej: MAD, BCN, SVQ", font=("Arial", 8, "italic"), fg="gray", bg="#ffffff").grid(row=1,
                                                                                                                column=2,
                                                                                                                sticky="w")

    # Fecha de Salida
    tk.Label(inputs_frame, text="Fecha Salida (YYYY-MM-DD):", font=("Arial", 10), bg="#ffffff").grid(row=2, column=0,
                                                                                                     sticky="w", pady=5)
    fecha_salida_entry = tk.Entry(inputs_frame, font=("Arial", 10), width=15)
    fecha_salida_entry.grid(row=2, column=1, padx=5, sticky="w")
    tk.Label(inputs_frame, text="Ej: 2024-12-25", font=("Arial", 8, "italic"), fg="gray", bg="#ffffff").grid(row=2,
                                                                                                             column=2,
                                                                                                             sticky="w")

    # Fecha de Regreso (opcional)
    tk.Label(inputs_frame, text="Fecha Regreso (opcional):", font=("Arial", 10), bg="#ffffff").grid(row=3, column=0,
                                                                                                    sticky="w", pady=5)
    fecha_regreso_entry = tk.Entry(inputs_frame, font=("Arial", 10), width=15)
    fecha_regreso_entry.grid(row=3, column=1, padx=5, sticky="w")
    tk.Label(inputs_frame, text="Dejar vacío para ida y vuelta", font=("Arial", 8, "italic"), fg="gray",
             bg="#ffffff").grid(row=3, column=2, sticky="w")

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
    footer = tk.Label(root, text="Asegúrate de haber configurado tu API Key de Skyscanner en api_handler.py",
                      font=("Arial", 8, "italic"), fg="gray", bg="#f0f0f0")
    footer.pack(pady=5)

    # Iniciar el bucle principal de la interfaz
    root.mainloop()