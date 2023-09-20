import numpy as np


class Individual:
    def __init__(self, constants):
        self.constants = constants
        self.gens = np.random.randint(
            0, 2, size=self.constants.GENS_SIZE, dtype=np.int32
        )

    @property
    def fitness(self):
        return np.sum(self.gens)

    def clone(self):
        new_individual = Individual(self.constants)
        new_individual.gens = self.gens.copy()
        return new_individual

    def __str__(self):
        return str(self.gens)
