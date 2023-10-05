import os

import pandas as pd

from utils import BASE_DIR


class DataFrameMixin:
    @classmethod
    def find_file(cls, filename, search_path):
        for root, dirs, files in os.walk(search_path):
            if filename in files:
                return os.path.join(root, filename)

    @classmethod
    def get_data_frame(cls):
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

    @classmethod
    def get_data_frames(cls):
        all_dataframes = []

        directory_path = BASE_DIR / 'frames'

        for root, dirs, files in os.walk(directory_path):
            files = sorted(files)
            for file in files:
                if file.endswith('.csv'):
                    file_path = os.path.join(root, file)
                    dataframe = pd.read_csv(file_path)
                    all_dataframes.append(dataframe)

        return all_dataframes
