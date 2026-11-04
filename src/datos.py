"""
Módulo: datos.py
Proyecto: EcoRuta IA - UTL

Define los estados, las conexiones y los costos (en metros) del campus,
y crea el problema de búsqueda del caso EcoCampus.
"""

from modelo import Accion, Estado, Problema

# Definición de acciones
accN = Accion('norte')
accS = Accion('sur')
accE = Accion('este')
accO = Accion('oeste')
accNE = Accion('noreste')
accNO = Accion('noroeste')
accSE = Accion('sureste')
accSO = Accion('suroeste')

# Definición de los estados
estacionamiento_norte = Estado('Estacionamiento Norte', [accNE, accSE]) # inicia
edificio_b_pesado = Estado('Edificio B Pesado', [accSO, accE])
edificio_b = Estado('Edificio B', [accO, accE, accS])
edificio_c = Estado('Edificio C', [accO, accE, accSE])
edificio_d = Estado('Edificio D', [accO, accSO])
canchas_futbol = Estado('Cancha de Fútbol', [accNO, accE])
edificio_a = Estado('Edificio A', [accO, accN, accNE, accSE])
edificio_a_pesado = Estado('Edificio A Pesado', [accNO, accN])
cafeteria = Estado('Cafetería', [accNO, accNE, accSO, accS, accSE])
contenedor_PET = Estado('Contenedor PET', [accNO]) # objetivo

# Diccionario de conexiones
viajes = {
    'Estacionamiento Norte': {'noreste': edificio_b_pesado, 'sureste': canchas_futbol},
    'Edificio B Pesado': {'suroeste': estacionamiento_norte, 'este': edificio_b},
    'Edificio B': {'oeste': edificio_b_pesado, 'este': edificio_c, 'sur': edificio_a},
    'Edificio C': {'oeste': edificio_b, 'este': edificio_d, 'sureste': cafeteria},
    'Edificio D': {'oeste': edificio_c, 'suroeste': cafeteria},
    'Cancha de Fútbol': {'noroeste': estacionamiento_norte, 'este': edificio_a},
    'Edificio A': {'oeste': canchas_futbol, 'norte': edificio_b, 'noreste': cafeteria, 'sureste': edificio_a_pesado},
    'Edificio A Pesado': {'noroeste': edificio_a, 'norte': cafeteria},
    'Cafetería': {'noroeste': edificio_c, 'noreste': edificio_d, 'suroeste': edificio_a, 'sur': edificio_a_pesado, 'sureste': contenedor_PET},
    'Contenedor PET': {'noroeste': cafeteria}
}

# Distancia en metros entre estados
metros = {
    'Estacionamiento Norte': {'noreste': 66, 'sureste': 100},
    'Edificio B Pesado': {'suroeste': 66, 'este': 93},
    'Edificio B': {'oeste': 93, 'este': 81, 'sur': 74},
    'Edificio C': {'oeste': 81, 'este': 110, 'sureste': 133},
    'Edificio D': {'oeste': 110, 'suroeste': 71},
    'Cancha de Fútbol': {'noroeste': 100, 'este': 82},
    'Edificio A': {'oeste': 82, 'norte': 74, 'noreste': 190, 'sureste': 53},
    'Edificio A Pesado': {'noroeste': 53, 'norte': 200},
    'Cafetería': {'noroeste': 133, 'noreste': 71, 'suroeste': 190, 'sur': 200, 'sureste': 15},
    'Contenedor PET': {'noroeste': 15}
}

# Diccionario con números (para el menú)
ubicaciones = {
    1: estacionamiento_norte,
    2: edificio_b_pesado,
    3: edificio_b,
    4: edificio_c,
    5: edificio_a,
    6: edificio_a_pesado,
    7: canchas_futbol,
    8: edificio_d,
    9: cafeteria,
    10: contenedor_PET
}

# Configuracion del problema 
estado_inicial = estacionamiento_norte
estado_objetivo = contenedor_PET

# Instancia del problema
problema_ecocampus = Problema(
    estado_inicial,
    [estado_objetivo],
    viajes,
    metros
)