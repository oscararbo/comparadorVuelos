from api_handler import buscar_vuelos

def main():
    print("Bienvenido al Comparador de Vuelos")
    origen = input("Introduce el lugar de origen: ")
    destino = input("Introduce el lugar de destino: ")
    fecha_salida = input("Introduce la fecha de salida (YYYY-MM-DD): ")
    fecha_regreso = input("Introduce la fecha de regreso (YYYY-MM-DD): ")

    resultados = buscar_vuelos(origen, destino, fecha_salida, fecha_regreso)

    if resultados:
        print("\nResultados de vuelos encontrados:")
        for vuelo in resultados:
            print(vuelo)
    else:
        print("No se encontraron vuelos para los criterios ingresados")

if __name__ == "__main__":
    main()
