import logging
import gzip
from pandas import DataFrame
import pyarrow as pa 
import pyarrow.parquet as pq
from pathlib import Path

from metar_station.utils.io import get_data_dir


logger = logging.getLogger(__name__)


def station_raw_csv_path(cache_key: str) -> Path:
    filepath = get_data_dir().joinpath("01-raw_station_csv_gz", f"{cache_key}.csv.gz")
    logger.info(f"Generating csv cache path: {filepath}")
    return filepath


def write_station_raw_csv(filepath: Path, data: bytes) -> None:
    filepath.parent.mkdir(parents=True, exist_ok=True)  #  create datastore if doesn't exist
    logger.info(f"Saving compressed csv file: {filepath}")
    with gzip.open(filepath, "wb") as f:
        f.write(data)


def station_raw_parquet_path() -> Path:
    root_path = get_data_dir().joinpath("02-raw_station_pq")
    logger.info(f"Generating parquet root path: {root_path}")
    return root_path


def write_station_raw_parquet(root_path: Path, df: DataFrame) -> None:
    root_path.parent.mkdir(parents=True, exist_ok=True)  #  create datastore if doesn't exist
    logger.info(f"Saving parquet dataset: {root_path}")
    df.to_parquet(root_path, engine="pyarrow", index=False, partition_cols=["year", "month", "station"])
