import numpy as np

from individual import Individual

from . import mixins


class Population(
    mixins.SelectionMixin,
    mixins.CrossingMixin,
    mixins.MutationMixin,
):
    @classmethod
    def create_population(cls, constants):
        population = Population(constants)
        population.extend([Individual(constants) for _ in range(constants.POPULATION_SIZE)])
        return population

    def get_fitness_values(self):
        return np.array([ind.fitness for ind in self])

    def _create_population_with_constants(self):
        return Population(self.constants)
