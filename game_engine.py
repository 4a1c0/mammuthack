#!/bin/env python3
from collections import deque
import copy
import random

ESPERANT_RESPOSTA = False


class Game:
    def __init__(self, players=None, rounds=None, board=None, rules=None, event_list=None):
        class Pile:
            pass
        
        self.deck = Deck()

        # Cartas que estan en el juego en una ronda
        self.cartas_jugadas = []

        self.players = players if players else [
            self.Player(x, 'test' + str(x),
                        {'active': True},
                        {'gems': 0, 'p_gems': 0}) for x in range(3)
        ]

        """self.rounds = rounds if rounds else [
            self.Round(players, None, order=True) for x in range(5)
        ]"""

        self.board = board if board else \
            self.Board(
                diamants_restants=0,
                retrieved_relics=0
            )

    class Board:
        def __init__(self, **kwargs):
            for k in kwargs:
                self.__dict__[k] = kwargs[k]
            self.ronda = 0
            self.turno = 0
            self.fase = 0

        def reset_round(self):
            pass

        def __repr__(self):
            return f'Board({self.__dict__})'

    class Player:
        def __init__(self, pid=0, name='unknown', public=None, private=None, game_state=None):
            self.pid = pid
            self.name = name
            self.public = public if public else {}              # public to every player
            self.private = private if private else {}           # private to this player
            self.game_state = game_state if game_state else {}  # only redable by game

        def __repr__(self):
            return f'Player({self.public} , ID: {self.pid:03d}, {self.private})\n'

    class EventQueue(deque):
        def execute(self):
            event = self.popleft()
            next_events = event.execute()
            # print(next_events)

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

        def execute(self):  # , target=None, **parameters):
            self.function(self.target, **self.parameters)

    # Events del joc que es criden entre ells
    def main_loop(self):
        # Primera fase que es crida, test
        def introduction(target, **kargs):
            print('hola')

        # Inici del primer torn
        def initial_turn(target, **kargs):
            self.create_deck()
            random.shuffle(self.deck.cards)
            event_queue.append(self.Event('turn', 'descripcio', self.board, seguent_ronda))

        # Torn normal de revelar carta i decidir que fer
        def standard_turn(target, **kargs):
            self.board.turno += 1
            print(f'\n Turno {self.board.turno}')

            carta = self.deck.cards.pop()
            self.cartas_jugadas.append(carta)

            # print(self.deck.cards[-5:])
            print(self.cartas_jugadas, f'Deck: {len(self.deck.cards)} cartas')


            if carta.cardType == "Tresor":
                event_queue.append(self.Event('repartir', 'descripcio', None, repartir,
                                              diamonds=carta.effects['reparteix']))
            else:
                event_queue.append(self.Event('comprovar_estat', 'descripcio', carta, comprovar_estat))

        # Reparteix els diamants entre els jugadors actius com a diamants de la ronda
        def repartir(target, diamonds=0, **kargs):
            active_players = [p for p in self.players if p.public['active']]

            # print(kargs)
            for ap in active_players:
                print('repartido ', diamonds//len(active_players), ' a ', ap.pid)
                ap.private['p_gems'] += diamonds//len(active_players)

            self.board.diamants_restants += diamonds%len(active_players)
            print('remain ', self.board.diamants_restants, ' al tabler')
            event_queue.append(self.Event("esperar_resposta", "descripcio", self.board, esperar_resposta))

        # Comprova que no hi hagi cap trampa repetida a la llista de cartes jugades
        def comprovar_estat(target, **kargs):
            if target.cardType == 'Trampa' and target in self.cartas_jugadas[:-1]:
                self.cartas_jugadas.pop()

                # Començar la seguent ronda (ficar als jugadors a la nova cova i torn normal)
                event_queue.append(self.Event("seguent_ronda", "descripcio", self.board, seguent_ronda))
            else:
                # Si ha sortit una trampa per primer cop o una reliquia, es segueix normal
                event_queue.append(self.Event("esperar_resposta", "descripcio", self.board, esperar_resposta))

        # Espera la resposta dels jugadors de si segueixen o no, el bot.py haura de posar un evento a la cua
        def esperar_resposta(target, **kargs):
            ESPERANT_RESPOSTA = True
            print(self.board)

            active_players = [p for p in self.players if p.public['active']]
            retired_players = []
            active_num = 0
            for ap in active_players:
                ap.public['active'] = (input(f'JUGADOR {ap.pid} continue? ') == '1')
                if ap.public['active']:
                    active_num += 1
                else:
                    retired_players.append(ap)

            for rp in retired_players:
                rp.private['gems'] += rp.private['p_gems'] + self.board.diamants_restants//len(retired_players)
                rp.private['p_gems'] = 0

            if retired_players:
                self.board.diamants_restants = self.board.diamants_restants%len(retired_players)
                if len(retired_players) == 1:
                    for c in self.cartas_jugadas:
                        if c.cardType == 'Reliquia':
                            self.cartas_jugadas.remove(c)
                            retired_players[0].private['gems'] += 10  # TODO - Reliquias bien

            print(self.players)
            if active_num:
                print('Fin del Turno')
                event_queue.append(self.Event('turn', 'descripcio', self.board, standard_turn))
            else:
                print('Fin de la Ronda')
                event_queue.append(self.Event("seguent_ronda", "descripcio", self.board, seguent_ronda))

        # Ficar als jugadors a la nova cova i torn normal
        def seguent_ronda(target, **kargs):
            self.board.turno = 0
            self.board.ronda += 1
            if self.board.ronda > 5:
                print('Fin del Juego')
            print(f'\n\n Ronda {self.board.ronda}\n', self.players)

            for c in self.cartas_jugadas:
                if c.cardType == 'Reliquia':
                    self.cartas_jugadas.remove(c)

            # Torna a guardar les cartes menys la trampa repeteix
            self.deck.reshuffle(self.cartas_jugadas)
            self.cartas_jugadas = []

            self.board.diamants_restants = 0
            for p in self.players:
                p.public['active'] = True
                p.private['p_gems'] = 0

            event_queue.append(self.Event('turn', 'descripcio', self.board, standard_turn))

        # Cua d'events
        event_queue = self.EventQueue([
            self.Event('intro', '', None, introduction),
            self.Event('init', '', None, initial_turn)
        ])

        while event_queue:
            event_queue.execute()

    def create_deck(self):
        tresors = [Card(str(x) + " diamants!", "Reparteix " + str(x) + " diamants.", "Tresor", {"reparteix": x}) for x
                   in range(3, 18)]

        trampes = [
            Card("Trampa d'ariet", "Una trampa d'ariet amb punxes", "Trampa"),
            Card("Trampa d'aranyes", "Una trampa d'aranyes gegants", "Trampa"),
            Card("Trampa de serps", "Una trampa amb serps verinoses", "Trampa"),
            Card("Trampa de roques", "Una trampa de roques", "Trampa"),
            Card("Trampa de lava", "Una trampa de pou de lava", "Trampa")
        ]*3

        reliquies = [Card("Una reliquia!", "Una reliquia que te recompensara con diamantes", "Reliquia")]*6

        self.deck.add(tresors)
        self.deck.add(trampes)
        self.deck.add(reliquies)


class Card:
    """Representation of a Card"""
    def __init__(self, name, description, card_type, effects=None):
        self.name = name
        self.description = description
        self.cardType = card_type
        self.effects = effects if effects else {}

    def __repr__(self):
        return f'Card({self.name}, type: {self.cardType}), {self.effects}\n'


class Deck:
    """Group of cards"""
    def add(self, card):
        if type(card) is list:
            self.cards = self.cards + card
        else:
            self.cards.append(card)

    def reshuffle(self, readd):
        self.cards += readd
        random.shuffle(self.cards)

    def __init__(self, cards=[]):
        self.cards = []


if __name__ == '__main__':
    g = Game()
    g.main_loop()
