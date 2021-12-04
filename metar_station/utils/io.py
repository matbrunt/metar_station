import os
from pathlib import Path


def get_root_dir() -> Path:
    root_dir = Path(__file__).parents[2]
    return root_dir.resolve()


def get_data_dir() -> Path:
    data_dir_env = os.getenv("DATA_DIR")

    if data_dir_env is not None and len(data_dir_env) > 0:
        data_dir = Path(data_dir_env)
    else:
        data_dir = Path(get_root_dir(), "data")

    return data_dir.resolve()
