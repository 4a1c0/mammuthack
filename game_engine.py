#!/bin/env python3


class Round:
    """Ronda, contiene el turno de todos los jugadores"""
    def __init__(self, order=False):
        self.order = False

        pass
    pass


class Turn:
    """Turno, contiene las fases de los jugadores involucrados"""
    def __init__(self):
        pass
    pass


class Phase:
    """Sub-turno/Fase, contiene la accion que tiene que ejecutar el jugador"""
    def __init__(self):
        pass
    pass


class Stage:
    """Fase global, contiene acciones para grupo de jugadores
    todo el mundo coge cartas
    """
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
    def __init__(self):
        pass
    pass


class Info:
    def __init__(self):
        pass
    pass


class Collectible:
    def __init__(self):
        pass
    pass

