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
        ranks = self.deck.values_in_game

        # Create each unique card
        cards = []
        for colour in suits:
            for number in ranks:
                cards.append([colour, number])

        # Generate all possible hands
        hands = permutations(cards, gameSettings.hand_size)

        # Create worlds
        template_assignment = self.generateTemplateAssignment(suits, ranks)
        for hand in hands:
            assignment = template_assignment.copy()
            card_index = 0
            for card in hand:
                assignment[str(card_index) + ":" + str(card(0))] = True
                assignment[str(card_index) + ":" + str(card(1))] = True
                card_index += 1
            worlds.append(World(str(hand), assignment))
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

    # Generate a template world truth assignment based on the hand size and cards in the game
    def generateTemplateAssignment(self, suits, ranks):
        assignment = {}
        for i in range(0, gameSettings.hand_size):
            for suit in suits:
                assignment[str(i) + ":" + str(suit)] = False
            for rank in ranks:
                assignment[str(i) + ":" + str(rank)] = False