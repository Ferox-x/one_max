import random


class Individual:
    def __init__(self, constants):
        self.constants = constants
        self.gens = [random.randint(0, 1) for _ in range(self.constants.GENS_SIZE)]

    @property
    def fitness(self):
        return sum(self.gens)

    def clone(self):
        new_individual = Individual(self.constants)
        new_individual.gens = self.gens.copy()
        return new_individual

    def __str__(self):
        return str(self.gens)
