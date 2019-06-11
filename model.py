# Model representing the hands of players in Hanabi
from external.mlsolver.mlsolver.kripke import KripkeStructure, World
from external.mlsolver.mlsolver.formula import Atom, And, Not, Or, Box_a, Box_star
from gameComponents import Deck
from collections import Counter

class HanabiModel:
    def __init__(self, deck, players):
        self.deck = deck
        self.players = players
        self.generate_model()

        knowledge_base = []

    def generate_model(self):
        self.worlds = self.create_worlds()
        self.relations = self.set_relations()

        self.relations.update(self.add_reflexive_edges(self.worlds, self.relations))
        self.relations.update(self.add_symmetric_edges(self.relations))

        self.ks = KripkeStructure(self.worlds, self.relations)

    def create_worlds(self):
        worlds = []
        suits = self.deck.colours_in_game
        ranks = list(set(self.deck.values_in_game))
        rank_counts = Counter(ranks)

        # Create each unique card
        cards = []
        for colour in suits:
            for number in ranks:
                cards.append(colour + number)

        # Create worlds
        # TODO Find way to iteratively construct each possible world. Also we need to find out if we need to rewrite the model checker to allow numbers for atoms instead of booleans.

        return worlds



    def set_relations(self):
        relations = []
        return relations

    # Taken from external.mlsolver.mlsolver.model
    def add_symmetric_edges(relations):
        """Routine adds symmetric edges to Kripke frame
        """
        result = {}
        for agent, agents_relations in relations.items():
            result_agents = agents_relations.copy()
            for r in agents_relations:
                x, y = r[1], r[0]
                result_agents.add((x, y))
            result[agent] = result_agents
        return result

    def add_reflexive_edges(worlds, relations):
        """Routine adds reflexive edges to Kripke frame
        """
        result = {}
        for agent, agents_relations in relations.items():
            result_agents = agents_relations.copy()
            for world in worlds:
                result_agents.add((world.name, world.name))
                result[agent] = result_agents
        return result