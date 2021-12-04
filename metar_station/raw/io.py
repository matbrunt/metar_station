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


def station_raw_parquet_path(cache_key: str) -> Path:
    filepath = get_data_dir().joinpath("02-raw_station_pq", f"{cache_key}.parquet")
    logger.info(f"Generating parquet cache path: {filepath}")
    return filepath


def write_station_raw_parquet(filepath: Path, df: DataFrame) -> None:
    filepath.parent.mkdir(parents=True, exist_ok=True)  #  create datastore if doesn't exist
    logger.info(f"Saving parquet file: {filepath}")
    table = pa.Table.from_pandas(df)
    pq.write_table(table, filepath, flavor="spark")
