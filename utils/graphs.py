import matplotlib.pyplot as plt

from utils import PLOTS_DIR
from utils.core import DataFrameMixin


class GraphsCreator(DataFrameMixin):
    def __init__(self):
        self._output_folder = PLOTS_DIR
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

    def create_graph(self, param, title, label, name):
        data_frame = self.get_data_frame()
        x_values = data_frame['GENERATION']
        y_values = data_frame[param]

        plt.figure(figsize=(10, 6))
        plt.plot(x_values, y_values, marker="o", linestyle=None)
        plt.title(title)
        plt.xlabel("generation")
        plt.ylabel(label)
        plt.grid(True)
        self._save(name)

    def _save(self, name):
        graph_filename = self._output_folder / name
        plt.savefig(graph_filename)


def create_graphs():
    creator = GraphsCreator()
    for param, title, x_label, name in creator.plot_params:
        creator.create_graph(param, title, x_label, name)


if __name__ == '__main__':
    create_graphs()
