import numpy as np

from dataclasses import dataclass
from population import Population
from population import mixins as population_mixins
from utils import ENV_CONSTANTS


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
        if bool(int(ENV_CONSTANTS.get('RANDOM'))):
            SELECTION_TYPE = np.random.randint(1, len(population_mixins.SelectionMixin.SelectionTypeChoice))
            CROSSING_TYPE = np.random.randint(1, len(population_mixins.CrossingMixin.CrossingTypeChoice))
            MUTATION_POWER = np.random.randint(1, len(population_mixins.MutationMixin.PowerOfMutationChoices))
            return PopulationConstants(
                ONE_MAX=100,
                GENS_SIZE=100,
                POPULATION_SIZE=np.random.randint(100, 150),
                P_CROSSOVER=np.random.randint(75, 101) / 100,
                P_MUTATION=np.random.randint(0, 26) / 100,
                MAX_GENERATIONS=np.random.randint(50, 150),
                TOURNAMENT_SIZE=np.random.randint(2, 4),
                SELECTION_TYPE=SELECTION_TYPE,
                CROSSING_TYPE=CROSSING_TYPE,
                MUTATION_POWER=MUTATION_POWER,
                EQUAL_SELECTION_CHANCE=0.25,
                HIGH_MUTATION_POWER=np.random.randint(3, 5),
                LOW_MUTATION_POWER=np.random.randint(3, 5),
            )

        return PopulationConstants(
            ONE_MAX=int(ENV_CONSTANTS.get("ONE_MAX")),
            GENS_SIZE=int(ENV_CONSTANTS.get("GENS_SIZE")),
            POPULATION_SIZE=int(ENV_CONSTANTS.get("POPULATION_SIZE")),
            P_CROSSOVER=float(ENV_CONSTANTS.get("P_CROSSOVER")),
            P_MUTATION=float(ENV_CONSTANTS.get("P_MUTATION")),
            MAX_GENERATIONS=int(ENV_CONSTANTS.get("MAX_GENERATIONS")),
            TOURNAMENT_SIZE=int(ENV_CONSTANTS.get("TOURNAMENT_SIZE")),
            SELECTION_TYPE=int(ENV_CONSTANTS.get("SELECTION_TYPE")),
            CROSSING_TYPE=int(ENV_CONSTANTS.get("CROSSING_TYPE")),
            MUTATION_POWER=int(ENV_CONSTANTS.get("MUTATION_POWER")),
            EQUAL_SELECTION_CHANCE=float(ENV_CONSTANTS.get("EQUAL_SELECTION_CHANCE")),
            HIGH_MUTATION_POWER=int(ENV_CONSTANTS.get("HIGH_MUTATION_POWER")),
            LOW_MUTATION_POWER=int(ENV_CONSTANTS.get("LOW_MUTATION_POWER")),
        )

    @classmethod
    def evolve(cls, consts):
        population = Population.create_population(
            constants=consts,
        )
        fitness_values = population.get_fitness_values()
        generation_counter = 0

        max_fitness = 0
        max_fitness_values = list()
        mean_fitness_values = list()
        while max(fitness_values) < consts.ONE_MAX and generation_counter < consts.MAX_GENERATIONS:
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
        return max_fitness_values, mean_fitness_values, generation_counter, max_fitness
