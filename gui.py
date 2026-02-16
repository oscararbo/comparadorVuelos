import tkinter as tk
from tkinter import Text
from api_handler import buscar_vuelos

def mostrar_resultados():
    origen = origen_entry.get()
    destino = destino_entry.get()
    fecha_salida = fecha_salida_entry.get()
    fecha_regreso = fecha_regreso_entry.get()

    resultados = buscar_vuelos(origen, destino, fecha_salida, fecha_regreso)

    # Limpiar el área de texto antes de mostrar nuevos resultados
    resultados_text.delete(1.0, tk.END)
    if resultados:
        for vuelo in resultados:
            resultados_text.insert(tk.END, f"{vuelo}\n")
    else:
        resultados_text.insert(tk.END, "No se encontraron vuelos para los criterios ingresados.")

def iniciar_interfaz():
    root = tk.Tk()
    root.title("Comparador de Vuelos")

    # Etiquetas y campos de entrada para los criterios de búsqueda
    tk.Label(root, text="Origen:").grid(row=0, column=0)
    global origen_entry
    origen_entry = tk.Entry(root)
    origen_entry.grid(row=0, column=1)

    tk.Label(root, text="Destino:").grid(row=1, column=0)
    global destino_entry
    destino_entry = tk.Entry(root)
    destino_entry.grid(row=1, column=1)

    tk.Label(root, text="Fecha de Salida (YYYY-MM-DD):").grid(row=2, column=0)
    global fecha_salida_entry
    fecha_salida_entry = tk.Entry(root)
    fecha_salida_entry.grid(row=2, column=1)

    tk.Label(root, text="Fecha de Regreso (YYYY-MM-DD):").grid(row=3, column=0)
    global fecha_regreso_entry
    fecha_regreso_entry = tk.Entry(root)
    fecha_regreso_entry.grid(row=3, column=1)

    # Botón para buscar vuelos
    buscar_button = tk.Button(root, text="Buscar Vuelos", command=mostrar_resultados)
    buscar_button.grid(row=4, columnspan=2)

    # Área de texto para mostrar los resultados
    global resultados_text
    resultados_text = Text(root, height=10, width=50)
    resultados_text.grid(row=5, columnspan=2)

    # Iniciar el bucle principal de la interfaz
    root.mainloop()
