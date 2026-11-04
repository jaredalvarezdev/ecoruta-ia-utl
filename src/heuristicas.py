"""Heurísticas para EcoRuta IA (EcoCampus).

Calcula las distancias mínimas (Dijkstra) desde un estado de referencia R
y construye h(n) = max(0, d(R, meta) - d(R, n)), que A* usa para estimar
el costo restante al objetivo. Es admisible y consistente. Distancias en metros.
"""

from heapq import heappush, heappop


def distancias_desde(referencia, viajes, metros):
    """Distancias mínimas (en metros) desde la referencia a cada estado."""
    dist = {referencia: 0}
    pendientes = [(0, referencia)]
    while pendientes:
        costo, estado = heappop(pendientes)
        if costo != dist[estado]:
            continue
        for accion, destino in viajes.get(estado, {}).items():
            nuevo = costo + metros[estado][accion]
            if nuevo < dist.get(destino.nombre, float('inf')):
                dist[destino.nombre] = nuevo
                heappush(pendientes, (nuevo, destino.nombre))
    return dist


def crear_heuristica(referencia, destino, viajes, metros):
    """Devuelve h(n) y el diccionario de distancias desde la referencia."""
    dist = distancias_desde(referencia, viajes, metros)
    if destino not in dist:
        raise ValueError('La referencia no puede alcanzar el objetivo.')

    def h(estado):
        if estado not in dist:
            return 0  # cota inferior segura para estados no alcanzables desde R
        return max(0, dist[destino] - dist[estado])

    return h, dist