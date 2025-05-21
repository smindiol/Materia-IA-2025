import math
import copy

X = "X"
O = "O"
VACIO = None
 
def estado_inicial():
    return [[VACIO, VACIO, VACIO],
            [VACIO, VACIO, VACIO],
            [VACIO, VACIO, VACIO]]

def jugador(tablero):
    x_count = sum(fila.count(X) for fila in tablero)
    o_count = sum(fila.count(O) for fila in tablero)
    return X if x_count == o_count else O

def acciones(tablero):
    return {(i, j) for i in range(3) for j in range(3) if tablero[i][j] == VACIO}

def resultado(tablero, accion):
    if tablero[accion[0]][accion[1]] is not VACIO:
        raise ValueError("Acción inválida")
    nuevo_tablero = copy.deepcopy(tablero)
    nuevo_tablero[accion[0]][accion[1]] = jugador(tablero)
    return nuevo_tablero

def ganador(tablero):
    # Filas
    for fila in tablero:
        if fila[0] == fila[1] == fila[2] and fila[0] is not VACIO:
            return fila[0]
    # Columnas
    for j in range(3):
        if tablero[0][j] == tablero[1][j] == tablero[2][j] and tablero[0][j] is not VACIO:
            return tablero[0][j]
    # Diagonales
    if tablero[0][0] == tablero[1][1] == tablero[2][2] and tablero[0][0] is not VACIO:
        return tablero[0][0]
    if tablero[0][2] == tablero[1][1] == tablero[2][0] and tablero[0][2] is not VACIO:
        return tablero[0][2]
    return None

def final(tablero):
    return ganador(tablero) is not None or all(celda is not VACIO for fila in tablero for celda in fila)

def utilidad(tablero):
    w = ganador(tablero)
    if w == X:
        return 1
    elif w == O:
        return -1
    else:
        return 0

def minimax(tablero):
    if final(tablero):
        return None

    turno = jugador(tablero)

    def max_valor(tablero, alpha, beta):
        if final(tablero):
            return utilidad(tablero), None
        v = -math.inf
        mejor_mov = None
        for accion in acciones(tablero):
            val, _ = min_valor(resultado(tablero, accion), alpha, beta)
            if val > v:
                v = val
                mejor_mov = accion
                alpha = max(alpha, v)
            if beta <= alpha:
                break  # poda beta
        return v, mejor_mov

    def min_valor(tablero, alpha, beta):
        if final(tablero):
            return utilidad(tablero), None
        v = math.inf
        mejor_mov = None
        for accion in acciones(tablero):
            val, _ = max_valor(resultado(tablero, accion), alpha, beta)
            if val < v:
                v = val
                mejor_mov = accion
                beta = min(beta, v)
            if beta <= alpha:
                break  # poda alfa
        return v, mejor_mov

    if turno == X:
        _, accion = max_valor(tablero, -math.inf, math.inf)
    else:
        _, accion = min_valor(tablero, -math.inf, math.inf)
    return accion

