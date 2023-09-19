import random

from population import Population
from dataclasses import dataclass


@dataclass
class PopulationConstants:
    ONE_MAX: int
    GENS_SIZE: int
    POPULATION_SIZE: int
    P_CROSSOVER: float
    P_MUTATION: float
    MAX_GENERATIONS: int


class EvolutionaryOptimizer:
    @classmethod
    def randomize_constants(cls):
        _constants = PopulationConstants(
            ONE_MAX=100,
            GENS_SIZE=random.randint(50, 150),
            POPULATION_SIZE=random.randint(50, 150),
            P_CROSSOVER=random.random(),
            P_MUTATION=random.random(),
            MAX_GENERATIONS=random.randint(50, 150),
        )
        return _constants

    @classmethod
    def evolve(cls, consts):
        population = Population.create_population(
            constants=consts,
        )
        fitness_values = population.get_fitness_values()
        generation_counter = 0

        max_fitness_values = []
        mean_fitness_values = []
        while (
            max(fitness_values) < consts.ONE_MAX
            and generation_counter < consts.MAX_GENERATIONS
        ):
            generation_counter += 1
            offspring = population.tournament()

            offspring.crossing()
            offspring.mutation()

            population[:] = offspring
            fitness_values = population.get_fitness_values()
            max_fitness = max(fitness_values)
            mean_fitness = sum(fitness_values) / len(population)
            max_fitness_values.append(max_fitness)
            mean_fitness_values.append(mean_fitness)

        return max_fitness_values, mean_fitness_values, generation_counter
