from astar import AStar

def crear_matriz(f, c):
    """Crea una matriz de f filas y c columnas"""
    matriz = [['.' for _ in range(c)] for _ in range(f)]
    for fila in matriz:
        print(" ".join(fila))
    return matriz

def obtener_obstaculos():
    """Solicita las posiciones de los obstáculos al usuario"""
    posiciones = []
    while True:
        entrada = input("Por favor ingrese la posición del obstáculo 'fila,columna' o 's' para terminar: ")
        if entrada.lower() == 's':
            break
        try:
            fila, columna = map(int, entrada.split(',')) #convertimos str a int generados por split, por map
            posiciones.append((fila, columna))
        except ValueError:
            print("Entrada no válida. Por favor, ingrese de nuevo en el formato 'fila,columna'.")
    return posiciones

def agregar_obstaculos(matriz, posiciones):
    """Agrega obstáculos a la matriz"""
    for fila, columna in posiciones:
        if 0 <= fila < len(matriz) and 0 <= columna < len(matriz[0]):
            matriz[fila][columna] = 'O'
    return matriz

def obtener_coordenada(tipo):
    """Solicita una coordenada del usuario para entrada o salida"""
    while True:
        entrada = input(f"Ingrese la posición de la {tipo} en el formato 'fila,columna': ")
        try:
            fila, columna = map(int, entrada.split(','))
            return (fila, columna)
        except ValueError:
            print("Entrada no válida. Por favor, ingrese de nuevo en el formato 'fila,columna'.")

def agregar_entrada_salida(matriz, entrada, salida):
    """Agrega la entrada y salida a la matriz"""
    if 0 <= entrada[0] < len(matriz) and 0 <= entrada[1] < len(matriz[0]):
        matriz[entrada[0]][entrada[1]] = 'E'  # Usamos 'E' para representar la entrada
    if 0 <= salida[0] < len(matriz) and 0 <= salida[1] < len(matriz[0]):
        matriz[salida[0]][salida[1]] = 'S'  # Usamos 'S' para representar la salida
    return matriz

def heuristica(posicion_actual, salida):
    """Calcula la distancia Manhattan desde la posición actual hasta la salida"""
    return abs(posicion_actual[0] - salida[0]) + abs(posicion_actual[1] - salida[1])

def mostrar_matriz(matriz):
    """Imprime la matriz"""
    for fila in matriz:
        print(" ".join(fila))
    print()

def encontrar_vecinos(matriz, nodo):
    """Encuentra los vecinos de un nodo que no sean obstáculos"""
    x, y = nodo
    vecinos = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(matriz) and 0 <= ny < len(matriz[0]) and matriz[nx][ny] != 'O':
            vecinos.append((nx, ny))
    return vecinos

def reconstruir_camino(came_from, inicio, meta):
    """Reconstruye el camino desde el inicio hasta la meta"""
    actual = meta
    camino = [actual]
    while actual != inicio:
        actual = came_from[actual]
        camino.append(actual)
    camino.reverse()
    return camino

def a_star(matriz, entrada, salida):
    """Implementa el algoritmo A* usando la biblioteca AStar"""
    conjunto_abierto = {entrada}
    de_donde_viene = {}

    g_score = {entrada: 0}
    f_score = {entrada: heuristica(entrada, salida)}

    while conjunto_abierto:
        actual = min(conjunto_abierto, key=lambda x: f_score.get(x, float('inf')))
        if actual == salida:
            return reconstruir_camino(de_donde_viene, entrada, salida)

        conjunto_abierto.remove(actual)
        for vecino in encontrar_vecinos(matriz, actual):
            puntaje_g_tentativo = g_score[actual] + 1
            if puntaje_g_tentativo < g_score.get(vecino, float('inf')):
                de_donde_viene[vecino] = actual
                g_score[vecino] = puntaje_g_tentativo
                f_score[vecino] = g_score[vecino] + heuristica(vecino, salida)
                if vecino not in conjunto_abierto:
                    conjunto_abierto.add(vecino)
    
    return []  # Retorna una lista vacía si no se encuentra un camino

def main():
    filas, columnas = 5, 5  # Tamaño de la matriz
    matriz = crear_matriz(filas, columnas)
    
    print("Ingrese las posiciones de los obstáculos.")
    posiciones_obstaculos = obtener_obstaculos()
    matriz = agregar_obstaculos(matriz, posiciones_obstaculos)
    
    entrada = obtener_coordenada("entrada")
    salida = obtener_coordenada("salida")
    matriz = agregar_entrada_salida(matriz, entrada, salida)
    
    mostrar_matriz(matriz)
    
    print(f"Distancia heurística desde la entrada hasta la salida: {heuristica(entrada, salida)}")
    
    camino = a_star(matriz, entrada, salida)
    if camino:
        print("Recorrido:")
        for paso in camino:
            print(paso)
        for (f, c) in camino:
            if matriz[f][c] not in ['E', 'S']:
                matriz[f][c] = '*'
    else:
        print("No se encontró un camino.")

    mostrar_matriz(matriz)

if __name__ == "__main__":
    main()
