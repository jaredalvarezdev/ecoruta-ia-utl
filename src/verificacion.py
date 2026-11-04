"""
Módulo: verificacion.py
Proyecto: EcoRuta IA - UTL

Verifica que las heurísticas cumplan con la condición de admisibilidad
comparándolas con el costo real restante de cada estado al objetivo.
"""

from heapq import heappush, heappop
from datos import viajes, metros, estado_objetivo

#%%
#Calcula el costo real mínimo (g*) desde cualquier nodo hasta la meta usando el grafo inverso.
def calcular_costos_reales(meta_nombre, viajes, costos):

    inverso = {meta_nombre: {}}
    for nodo, vecinos in viajes.items():
        for acc, destino in vecinos.items():
            dest_nombre = destino.nombre
            if dest_nombre not in inverso:
                inverso[dest_nombre] = {}
            c = costos[nodo][acc]
            inverso[dest_nombre][nodo] = c
            
    dist = {meta_nombre: 0}
    pendientes = [(0, meta_nombre)]
    while pendientes:
        costo, actual = heappop(pendientes)
        if costo != dist[actual]:
            continue
        for vecino, c in inverso.get(actual, {}).items():
            nuevo = costo + c
            if nuevo < dist.get(vecino, float('inf')):
                dist[vecino] = nuevo
                heappush(pendientes, (nuevo, vecino))
    return dist

#%%
#Calcula las distancias mínimas desde una referencia respetando el sentido de las conexiones.
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
#Crea la función heurística h(n) = max(0, d(R, meta) - d(R, n))

def crear_heuristica(referencia, destino_nombre, viajes, costos):
    dist = distancias_desde(referencia, viajes, costos)
    def h(ciudad):
        if ciudad not in dist or destino_nombre not in dist:
            return 0
        return max(0, dist[destino_nombre] - dist[ciudad])
    return h, dist

if __name__ == '__main__':
    meta = estado_objetivo.nombre
    costos_reales = calcular_costos_reales(meta, viajes, metros)
    
    # Heurística 1: Referencia 'Edificio B Pesado'
    h1, _ = crear_heuristica('Edificio B Pesado', meta, viajes, metros)
    # Heurística 2: Referencia 'Cancha de Fútbol'
    h2, _ = crear_heuristica('Cancha de Fútbol', meta, viajes, metros)
    
    print("=" * 85)
    print(f"VERIFICACIÓN DE ADMISIBILIDAD DE HEURÍSTICAS (Meta: {meta})")
    print("=" * 85)
    print(f"{'Estado':<25} | {'Costo Real (g*)':<15} | {'H1 (Edif. B Pesado)':<20} | {'H2 (Cancha Fútbol)':<20}")
    print("-" * 85)
    
    adm1_valida = True
    adm2_valida = True
    
    for estado in viajes.keys():
        g_star = costos_reales.get(estado, float('inf'))
        val_h1 = h1(estado)
        val_h2 = h2(estado)
        
        if val_h1 > g_star:
            adm1_valida = False
        if val_h2 > g_star:
            adm2_valida = False
            
        print(f"{estado:<25} | {str(g_star):<15} | {str(val_h1):<20} | {str(val_h2):<20}")
        
    print("=" * 85)
    print(f"¿Heurística 1 es admisible (h(n) <= g*(n))?: {adm1_valida}")
    print(f"¿Heurística 2 es admisible (h(n) <= g*(n))?: {adm2_valida}")