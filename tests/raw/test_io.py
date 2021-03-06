import pytest
import pandas as pd
import numpy as np
from pandas.testing import assert_frame_equal
from pathlib import Path
from secrets import token_bytes

from metar_station.raw import io


def test_station_raw_csv_path(mocker):
    cache_key = "foobar"
    expected_path = Path("/foo/bar/01-raw_station_csv_gz/foobar.csv.gz")

    mocker.patch("metar_station.raw.io.get_data_dir", return_value=Path("/foo/bar"))
    logger = mocker.patch("logging.Logger.info")
    assert io.station_raw_csv_path(cache_key) == expected_path
    logger.assert_called_once_with(f"Generating csv cache path: {expected_path}")


def test_station_raw_parquet_path(mocker):
    expected_path = Path("/foo/bar/02-raw_station_pq/")

    mocker.patch("metar_station.raw.io.get_data_dir", return_value=Path("/foo/bar"))
    logger = mocker.patch("logging.Logger.info")
    assert io.station_raw_parquet_path() == expected_path
    logger.assert_called_once_with(f"Generating parquet root path: {expected_path}")


@pytest.mark.slow
def test_write_station_raw_csv(mocker, tmp_path):
    logger = mocker.patch("logging.Logger.info")
    tmp_file = tmp_path / "station_raw.csv.gz"

    io.write_station_raw_csv(tmp_file, token_bytes(16))

    assert tmp_file.exists()
    logger.assert_called_once_with(f"Saving compressed csv file: {tmp_file}")


@pytest.mark.slow
def test_write_station_raw_parquet(mocker, tmp_path):
    logger = mocker.patch("logging.Logger.info")

    rng = np.random.default_rng()
    expected_df = pd.DataFrame(rng.integers(0, 100, size=(100, 4)), columns=list("ABCD"))
    expected_df["year"] = pd.Categorical([2020] * len(expected_df))
    expected_df["month"] = pd.Categorical([1] * len(expected_df))
    expected_df["station"] = pd.Categorical(["somestation"] * len(expected_df))

    io.write_station_raw_parquet(tmp_path, expected_df)

    assert tmp_path.exists()
    logger.assert_called_once_with(f"Saving parquet dataset: {tmp_path}")

    df = pd.read_parquet(tmp_path)
    assert_frame_equal(df, expected_df)
