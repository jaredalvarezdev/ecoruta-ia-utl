"""
Módulo: visualizacion.py
Proyecto: EcoRuta IA - UTL

Construye el grafo del campus a partir de datos.py y lo dibuja con
matplotlib, resaltando el estado inicial, el objetivo y la ruta encontrada.
"""

import networkx as nx
from matplotlib.lines import Line2D

from datos import metros, ubicaciones, viajes


# Distribución visual aproximada del croquis elaborado por el equipo.
# No representa coordenadas reales.
POSICIONES = {
    "Estacionamiento Norte": (0.9, 4.45),
    "Edificio B Pesado": (2.9, 4.75),
    "Edificio B": (4.3, 4.45),
    "Edificio C": (5.8, 4.05),
    "Edificio D": (8.4, 3.10),
    "Cancha de Fútbol": (2.25, 2.85),
    "Edificio A": (4.4, 2.47),
    "Edificio A Pesado": (5.35, 1.38),
    "Cafetería": (7.75, 1.65),
    "Contenedor PET": (8.10, 0.66),
}

ETIQUETAS = {
    "Estacionamiento Norte": "Estacionamiento\nNorte",
    "Edificio B Pesado": "Edificio B\nPesado",
    "Edificio B": "Edificio B",
    "Edificio C": "Edificio C",
    "Edificio D": "Edificio D",
    "Cancha de Fútbol": "Cancha de\nFútbol",
    "Edificio A": "Edificio A",
    "Edificio A Pesado": "Edificio A\nPesado",
    "Cafetería": "Cafetería",
    "Contenedor PET": "Contenedor\nPET",
}


def construir_grafo():
    """Construye el grafo usando las conexiones del proyecto."""
    grafo = nx.Graph()

    for estado in ubicaciones.values():
        grafo.add_node(estado.nombre)

    for origen, direcciones in viajes.items():
        for accion, destino in direcciones.items():
            nombre_destino = destino.nombre
            distancia = metros[origen][accion]

            if grafo.has_edge(origen, nombre_destino):
                anterior = grafo[origen][nombre_destino]["weight"]

                if anterior != distancia:
                    raise ValueError(
                        f"Costos distintos entre {origen} y {nombre_destino}."
                    )
            else:
                grafo.add_edge(origen, nombre_destino, weight=distancia)

    return grafo


def reconstruir_ruta(nodo_solucion):
    """Recupera la ruta siguiendo los padres de los nodos."""
    ruta = []
    actual = nodo_solucion

    while actual is not None:
        ruta.append(actual.estado.nombre)
        actual = actual.padre

    ruta.reverse()
    return ruta


def dibujar_grafo(eje, grafo, origen, destino, ruta=None):
    """Dibuja los estados, las distancias y la ruta encontrada."""
    eje.clear()
    eje.set_facecolor("white")
    ruta = ruta or []

    # Dibujar todas las conexiones
    nx.draw_networkx_edges(
        grafo,
        POSICIONES,
        ax=eje,
        width=2.2,
        edge_color="#64748B"
    )

    # Resaltar la ruta encontrada
    if len(ruta) > 1:
        tramos = list(zip(ruta[:-1], ruta[1:]))

        nx.draw_networkx_edges(
            grafo,
            POSICIONES,
            ax=eje,
            edgelist=tramos,
            width=5,
            edge_color="#16A34A"
        )

    # Mostrar las distancias de las conexiones
    etiquetas_distancia = {
        arista: f"{distancia} m"
        for arista, distancia in nx.get_edge_attributes(
            grafo, "weight"
        ).items()
    }

    nx.draw_networkx_edge_labels(
        grafo,
        POSICIONES,
        ax=eje,
        edge_labels=etiquetas_distancia,
        font_size=8,
        rotate=False,
        bbox={
            "boxstyle": "round,pad=0.18",
            "facecolor": "white",
            "edgecolor": "#CBD5E1"
        }
    )

    # Dibujar los recuadros de las ubicaciones
    for nombre in grafo.nodes:

        if nombre == origen and nombre == destino:
            fondo = "#FCD34D"
        elif nombre == origen:
            fondo = "#86EFAC"
        elif nombre == destino:
            fondo = "#FDA4AF"
        elif nombre in ruta:
            fondo = "#BFDBFE"
        else:
            fondo = "#E2E8F0"

        x, y = POSICIONES[nombre]

        eje.text(
            x,
            y,
            ETIQUETAS[nombre],
            ha="center",
            va="center",
            fontsize=8.7,
            fontweight="bold",
            color="#17324D",
            zorder=10,
            bbox={
                "boxstyle": "round,pad=0.5",
                "facecolor": fondo,
                "edgecolor": "#334155",
                "linewidth": 1.3
            }
        )

    eje.set_title(
        "Grafo EcoRuta - Campus UTL",
        fontsize=15,
        fontweight="bold",
        color="#17324D",
        pad=12
    )

    # Leyenda del grafo
    eje.legend(
        handles=[
            Line2D(
                [0], [0],
                marker="s",
                linestyle="None",
                markersize=11,
                markerfacecolor="#86EFAC",
                markeredgecolor="#334155",
                label="Estado inicial"
            ),
            Line2D(
                [0], [0],
                marker="s",
                linestyle="None",
                markersize=11,
                markerfacecolor="#FDA4AF",
                markeredgecolor="#334155",
                label="Objetivo"
            ),
            Line2D(
                [0], [0],
                color="#16A34A",
                linewidth=4,
                label="Ruta calculada"
            )
        ],
        loc="lower center",
        bbox_to_anchor=(0.5, -0.09),
        ncol=3,
        fontsize=9,
        frameon=False
    )

    eje.set_xlim(-0.1, 9.6)
    eje.set_ylim(-0.2, 5.55)
    eje.axis("off")