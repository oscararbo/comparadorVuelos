import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.lines import Line2D
import matplotlib

matplotlib.use('TkAgg')


def graficar_precios(vuelos, moneda="EUR"):
    if not vuelos:
        return None

    precios = [v["precio"] for v in vuelos]
    indices = list(range(1, len(precios) + 1))

    fig, ax = plt.subplots(figsize=(10, 6))

    # Línea de precios con marcadores más visibles
    ax.plot(indices, precios, marker='o', linestyle='-', color='#1976D2',
            linewidth=3, markersize=8, markerfacecolor='#2196F3',
            markeredgecolor='white', markeredgewidth=2, label='Precio por vuelo')

    # Área sombreada bajo la curva
    ax.fill_between(indices, precios, alpha=0.2, color='#2196F3')

    # Estadísticas
    precio_promedio = sum(precios) / len(precios)
    precio_min = min(precios)
    precio_max = max(precios)

    # Línea de precio promedio más visible
    ax.axhline(y=precio_promedio, color='#FF5722', linestyle='--', linewidth=2.5,
               label=f'Precio Promedio: {precio_promedio:.2f} {moneda}')

    # Marcar precio mínimo y máximo
    idx_min = precios.index(precio_min)
    idx_max = precios.index(precio_max)
    ax.scatter([idx_min + 1], [precio_min], color='#4CAF50', s=200, zorder=5,
               marker='v', edgecolors='white', linewidths=2, label=f'Mínimo: {precio_min:.2f} {moneda}')
    ax.scatter([idx_max + 1], [precio_max], color='#F44336', s=200, zorder=5,
               marker='^', edgecolors='white', linewidths=2, label=f'Máximo: {precio_max:.2f} {moneda}')

    # Etiquetas y título más grandes
    ax.set_xlabel('Número de Vuelo', fontsize=14, fontweight='bold')
    ax.set_ylabel(f'Precio ({moneda})', fontsize=14, fontweight='bold')
    ax.set_title('TENDENCIA DE PRECIOS DE VUELOS', fontsize=16, fontweight='bold', pad=20)

    # Grid mejorado
    ax.grid(True, alpha=0.4, linestyle='--', linewidth=0.8)
    ax.set_axisbelow(True)

    # Leyenda más clara
    ax.legend(fontsize=11, loc='best', framealpha=0.95, edgecolor='black')

    # Mejorar los ticks
    ax.tick_params(axis='both', labelsize=11)

    fig.tight_layout()
    return fig


def graficar_aerolineas(vuelos, moneda="EUR"):
    if not vuelos:
        return None

    # Extraer aerolíneas y precios
    aerolineas_precios = {}
    for vuelo in vuelos:
        try:
            # Obtener código de aerolínea del primer segmento
            aerolinea = vuelo["itineraries"][0]["segmentos"][0]["aerolinea"]
            precio = vuelo["precio"]

            if aerolinea not in aerolineas_precios:
                aerolineas_precios[aerolinea] = []
            aerolineas_precios[aerolinea].append(precio)
        except (IndexError, KeyError):
            continue

    if not aerolineas_precios:
        return None

    # Calcular estadísticas por aerolínea
    aerolineas = list(aerolineas_precios.keys())
    precios_promedio = [sum(precios) / len(precios) for precios in aerolineas_precios.values()]
    cantidad_vuelos = [len(precios) for precios in aerolineas_precios.values()]

    # Ordenar por precio promedio
    datos_ordenados = sorted(zip(aerolineas, precios_promedio, cantidad_vuelos),
                             key=lambda x: x[1])
    aerolineas, precios_promedio, cantidad_vuelos = zip(*datos_ordenados)

    fig, ax = plt.subplots(figsize=(10, 6))

    # Colores degradados del más barato al más caro
    colores = plt.cm.RdYlGn_r(range(0, 256, 256 // len(aerolineas)))

    bars = ax.barh(aerolineas, precios_promedio, color=colores,
                   alpha=0.8, edgecolor='black', linewidth=1.5)

    # Añadir valores y cantidad de vuelos en las barras
    for i, (bar, precio, cantidad) in enumerate(zip(bars, precios_promedio, cantidad_vuelos)):
        width = bar.get_width()
        ax.text(width + max(precios_promedio) * 0.02, bar.get_y() + bar.get_height() / 2.,
                f'{precio:.2f} {moneda}\n({cantidad} vuelo{"s" if cantidad > 1 else ""})',
                ha='left', va='center', fontsize=11, fontweight='bold')

    ax.set_xlabel(f'Precio Promedio ({moneda})', fontsize=14, fontweight='bold')
    ax.set_ylabel('Aerolínea', fontsize=14, fontweight='bold')
    ax.set_title('COMPARACIÓN DE PRECIOS POR AEROLÍNEA', fontsize=16, fontweight='bold', pad=20)

    # Grid mejorado
    ax.grid(True, axis='x', alpha=0.4, linestyle='--', linewidth=0.8)
    ax.set_axisbelow(True)

    # Mejorar los ticks
    ax.tick_params(axis='both', labelsize=12)

    # Ajustar límites para que se vean las etiquetas
    ax.set_xlim(0, max(precios_promedio) * 1.25)

    fig.tight_layout()
    return fig


def graficar_distribucion(vuelos, moneda="EUR"):
    if not vuelos:
        return None

    precios = [v["precio"] for v in vuelos]

    fig, ax = plt.subplots(figsize=(10, 6))

    # Crear histograma con más bins si hay suficientes datos
    num_bins = min(15, max(5, len(precios) // 3))
    n, bins, patches = ax.hist(precios, bins=num_bins,
                               color='#FF9800', alpha=0.7,
                               edgecolor='black', linewidth=1.5)

    # Colorear las barras con un gradiente
    for i, patch in enumerate(patches):
        color_intensity = i / len(patches)
        patch.set_facecolor(plt.cm.YlOrRd(color_intensity * 0.7 + 0.3))

    # Estadísticas
    precio_promedio = sum(precios) / len(precios)
    precio_central = sorted(precios)[len(precios) // 2]
    precio_min = min(precios)
    precio_max = max(precios)

    # Líneas verticales para estadísticas más visibles
    ax.axvline(precio_promedio, color='#D32F2F', linestyle='--', linewidth=3,
               label=f'Promedio: {precio_promedio:.2f} {moneda}', zorder=5)
    ax.axvline(precio_central, color='#1976D2', linestyle='--', linewidth=3,
               label=f'Precio Central: {precio_central:.2f} {moneda}', zorder=5)

    # Etiquetas y título más grandes
    ax.set_xlabel(f'Rango de Precios ({moneda})', fontsize=14, fontweight='bold')
    ax.set_ylabel('Cantidad de Vuelos', fontsize=14, fontweight='bold')
    ax.set_title('DISTRIBUCIÓN DE PRECIOS', fontsize=16, fontweight='bold', pad=20)

    # Grid mejorado
    ax.grid(True, axis='y', alpha=0.4, linestyle='--', linewidth=0.8)
    ax.set_axisbelow(True)

    # Leyenda mejorada con más información
    leyenda_texto = [
        f'Promedio: {precio_promedio:.2f} {moneda}',
        f'Precio Central: {precio_central:.2f} {moneda}',
        f'Mínimo: {precio_min:.2f} {moneda}',
        f'Máximo: {precio_max:.2f} {moneda}',
        f'Total vuelos: {len(precios)}'
    ]

    # Crear leyenda personalizada
    legend_elements = [
        Line2D([0], [0], color='#D32F2F', linewidth=3, linestyle='--', label=leyenda_texto[0]),
        Line2D([0], [0], color='#1976D2', linewidth=3, linestyle='--', label=leyenda_texto[1])
    ]
    ax.legend(handles=legend_elements, fontsize=11, loc='best', framealpha=0.95, edgecolor='black')

    # Añadir texto con estadísticas adicionales
    stats_text = f'Rango: {precio_min:.2f} - {precio_max:.2f} {moneda}\n'
    stats_text += f'Total: {len(precios)} vuelos'
    ax.text(0.98, 0.97, stats_text, transform=ax.transAxes,
            fontsize=11, verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    # Mejorar los ticks
    ax.tick_params(axis='both', labelsize=11)

    fig.tight_layout()
    return fig


def mostrar_grafico_en_ventana(figura, titulo="Gráfico"):
    import tkinter as tk
    from tkinter import ttk

    ventana = tk.Toplevel()
    ventana.title(titulo)
    ventana.geometry("1100x700")
    ventana.configure(bg='white')

    # Frame para el canvas
    frame_canvas = tk.Frame(ventana, bg='white')
    frame_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    canvas = FigureCanvasTkAgg(figura, master=frame_canvas)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Frame para botones
    frame_botones = tk.Frame(ventana, bg='white')
    frame_botones.pack(pady=10)

    # Botón para cerrar más visible
    btn_cerrar = ttk.Button(frame_botones, text="Cerrar", command=ventana.destroy)
    btn_cerrar.pack(pady=5)

    # Centrar ventana
    ventana.update_idletasks()
    width = ventana.winfo_width()
    height = ventana.winfo_height()
    x = (ventana.winfo_screenwidth() // 2) - (width // 2)
    y = (ventana.winfo_screenheight() // 2) - (height // 2)
    ventana.geometry(f'{width}x{height}+{x}+{y}')