import pandas as pd
import numpy as np

from evolution import EvolutionaryOptimizer

from utils.data_service import DataSaver
from utils import ENV_CONSTANTS


def job(index):
    np.random.seed()
    constants = EvolutionaryOptimizer.randomize_constants()
    data_frame = pd.DataFrame()

    for _ in range(int(ENV_CONSTANTS.get("TOTAL_GENERATIONS", 1))):  # Цикл для генерации новых генов
        (
            max_fitness_values,
            mean_fitness_values,
            generation,
            best_individual_fitness,
        ) = EvolutionaryOptimizer.evolve(consts=constants)
        constants_data = {
            "ONE_MAX": constants.ONE_MAX,
            "GENS_SIZE": constants.GENS_SIZE,
            "POPULATION_SIZE": constants.POPULATION_SIZE,
            "P_CROSSOVER": constants.P_CROSSOVER,
            "P_MUTATION": constants.P_MUTATION,
            "MAX_GENERATIONS": constants.MAX_GENERATIONS,
            "TOURNAMENT_SIZE": constants.TOURNAMENT_SIZE,
            "SELECTION_TYPE": constants.SELECTION_TYPE,
            "CROSSING_TYPE": constants.CROSSING_TYPE,
            "MUTATION_POWER": constants.MUTATION_POWER,
            "EQUAL_SELECTION_CHANCE": constants.EQUAL_SELECTION_CHANCE,
            "HIGH_MUTATION_POWER": constants.HIGH_MUTATION_POWER,
            "LOW_MUTATION_POWER": constants.LOW_MUTATION_POWER,
        }
        if best_individual_fitness < 100 and generation == constants.MAX_GENERATIONS:
            generation = pd.NA
        results = {
            "BEST_FITNESS": best_individual_fitness,
            "GENERATION": generation,
            "MAX_FITNESS_VALUES": str(max_fitness_values),
            "MEAN_FITNESS_VALUES": str(mean_fitness_values),
        }
        population_frame = pd.DataFrame({**constants_data, **results}, index=[0])
        data_frame = pd.concat([data_frame, population_frame])
    DataSaver.save_data_frame(
        data_frame=data_frame,
        index=index,
    )
