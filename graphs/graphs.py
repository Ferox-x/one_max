import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path


class GraphsCreator:
    def __init__(self):
        self.data_frame = pd.read_csv("../frames/constants.csv")
        self._output_folder = Path("../plots")
        self.plot_params = [
            (
                "GENS_SIZE",
                "Зависимость generation от gens size",
                "GENS_SIZE",
                "gene_count_graph.png",
            ),
            (
                "POPULATION_SIZE",
                "Зависимость generation от population size",
                "population_size",
                "population_size_count_graph.png",
            ),
            (
                "P_CROSSOVER",
                "Зависимость generation от p crossover",
                "p_crossover",
                "p_crossover_count_graph.png",
            ),
            (
                "P_MUTATION",
                "Зависимость generation от p mutation",
                "p_mutation",
                "p_mutation_count_graph.png",
            ),
            (
                "MAX_GENERATIONS",
                "Зависимость generation от max generations",
                "max_generations",
                "max_generations_count_graph.png",
            ),
        ]

    def create_graph(self, param, title, xlabel, name):
        grouped_data = self.data_frame.groupby(param)["generation"].mean()
        x_values = grouped_data.index
        y_values = grouped_data.values

        plt.figure(figsize=(10, 6))
        plt.plot(x_values, y_values, marker="o", linestyle="-")
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel("generation")
        plt.grid(True)
        self._save(name)

    def _save(self, name):
        graph_filename = self._output_folder / name
        plt.savefig(graph_filename)


def create_graphs():
    creator = GraphsCreator()
    for param, title, x_label, name in creator.plot_params:
        creator.create_graph(param, title, x_label, name)
