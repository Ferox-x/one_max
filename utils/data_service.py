import datetime
import pandas
import uuid

from pathlib import Path

from utils import BASE_DIR


class DataSaver:
    FRAMES_DIR = BASE_DIR / "frames"

    @classmethod
    def _check_or_create_dir(cls, path: Path) -> bool:
        if not path.is_dir():
            path.mkdir()
        return True

    @classmethod
    def save_data_frame(cls, data_frame: pandas.DataFrame, index: int) -> None:
        cls._check_or_create_dir(cls.FRAMES_DIR)
        date = datetime.datetime.now().strftime("%d_%m_%Y")
        path_to_file = cls.FRAMES_DIR / date
        cls._check_or_create_dir(path_to_file)
        data_frame.to_csv(path_to_file / str(uuid.uuid4()), index=False)
