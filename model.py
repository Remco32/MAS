# Model representing the hands of players in Hanabi
from external.mlsolver.mlsolver.kripke import KripkeStructure, World
from external.mlsolver.mlsolver.formula import Atom, And, Not, Or, Box_a, Box_star
from gameComponents import Deck
from collections import Counter
from itertools import permutations
import gameSettings

class HanabiModel:
    def __init__(self, deck, players):
        self.deck = deck
        self.players = players
        self.generate_model()

    def generate_model(self):
        self.worlds = self.create_worlds()
        self.relations = self.set_relations()

        self.ks = KripkeStructure(self.worlds, self.relations)

    def create_worlds(self):
        worlds = []
        suits = self.deck.colours_in_game
        ranks = list(set(self.deck.values_in_game))
        rank_counts = Counter(ranks)

        # Create each unique card
        cards = []
        for colour in suits:
            for number in self.deck.values_in_game:
                cards.append(colour + number)

        # Generate all possible hands
        hands = permutations(cards, gameSettings.hand_size)

        # Create worlds


        return worlds



    def set_relations(self):
        relations = {}
        # Create relations between all worlds
        world_relations = {}
        for origin in self.worlds:
            for dest in self.worlds:
                world_relations.add((origin, dest))

        # Set relations for each player
        for player in self.players:
            relations[player] = {
                world_relations
            }
        return relations