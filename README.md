# EcoRuta IA - UTL

Búsqueda de rutas de menor costo con UCS y A* para recolección de residuos sólidos en el campus de la UTL.

Proyecto del examen práctico de la Unidad II de Fundamentos de Inteligencia Artificial, Universidad Tecnológica de León.

## Caso: EcoCampus

Un sensor reporta que el contenedor de PET junto a la Cafetería está casi lleno. El carrito de recolección sale del Estacionamiento Norte y debe llegar por la ruta de menor distancia, en metros.

El grafo tiene 10 estados y 13 conexiones, todas de doble sentido.

## Estructura

```
src/
├── modelo.py          Clases Accion, Estado, Nodo y Problema
├── datos.py           Estados, conexiones, costos, inicio y objetivo
├── heuristicas.py     Heurísticas basadas en un estado de referencia
├── busqueda.py        UCS y A*
├── verificacion.py    Comprueba que la heurística no sobreestima
├── comparar.py        Compara UCS y A* con dos heurísticas
└── main.py            Menú del programa
```

## Cómo ejecutarlo

Desde la raíz del repositorio:

```
python src/main.py
```

Requiere Python 3.