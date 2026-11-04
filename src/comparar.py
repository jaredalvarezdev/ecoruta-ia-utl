"""
Módulo: comparar.py
Proyecto: EcoRuta IA - UTL

Ejecuta las 3 pruebas (UCS, A* H1 y A* H2) con el mismo inicio y objetivo,
imprimiendo el detalle de nodos y la tabla comparativa de resultados.
"""

from heapq import heappush, heappop
from itertools import count
from modelo import Nodo
from datos import problema_ecocampus, viajes, metros, estado_inicial, estado_objetivo

#%%
# Función para calcular distancias mínimas desde un nodo de referencia
def distancias_desde(referencia, viajes, costos):
    dist = {referencia: 0}
    pendientes = [(0, referencia)]
    while pendientes:
        costo, ciudad = heappop(pendientes)
        if costo != dist[ciudad]:
            continue
        for direccion, destino in viajes.get(ciudad, {}).items():
            nuevo = costo + costos[ciudad][direccion]
            if nuevo < dist.get(destino.nombre, float('inf')):
                dist[destino.nombre] = nuevo
                heappush(pendientes, (nuevo, destino.nombre))
    return dist

#%%
# Función para crear la heurística admisible y consistente basada en referencias
def crear_heuristica(referencia, destino_nombre, viajes, costos):
    dist = distancias_desde(referencia, viajes, costos)
    def h(ciudad):
        if ciudad not in dist or destino_nombre not in dist:
            return 0
        return max(0, dist[destino_nombre] - dist[ciudad])
    return h, dist

#%%
# Función principal de búsqueda unificada (UCS si h=0, A* si h es heurística)
def buscar(problema, heuristica, nombre_algoritmo):
    meta = problema.estados_objetivos[0].nombre
    raiz = Nodo(problema.estado_inicial)
    contador = count()
    frontera = [(raiz.coste + heuristica(raiz.estado.nombre), next(contador), raiz)]
    mejor_g = {raiz.estado.nombre: raiz.coste}
    explorados = set()
    orden = []
    
    print(f'\n=== {nombre_algoritmo} ===')
    print(f'{"Nodo":<25} {"g(n)":>7} {"h(n)":>7} {"f(n)":>7}')
    
    while frontera:
        _, _, nodo = heappop(frontera)
        ciudad = nodo.estado.nombre
        if ciudad in explorados or nodo.coste != mejor_g.get(ciudad):
            continue
        g = nodo.coste
        h = heuristica(ciudad)
        print(f'{ciudad:<25} {g:>7} {h:>7} {g+h:>7}')
        orden.append(ciudad)
        explorados.add(ciudad)
        
        if ciudad == meta:
            return nodo, orden
            
        for hijo in nodo.expandir(problema):
            vecino = hijo.estado.nombre
            if vecino not in explorados and hijo.coste < mejor_g.get(vecino, float('inf')):
                mejor_g[vecino] = hijo.coste
                heappush(frontera, (hijo.coste + heuristica(vecino), next(contador), hijo))
    return None, orden

#%%
# Función para formatear y mostrar los resultados de la ruta y métricas
def mostrar_resultado(solucion, orden):
    if solucion is None:
        print('No se encontró ruta.')
        return
    ruta = []
    actual = solucion
    while actual is not None:
        ruta.append(actual.estado.nombre)
        actual = actual.padre
    ruta_reversa = list(reversed(ruta))
    print('Ruta:', ' -> '.join(ruta_reversa))
    print('Costo total:', solucion.coste, 'metros')
    print('Nodos explorados:', len(orden))
    print('Orden:', ' -> '.join(orden))


if __name__ == '__main__':
    meta = estado_objetivo.nombre
    
    # Definir heurísticas
    h1, _ = crear_heuristica('Edificio B Pesado', meta, viajes, metros)
    h2, _ = crear_heuristica('Cancha de Fútbol', meta, viajes, metros)
    h_ucs = lambda _: 0

    print("==========================================================")
    print(" COMPARATIVA DE ALGORITMOS DE BÚSQUEDA - CASO ECOCAMPUS")
    print(f" Inicio: {estado_inicial.nombre} | Meta: {meta}")
    print("==========================================================")

# 1. UCS
    sol_ucs, orden_ucs = buscar(problema_ecocampus, h_ucs, 'UCS (Costo Uniforme)')
    mostrar_resultado(sol_ucs, orden_ucs)

# 2. A* con Heurística 1
    sol_a1, orden_a1 = buscar(problema_ecocampus, h1, 'A* (Heurística 1: Edificio B Pesado)')
    mostrar_resultado(sol_a1, orden_a1)

# 3. A* con Heurística 2
    sol_a2, orden_a2 = buscar(problema_ecocampus, h2, 'A* (Heurística 2: Cancha de Fútbol)')
    mostrar_resultado(sol_a2, orden_a2)

# Tabla Resumen Final
    print("\n" + "=" * 70)
    print("TABLA RESUMEN DE RESULTADOS")
    print("=" * 70)
    print(f"{'Algoritmo / Prueba':<32} | {'Costo (m)':<10} | {'Nodos Explorados':<16}")
    print("-" * 64)
    print(f"{'UCS (h = 0)':<32} | {sol_ucs.coste:<10} | {len(orden_ucs):<16}")
    print(f"{'A* (H1 - Edif. B Pesado)':<32} | {sol_a1.coste:<10} | {len(orden_a1):<16}")
    print(f"{'A* (H2 - Cancha Fútbol)':<32} | {sol_a2.coste:<10} | {len(orden_a2):<16}")
    print("=" * 70)