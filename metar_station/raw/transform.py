import pandas as pd


def parse_observation_dt(df: pd.DataFrame) -> pd.DataFrame:
    df["valid"] = pd.to_datetime(df["valid"], format="%Y-%m-%d %H:%M:%S")

    return df


def add_partition_cols(df: pd.DataFrame) -> pd.DataFrame:
    df["year"] = df["valid"].dt.strftime("%Y")
    df["month"] = df["valid"].dt.strftime("%m")

    return df
