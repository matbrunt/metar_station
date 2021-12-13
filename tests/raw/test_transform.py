import pandas as pd
from pandas.testing import assert_series_equal

from metar_station.raw import transform


def test_parse_observation_dt():
    base_df = pd.DataFrame(
        {
            "valid": ["2020-01-01 11:50:00", "2020-01-05 09:34:26"],
        }
    )

    df = transform.parse_observation_dt(base_df)

    assert pd.api.types.is_datetime64_dtype(df["valid"])
    assert_series_equal(df["valid"], pd.to_datetime(base_df["valid"]))


def test_add_partition_cols():
    base_df = pd.DataFrame(
        {
            "valid": ["2020-01-01 11:50:00", "2020-01-05 09:34:26"],
        }
    )
    base_df["valid"] = pd.to_datetime(base_df["valid"], format="%Y-%m-%d %H:%M:%S")

    df = transform.add_partition_cols(base_df)

    assert all([x in ["valid", "year", "month"] for x in df.columns])
