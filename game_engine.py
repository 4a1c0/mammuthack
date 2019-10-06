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

        #Cartas que estan en el juego en una ronda
        self.cartas_jugadas = []

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



    class EventQueue(deque):
        def execute(self):
            event = self.popleft()
            next_events = event.execute()
            #print(next_events)

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


    # Events del joc que es criden entre ells
    def main_loop(self):
                
        # Primera fase que es crida, test
        def introduction(target, **kargs):
            print('hola')


        # Inici del primer torn
        def initial_turn(target, **kargs):
            self.createDeck()
            random.shuffle(self.deck.cards)
            event_queue.append(self.Event('turn', 'descripcio', self.board, standard_turn))

        # Torn normal de revelar carta i decidir que fer
        def standard_turn(target, **kargs):

            carta = self.deck.cards.pop()
            self.cartas_jugadas.append(carta)

            print(self.cartas_jugadas[0].name)

            if(carta.cardType == "Tresor"):
                event_queue.append(self.Event('repartir', 'descripcio', self.board, repartir))
            else:
                event_queue.append(self.Event('comprovar_estat', 'descripcio', self.board, comprovar_estat))

        # Reparteix els diamants entre els jugadors actius com a diamants de la ronda
        def repartir(target, **kargs):

            # No entenc com s'han codificat les coses de jugadors
            # No veig on esta codificat lo de deixar els diamants sobrants a la ruta

            event_queue.append(self.Event("esperar_resposta", "descripcio", self.board, esperar_resposta))

        # Comprova que no hi hagi cap trampa repetida a la llista de cartes jugades
        def comprovar_estat(target, **kargs):
            
            trampa_repetida = False
            for i in self.cartas_jugadas[:-1]:
                if(i.name == self.cartas_jugadas[-1].name):
                    trampa_repetida = True
                    # Treure els jugadors de la cova i fer perdre diamants

                    # Torna a guardar les cartes menys la trampa repe
                    self.deck.add(self.cartas_jugadas[:-1])
                    # Començar la seguent ronda (ficar als jugadors a la nova cova i torn normal)
                    event_queue.append(self.Event("seguent_ronda", "descripcio", self.board, seguent_ronda))
                    break
            
            # Si ha sortit una trampa per primer cop o una reliquia, es segueix normal
            if(trampa_repetida == False):
                event_queue.append(self.Event("esperar_resposta", "descripcio", self.board, esperar_resposta))
            

        # Espera la resposta dels jugadors de si segueixen o no, el bot.py haura de posar un evento a la cua
        def esperar_resposta(target, **kargs):
            ESPERANT_RESPOSTA = True
            print("ESPERANT JUGADORS")

        # Ficar als jugadors a la nova cova i torn normal
        def seguent_ronda(target, **kargs):
            pass
        
        # FALTA DEFINIR QUE PASSA QUAN CONTESTEN ELS JUGADORS: 
        #       REPARTIR RELIQUIES I TREURE DEL DECK
        #       REPARTIR DIAMANTS ENTRE ELS QUE ES RETIREN
        #       ACABAR RONDA SI ES RETIREN TOTS




        # Cua d'events
        event_queue = self.EventQueue([
            self.Event('intro', '', None, introduction),
            self.Event('init', '', None, initial_turn)
        ])

        while event_queue:
            event_queue.execute()

    def createDeck(self):

        tresors = [Card(str(x) + " diamants!", "Reparteix " + str(x) + " diamants.", "Tresor", {"reparteix": x}) for x
                   in range(3, 18)]

        trampes = []

        trampaAriet = Card("Trampa d'ariet", "Una trampa d'ariet amb punxes", "Trampa")
        trampes.append(trampaAriet)
        trampes.append(copy.deepcopy(trampaAriet))
        trampes.append(copy.deepcopy(trampaAriet))

        trampaAranyes = Card("Trampa d'aranyes", "Una trampa d'aranyes gegants", "Trampa")
        trampes.append(trampaAranyes)
        trampes.append(copy.deepcopy(trampaAranyes))
        trampes.append(copy.deepcopy(trampaAranyes))

        trampaSerps = Card("Trampa de serps", "Una trampa amb serps verinoses", "Trampa")
        trampes.append(trampaSerps)
        trampes.append(copy.deepcopy(trampaSerps))
        trampes.append(copy.deepcopy(trampaSerps))

        trampaRoques = Card("Trampa de roques", "Una trampa de roques", "Trampa")
        trampes.append(trampaRoques)
        trampes.append(copy.deepcopy(trampaRoques))
        trampes.append(copy.deepcopy(trampaRoques))

        trampaLava = Card("Trampa de lava", "Una trampa de pou de lava", "Trampa")
        trampes.append(trampaLava)
        trampes.append(copy.deepcopy(trampaLava))
        trampes.append(copy.deepcopy(trampaLava))

        reliquies = []

        reliquia = Card("Una reliquia!", "Una reliquia que te recompensara con diamantes", "Reliquia")
        reliquies.append(reliquia)
        reliquies.append(copy.deepcopy(reliquia))
        reliquies.append(copy.deepcopy(reliquia))
        reliquies.append(copy.deepcopy(reliquia))
        reliquies.append(copy.deepcopy(reliquia))
        reliquies.append(copy.deepcopy(reliquia))

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
    pass


class Deck:
    """Group of cards"""
    def add(self, card):
        if type(card) is list:
            self.cards = self.cards + card
        else:
            self.cards.append(card)

    def __init__(self, cards=[]):
        self.cards = []


if __name__ == '__main__':
    g = Game()
    g.main_loop()
