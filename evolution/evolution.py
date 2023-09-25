import random

from population import Population
from dataclasses import dataclass
from population import mixins as population_mixins


@dataclass
class PopulationConstants:
    ONE_MAX: int
    GENS_SIZE: int
    POPULATION_SIZE: int
    P_CROSSOVER: float
    P_MUTATION: float
    MAX_GENERATIONS: int
    TOURNAMENT_SIZE: int
    SELECTION_TYPE: int
    CROSSING_TYPE: int
    EQUAL_SELECTION_CHANCE: float
    MUTATION_POWER: int
    HIGH_MUTATION_POWER: int
    LOW_MUTATION_POWER: int


class EvolutionaryOptimizer:
    @classmethod
    def randomize_constants(cls):
        SELECTION_TYPE = random.randint(
            1, len(population_mixins.SelectionMixin.SelectionTypeChoice)
        )
        CROSSING_TYPE = random.randint(
            1, len(population_mixins.CrossingMixin.CrossingTypeChoice)
        )
        MUTATION_POWER = random.randint(
            1, len(population_mixins.MutationMixin.PowerOfMutationChoices)
        )

        return PopulationConstants(
            ONE_MAX=100,
            GENS_SIZE=100,
            POPULATION_SIZE=random.randint(100, 150),
            P_CROSSOVER=random.random(),
            P_MUTATION=random.random(),
            MAX_GENERATIONS=random.randint(50, 150),
            TOURNAMENT_SIZE=random.randint(2, 4),
            SELECTION_TYPE=SELECTION_TYPE,
            CROSSING_TYPE=CROSSING_TYPE,
            MUTATION_POWER=MUTATION_POWER,
            EQUAL_SELECTION_CHANCE=0.25,
            HIGH_MUTATION_POWER=random.randint(3, 5),
            LOW_MUTATION_POWER=random.randint(3, 5),
        )

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
            offspring = population.selection()

            offspring.crossing()
            offspring.mutation()

            population[:] = offspring
            fitness_values = population.get_fitness_values()
            max_fitness = fitness_values.max()
            mean_fitness = fitness_values.sum() / len(population)
            max_fitness_values.append(max_fitness)
            mean_fitness_values.append(mean_fitness)

        return max_fitness_values, mean_fitness_values, generation_counter
