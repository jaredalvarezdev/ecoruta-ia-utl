
"""
Reto 5: mejoras 1, 2 y 5.
1) Elegir el estado inicial y objetivo.
2) Dibujar el grafo y resaltar la ruta encontrada.
5) Interfaz sencilla.

La ruta la calcula buscar_ucs() del módulo busqueda.py del equipo.
Las conexiones y distancias se leen de datos.py, sin duplicarlas.
"""

import io
import tkinter as tk
from contextlib import redirect_stdout
from tkinter import messagebox, ttk

import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.lines import Line2D

from busqueda import buscar_ucs
from datos import metros, ubicaciones, viajes
from modelo import Problema


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
                grafo.add_edge(
                    origen,
                    nombre_destino,
                    weight=distancia
                )

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


# -------------------- INTERFAZ GRÁFICA --------------------

class InterfazEcoRuta(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("EcoRuta IA - Universidad Tecnológica de León")
        self.geometry("1250x760")
        self.minsize(1050, 650)
        self.configure(bg="#EEF3F8")

        self.grafo = construir_grafo()

        self.estados = {
            estado.nombre: estado
            for estado in ubicaciones.values()
        }

        nombres = list(self.estados.keys())

        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        # Cabecera
        cabecera = tk.Frame(
            self,
            bg="#17324D",
            padx=20,
            pady=16
        )

        cabecera.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew"
        )

        tk.Label(
            cabecera,
            text="EcoRuta IA  |  UTL",
            font=("Segoe UI", 19, "bold"),
            fg="white",
            bg="#17324D"
        ).pack(anchor="w")

        tk.Label(
            cabecera,
            text="Búsqueda de la ruta de recolección con menor distancia",
            font=("Segoe UI", 10),
            fg="#D4E4F2",
            bg="#17324D"
        ).pack(anchor="w")

        # Panel del menú
        panel = tk.Frame(
            self,
            bg="white",
            padx=18,
            pady=20,
            width=320
        )

        panel.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=(14, 8),
            pady=14
        )

        panel.grid_propagate(False)

        tk.Label(
            panel,
            text="Planificar ruta",
            bg="white",
            fg="#17324D",
            font=("Segoe UI", 15, "bold")
        ).pack(anchor="w", pady=(0, 16))

        # Selección del estado inicial
        tk.Label(
            panel,
            text="Estado inicial",
            bg="white",
            fg="#334155",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w")

        self.combo_inicio = ttk.Combobox(
            panel,
            state="readonly",
            values=nombres,
            font=("Segoe UI", 10),
            width=29
        )

        self.combo_inicio.pack(
            fill="x",
            pady=(6, 16)
        )

        self.combo_inicio.set("Estacionamiento Norte")

        self.combo_inicio.bind(
            "<<ComboboxSelected>>",
            self.actualizar_vista
        )

        # Selección del estado objetivo
        tk.Label(
            panel,
            text="Estado objetivo",
            bg="white",
            fg="#334155",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w")

        self.combo_destino = ttk.Combobox(
            panel,
            state="readonly",
            values=nombres,
            font=("Segoe UI", 10),
            width=29
        )

        self.combo_destino.pack(
            fill="x",
            pady=(6, 20)
        )

        self.combo_destino.set("Contenedor PET")

        self.combo_destino.bind(
            "<<ComboboxSelected>>",
            self.actualizar_vista
        )

        # Botón para ejecutar UCS
        tk.Button(
            panel,
            text="Calcular ruta",
            command=self.calcular_ruta,
            bg="#15803D",
            fg="white",
            activebackground="#166534",
            activeforeground="white",
            cursor="hand2",
            relief="flat",
            font=("Segoe UI", 11, "bold"),
            pady=11
        ).pack(fill="x")

        # Botón para mostrar el grafo completo
        tk.Button(
            panel,
            text="Ver grafo completo",
            command=self.actualizar_vista,
            bg="#E2E8F0",
            fg="#1E293B",
            cursor="hand2",
            relief="flat",
            font=("Segoe UI", 10),
            pady=9
        ).pack(fill="x", pady=(9, 18))

        tk.Label(
            panel,
            text="Resultado de la búsqueda",
            bg="white",
            fg="#17324D",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w", pady=(0, 7))


        tk.Label(
            panel,
            text="Algoritmo: UCS (costo uniforme)",
            bg="white",
            fg="#64748B",
            font=("Segoe UI", 9)
        ).pack(anchor="w", pady=(12, 0))

        # Área donde se muestra el resultado
        self.resultado = tk.Text(
            panel,
            height=14,
            wrap="word",
            bg="#F1F5F9",
            fg="#1E293B",
            font=("Segoe UI", 10),
            relief="flat",
            padx=11,
            pady=11
        )

        self.resultado.pack(
            fill="both",
            expand=True
        )

        self.mostrar_resultado(
            "Selecciona dos ubicaciones y presiona 'Calcular ruta'."
        )

        

        # Panel de visualización del grafo
        panel_grafo = tk.Frame(
            self,
            bg="white",
            padx=5,
            pady=5
        )

        panel_grafo.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=(0, 14),
            pady=14
        )

        panel_grafo.rowconfigure(0, weight=1)
        panel_grafo.columnconfigure(0, weight=1)

        self.figura = Figure(
            figsize=(10, 7),
            dpi=100,
            facecolor="white"
        )

        self.eje = self.figura.add_subplot(111)

        self.figura.subplots_adjust(
            left=0.01,
            right=0.99,
            top=0.93,
            bottom=0.12
        )

        self.canvas = FigureCanvasTkAgg(
            self.figura,
            master=panel_grafo
        )

        self.canvas.get_tk_widget().grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.dibujar()

    # Mostrar texto en el panel de resultados
    def mostrar_resultado(self, texto):

        self.resultado.configure(state="normal")
        self.resultado.delete("1.0", tk.END)
        self.resultado.insert(tk.END, texto)
        self.resultado.configure(state="disabled")

    # Actualizar el dibujo
    def dibujar(self, ruta=None):

        dibujar_grafo(
            self.eje,
            self.grafo,
            self.combo_inicio.get(),
            self.combo_destino.get(),
            ruta
        )

        self.canvas.draw_idle()

    # Limpiar la ruta resaltada
    def actualizar_vista(self, evento=None):

        self.mostrar_resultado(
            "Selecciona dos ubicaciones y presiona 'Calcular ruta'."
        )

        self.dibujar()

    # Ejecutar el agente UCS
    def calcular_ruta(self):

        origen = self.combo_inicio.get()
        destino = self.combo_destino.get()

        if origen not in self.estados or destino not in self.estados:
            messagebox.showwarning(
                "Faltan datos",
                "Selecciona un inicio y un objetivo válidos."
            )
            return

        # Crear el problema con las clases del proyecto
        problema = Problema(
            self.estados[origen],
            [self.estados[destino]],
            viajes,
            metros
        )

        try:
            # Utilizar el algoritmo UCS del equipo
            # La salida detallada se omite de la terminal
            with redirect_stdout(io.StringIO()):
                solucion, explorados = buscar_ucs(problema)

        except Exception as error:
            messagebox.showerror(
                "Error en búsqueda",
                str(error)
            )
            return

        if solucion is None:
            self.mostrar_resultado(
                "No se encontró una ruta entre estas ubicaciones."
            )
            self.dibujar()
            return

        # Reconstruir la ruta con los nodos padres
        ruta = reconstruir_ruta(solucion)

        # Mostrar el resultado en la interfaz
        texto = (
            f"Estado inicial: {origen}\n"
            f"Estado objetivo: {destino}\n\n"
            "RUTA ENCONTRADA\n"
            + "\n".join(
                f"{numero}. {ciudad}"
                for numero, ciudad in enumerate(ruta, 1)
            )
            + f"\n\nDistancia total: {solucion.coste} metros"
            + f"\nMovimientos: {len(ruta) - 1}"
            + f"\nNodos explorados: {len(explorados)}"
        )

        self.mostrar_resultado(texto)

        # Mostrar la ruta encontrada sobre el grafo
        self.dibujar(ruta)


# -------------------- PROGRAMA PRINCIPAL --------------------

if __name__ == "__main__":

    ventana = InterfazEcoRuta()
    ventana.mainloop()
