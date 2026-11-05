"""
Módulo: ventana.py
Proyecto: EcoRuta IA - UTL

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

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from busqueda import buscar_ucs
from datos import metros, ubicaciones, viajes
from modelo import Problema
from interfaz.visualizacion import construir_grafo, dibujar_grafo, reconstruir_ruta


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
        cabecera = tk.Frame(self, bg="#17324D", padx=20, pady=16)
        cabecera.grid(row=0, column=0, columnspan=2, sticky="ew")

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
        panel = tk.Frame(self, bg="white", padx=18, pady=20, width=320)
        panel.grid(row=1, column=0, sticky="nsew", padx=(14, 8), pady=14)
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
        self.combo_inicio.pack(fill="x", pady=(6, 16))
        self.combo_inicio.set("Estacionamiento Norte")
        self.combo_inicio.bind("<<ComboboxSelected>>", self.actualizar_vista)

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
        self.combo_destino.pack(fill="x", pady=(6, 20))
        self.combo_destino.set("Contenedor PET")
        self.combo_destino.bind("<<ComboboxSelected>>", self.actualizar_vista)

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
            text="Limpiar ruta",
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
        self.resultado.pack(fill="both", expand=True)

        self.mostrar_resultado(
            "Selecciona dos ubicaciones y presiona 'Calcular ruta'."
        )

        # Panel de visualización del grafo
        panel_grafo = tk.Frame(self, bg="white", padx=5, pady=5)
        panel_grafo.grid(row=1, column=1, sticky="nsew", padx=(0, 14), pady=14)
        panel_grafo.rowconfigure(0, weight=1)
        panel_grafo.columnconfigure(0, weight=1)

        self.figura = Figure(figsize=(10, 7), dpi=100, facecolor="white")
        self.eje = self.figura.add_subplot(111)
        self.figura.subplots_adjust(left=0.01, right=0.99, top=0.93, bottom=0.12)

        self.canvas = FigureCanvasTkAgg(self.figura, master=panel_grafo)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

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
            # La salida detallada se omite de la terminal
            with redirect_stdout(io.StringIO()):
                solucion, explorados = buscar_ucs(problema)

        except Exception as error:
            messagebox.showerror("Error en búsqueda", str(error))
            return

        if solucion is None:
            self.mostrar_resultado(
                "No se encontró una ruta entre estas ubicaciones."
            )
            self.dibujar()
            return

        # Reconstruir la ruta con los nodos padres
        ruta = reconstruir_ruta(solucion)

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
        self.dibujar(ruta)