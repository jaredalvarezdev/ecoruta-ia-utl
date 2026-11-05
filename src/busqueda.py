"""
Busqueda UCS para EcoRuta IA (EcoCampus)

"""

from heapq import heappush, heappop
from itertools import count
from modelo import Accion, Estado, Problema, Nodo

def buscar_ucs(problema):
    """Implementación de Uniform Cost Search (UCS)."""
    meta = problema.estados_objetivos[0].nombre
    raiz = Nodo(problema.estado_inicial)
    contador = count()
    # Cola de prioridad ordenada por el costo acumulado g(n)
    frontera = [(raiz.coste, next(contador), raiz)]
    mejor_g = {raiz.estado.nombre: raiz.coste}
    explorados = set()
    orden = []

    print('\n=== BÚSQUEDA POR COSTO UNIFORME (UCS) - ECOCAMPUS ===')
    print(f'{"Ubicación / Estado":<25} {"g(n) (Costo Acumulado)":>22}')
    print('-' * 50)

    while frontera:
        _, _, nodo = heappop(frontera)
        lugar = nodo.estado.nombre

        if lugar in explorados or nodo.coste != mejor_g.get(lugar):
            continue

        g = nodo.coste
        print(f'{lugar:<25} {g:>22}')
        orden.append(lugar)
        explorados.add(lugar)

        if lugar == meta:
            return nodo, orden

        for hijo in nodo.expandir(problema):
            vecino = hijo.estado.nombre
            if vecino not in explorados and hijo.coste < mejor_g.get(vecino, float('inf')):
                mejor_g[vecino] = hijo.coste
                heappush(frontera, (hijo.coste, next(contador), hijo))

    return None, orden


def mostrar_resultado(solucion, orden):
    if solucion is None:
        print('\nNo se encontró ruta.')
        return
    ruta = []
    actual = solucion
    while actual is not None:
        ruta.append(actual.estado.nombre)
        actual = actual.padre
    print('\n--- RESULTADO ÓPTIMO ---')
    print('Ruta encontrada:', ' -> '.join(reversed(ruta)))
    print('Costo total:', solucion.coste, 'metros')
    print('Nodos explorados:', len(orden))
    print('Orden de expansión:', ' -> '.join(orden))