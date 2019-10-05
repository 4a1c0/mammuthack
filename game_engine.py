#!/bin/env python3


class Round:
    """5 rondas"""
    """Ronda, contiene el turno/stage de todos los jugadores"""
    def __init__(self, players, order=False):
        self.order = False
        self.players = players if players else []
        pass
    pass


class Stage:
    """cueva hasta que no queden jugadores"""
    """Fase asincrona, contiene acciones para grupo de jugadores sin orden concreto.
    todo el mundo coge cartas
    ...
    """
    def __init__(self):
        pass
    pass


class Turn:
    """"""
    """Turno, contiene las fases de los jugadores involucrados"""
    def __init__(self):
        pass
    pass


class Phase:
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
    pass


class Action:
    def __init__(self):
        pass
    pass


class Event:
    """Acciones que generan una reaccion
    fin de turno
    ataque
    """
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


class Deck(Pile):
    """Group of cards"""
    def __init__(self):
        pass
    pass


class Player:
    def __init__(self, public, private, game_state, pid=0, name='unknown'):
        self.pid = pid
        self.name = name
        self.public = public if public else {}              # public to every player
        self.private = private if private else {}           # private to this player
        self.game_state = game_state if game_state else {}  # only redable by game
    pass


class PlayerGroup:
    def __init__(self, shared_info, shared_state):
        self.shared_state = shared_state if shared_state else []
        self.shared_info = shared_info if shared_info else []
    pass


class Info:
    def __init__(self):
        pass
    pass


class Collectible:
    def __init__(self):
        pass
    pass




