#!/bin/env python3
from collections import deque


class Game:
    class Board:
        def __init__(self, **kwargs):
            for k in kwargs:
                self.__dict__[k] = kwargs[k]

    class Player:
        def __init__(self, pid=0, name='unknown', public=None, private=None, game_state=None):
            self.pid = pid
            self.name = name
            self.public = public if public else {}              # public to every player
            self.private = private if private else {}           # private to this player
            self.game_state = game_state if game_state else {}  # only redable by game

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

    def __init__(self, players=None, rounds=None, board=None, rules=None, event_list=None):
        class Deck(deque):
            pass

        class Pile:
            pass

        self.players = players if players else [
            self.Player(x, 'test' + str(x), {'active': True}, {'gems': 0}) for x in range(5)
        ]

        self.rounds = rounds if rounds else [
            self.Round(players, None, order=True) for x in range(5)
        ]

        self.board = board if board else \
            self.Board(
                desk=Deck(['Card(' + str(n) + ')' for n in range(30)]),
                discard=Pile(),
                visible=Pile(),
                counter=5
            )

    class EventQueue(deque):
        def execute(self):
            event = self.popleft()
            next_events = event.execute()
            print(next_events)

    class Event:
        """Acciones que generan una reaccion
        fin de turno
        ataque
        """

        def __init__(self, name, description, target, function, **parameters):
            self.name = name
            self.description = description

            self.target = target
            self.function = function
            self.parameters = parameters

        def execute(self, target=None, **parameters):
            self.function(target if target else self.target, **parameters)
            pass

        pass

    def main_loop(self):
        def decrease(target, **kargs):
            if target is self.board:
                target.counter -= 1
                if target.counter > 0:
                    event_queue.append(self.Event('decrease', '-1', self.board, decrease))
            else:
                raise LookupError
            pass

        def introduction(target, **kargs):
            print('hola')

        def initial_turn(target, **kargs):
            print('mundo')
            event_queue.append(self.Event('decrease', '-1', self.board, decrease))

        event_queue = self.EventQueue([
            self.Event('intro', '', None, introduction),
            self.Event('init', '', None, initial_turn)
        ])

        while event_queue:
            event_queue.execute()


if __name__ == '__main__':
    g = Game()
    g.main_loop()


