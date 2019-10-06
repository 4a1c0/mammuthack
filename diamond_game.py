class Round:
    """5 rondas"""
    """Ronda, contiene el turno/stage de todos los jugadores"""

    def __init__(self, players, event, order=False):
        self.players = players if players else []
        self.event = event
        self.order = False

    def __enter__(self):
        return self.event

    def __exit__(self):
        for p in self.players:
            p.public['active'] = True


class Turn:
    """cueva hasta que no queden jugadores x5"""
    """Turno, contiene las fases de los jugadores involucrados"""
    def __init__(self, sync=False):
        pass

    pass


class Phase:
    """revelar, carta, repartir/fin x?"""
    """Sub-turno/Fase, contiene las opciones que tiene que ejecutar el jugador
    coger carta
    jugar mano
    fin del turno
    """
    def __init__(self, name='unknown', description='description', events=None, actions=None):
        self.name = name
        self.description = description
        self.events = events if events else []
        self.actions = actions if actions else []


phases = [  # TODO - Crear eventos y acciones
    Phase('Revelar carta', 'Se revela una carta y se añade al mapa.', Deck().top(), ''),
    # Añadir evento de la carta a lista de eventos (desde la carta)
    Phase('Ronda de decision', 'Los jugadores deciden si continuan o se retiran', '', Action().decide()),
    Phase('Ronda de decision (cont.)', 'Se guarda el progreso de los jugadores retirados', Event, ),
    # Añadir evento de la carta a lista de eventos (desde la carta)
    Phase('Siguiente turno', 'Añade turno extra a la cola de Eventos', Event, '')
]


class Action:
    """Evento con interaccion del user"""
    def __init__(self):
        pass
    pass


class GameObject:
    pass


class Pile:
    """Group of objects
    discard pile
    graveyad
    """
    pass


class Card(GameObject):
    """Representation of a Card"""
    def __init__(self):
        pass
    pass


class Deck(list):
    """Group of cards"""
    #def __init__(self):
    #    pass
    pass





class PlayerGroup:
    def __init__(self, players, shared_info=None, shared_state=None):
        self.players = players
        self.shared_info = shared_info if shared_info else []
        self.shared_state = shared_state if shared_state else []


class Info:
    def __init__(self):
        pass
    pass


class Collectible:
    def __init__(self):
        pass
    pass