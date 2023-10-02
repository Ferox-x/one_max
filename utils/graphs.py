import os
import matplotlib.pyplot as plt
import pandas as pd


from utils import BASE_DIR


class GraphsCreator:
    def __init__(self):
        self._output_folder = BASE_DIR / 'plots'
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

    def get_data_frame(self):
        all_dataframes = []

        directory_path = BASE_DIR / 'frames'

        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.endswith('.csv'):
                    file_path = os.path.join(root, file)
                    dataframe = pd.read_csv(file_path)
                    all_dataframes.append(dataframe)

        final_dataframe = pd.concat(all_dataframes, ignore_index=True)
        return final_dataframe

    def create_graph(self, param, title, xlabel, name):
        data_frame = self.get_data_frame()
        grouped_data = data_frame.groupby(param)["GENERATION"].mean()
        x_values = grouped_data.index
        y_values = grouped_data.values

        plt.figure(figsize=(10, 6))
        plt.plot(x_values, y_values, marker="o", linestyle=None)
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


if __name__ == '__main__':
    create_graphs()
