import datetime
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
    def create_best_found_csv(self) -> pd.DataFrame:
        data_frames = self.get_data_frames()
        data = dict()
        for index, data_frame in enumerate(data_frames):
            series = data_frame['BEST_FITNESS']
            data[f'P{index}'] = series
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
    best_found = analyzer.create_best_found_csv()
    generation = analyzer.create_generation_csv()
