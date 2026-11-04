
"""
Proyecto: Algoritmos de búsqueda en Inteligencia Artificial
Módulo: Estructuras de datos para búsqueda en grafos.

Descripción:
Implementación de acciones, estados, problemas y nodos.

Se construye el problema de búsqueda y se realizan
expansiones de nodos con cálculo de costos acumulados.
"""


# Clase Accion
class Accion:
    def __init__(self, nombre):
        self.nombre = nombre

    def __str__(self):
        return self.nombre


# Clase Estado
class Estado:
    def __init__(self, nombre, acciones):
        self.nombre = nombre
        self.acciones = acciones

    def __str__(self):
        return self.nombre


# Clase Problema
class Problema:
    def __init__(self, estado_inicial, estados_objetivos,
                 acciones, costes=None):

        self.estado_inicial = estado_inicial
        self.estados_objetivos = estados_objetivos
        self.acciones = acciones
        self.costes = costes
        self.infinito = float('inf') # Si no encuentra estado, accion

        # Si no se proporcionan costos,
        # se asigna costo 1 a cada acción.
        if self.costes is None:
            self.costes = {}

            for estado in self.acciones:
                self.costes[estado] = {}

                for accion in self.acciones[estado]:
                    self.costes[estado][accion] = 1

    def __str__(self):
        objetivos = [
            estado.nombre
            for estado in self.estados_objetivos
        ]

        mensaje = "Estado Inicial: {0} -> Objetivos: {1}"

        return mensaje.format(
            self.estado_inicial.nombre,
            objetivos
        )

    def es_objetivo(self, estado):
        return estado in self.estados_objetivos

    def resultado(self, estado, accion):
        if estado.nombre not in self.acciones:
            return None

        acciones_estado = self.acciones[estado.nombre]

        if accion.nombre not in acciones_estado:
            return None

        return acciones_estado[accion.nombre]

    def coste_accion(self, estado, accion):
        if estado.nombre not in self.costes:
            return self.infinito

        costes_estado = self.costes[estado.nombre]

        if accion.nombre not in costes_estado:
            return self.infinito

        return costes_estado[accion.nombre]


# Clase Nodo
class Nodo:
    def __init__(self, estado, accion=None,
                 acciones=None, padre=None):

        self.estado = estado
        self.accion = accion
        self.acciones = acciones
        self.padre = padre
        self.hijos = [] 
        self.coste = 0

    def __str__(self):
        return self.estado.nombre

    def expandir(self, problema):
        self.hijos = []

        # Consultar las acciones disponibles.
        if self.acciones is None:
            self.acciones = problema.acciones.get(
                self.estado.nombre, {}
            )

        # Crear un nodo hijo por cada acción.
        for nombre_accion in self.acciones:

            accion_hijo = Accion(nombre_accion)

            nuevo_estado = problema.resultado(
                self.estado, accion_hijo
            )

            if nuevo_estado is None:
                continue

            acciones_nuevo = problema.acciones.get(
                nuevo_estado.nombre, {}
            )

            hijo = Nodo(
                nuevo_estado,
                accion_hijo,
                acciones_nuevo,
                self
            )

            # Calcular el costo acumulado.
            hijo.coste = (
                self.coste + problema.coste_accion(self.estado,accion_hijo)
            )

            self.hijos.append(hijo)

        return self.hijos # Frontera

    def hijo_mejor(self, problema=None):
        if not self.hijos:
            return None

        mejor = min(
            self.hijos,
            key=lambda hijo: hijo.coste
        )

        return mejor