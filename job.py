from evolution import EvolutionaryOptimizer
import pandas as pd


def job(index):
    constants = EvolutionaryOptimizer.randomize_constants()
    data_frame = pd.DataFrame()

    for _ in range(100):  # Цикл для генерации новых генов
        (
            max_fitness_values,
            mean_fitness_values,
            generation,
        ) = EvolutionaryOptimizer.evolve(consts=constants)
        constants_data = {
            "ONE_MAX": constants.ONE_MAX,
            "GENS_SIZE": constants.GENS_SIZE,
            "POPULATION_SIZE": constants.POPULATION_SIZE,
            "P_CROSSOVER": constants.P_CROSSOVER,
            "P_MUTATION": constants.P_MUTATION,
            "MAX_GENERATIONS": constants.MAX_GENERATIONS,
        }
        results = {
            "generation": generation,
            "max_fitness_values": str(max_fitness_values),
            "mean_fitness_values": str(mean_fitness_values),
        }
        population_frame = pd.DataFrame({**constants_data, **results}, index=[0])
        data_frame = pd.concat([data_frame, population_frame])

    return data_frame
