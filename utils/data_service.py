import datetime
import os

import pandas as pd
import uuid

from pathlib import Path


from utils import FRAMES_DIR, RESULTS_DIR
from utils.core import DataFrameMixin


class DataSaver:
    @classmethod
    def _check_or_create_dir(cls, path: Path) -> bool:
        if not path.is_dir():
            path.mkdir()
        return True

    @classmethod
    def save_data_frame(cls, data_frame: pd.DataFrame, index: int) -> None:
        cls._check_or_create_dir(FRAMES_DIR)
        date = datetime.datetime.now().strftime("%d_%m_%Y")
        path_to_file = FRAMES_DIR / date
        cls._check_or_create_dir(path_to_file)
        data_frame.to_csv(path_to_file / f'{str(uuid.uuid4())}.csv', index=False)


class DataAnalyzer(DataFrameMixin):
    @classmethod
    def get_params(cls) -> pd.DataFrame:
        df = pd.DataFrame(columns=['Название файла', 'Номер параметров', 'Параметры'])
        index = 0
        for root, dirs, files in os.walk(FRAMES_DIR):
            files = sorted(files)
            for file in files:
                if file.endswith('.csv'):
                    data = pd.read_csv(os.path.join(root, file))
                    params = data.iloc[0, :13].tolist()
                    params = (
                        f'ONE_MAX: {params[0]}\n'
                        f'GENS_SIZE: {params[1]}\n'
                        f'POPULATION_SIZE: {params[2]}\n'
                        f'P_CROSSOVER: {params[3]}\n'
                        f'P_MUTATION: {params[4]}\n'
                        f'MAX_GENERATIONS: {params[5]}\n'
                        f'TOURNAMENT_SIZE: {params[6]}\n'
                        f'SELECTION_TYPE: {params[7]}\n'
                        f'CROSSING_TYPE: {params[8]}\n'
                        f'MUTATION_POWER: {params[9]}\n'
                        f'EQUAL_SELECTION_CHANCE: {params[10]}\n'
                        f'HIGH_MUTATION_POWER: {params[11]}\n'
                        f'LOW_MUTATION_POWER: {params[12]}\n'
                    )
                    df = pd.concat(
                        [
                            df,
                            pd.DataFrame(
                                {
                                    'Название файла': [file],
                                    'Номер параметров': f'P{index}',
                                    'Параметры': str(params),
                                }
                            ),
                        ],
                        ignore_index=True,
                    )
                    index += 1
        df.to_csv(RESULTS_DIR / 'params.csv')
        return df

    def create_best_found_csv(self) -> pd.DataFrame:
        params = pd.read_csv(RESULTS_DIR / 'params.csv')
        data = dict()
        file_names = params['Название файла']
        params_number = params['Номер параметров']
        for index, file_name in enumerate(file_names):
            data_frame = pd.read_csv(self.find_file(file_name, FRAMES_DIR))
            series = data_frame['BEST_FITNESS']
            data[params_number[index]] = series
        df = pd.DataFrame(data)
        df.to_csv(RESULTS_DIR / 'best_found.csv')
        return df

    def create_generation_csv(self) -> pd.DataFrame:
        data_frames = self.get_data_frames()
        data = dict()
        for index, data_frame in enumerate(data_frames):
            series = data_frame['GENERATION']
            data[f'P{index}'] = series
        df = pd.DataFrame(data)
        df.to_csv(RESULTS_DIR / 'generation.csv')
        return df

    def create_max_fitness_values_csv(self) -> pd.DataFrame:
        data_frames = self.get_data_frames()
        data = dict()
        for index, data_frame in enumerate(data_frames):
            series = data_frame['MAX_FITNESS_VALUES']
            data[f'P{index}'] = series
        df = pd.DataFrame(data)
        df.to_csv(RESULTS_DIR / 'generation.csv')
        return df


if __name__ == '__main__':
    analyzer = DataAnalyzer()
    # analyzer.get_params()
    best_found = analyzer.create_best_found_csv()
    # generation = analyzer.create_generation_csv()
