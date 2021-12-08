import click
import gzip
import os
import datetime
import prefect
import pendulum
import requests
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path
from prefect import task, Flow, Parameter
from prefect.engine.results import LocalResult
from prefect.engine.signals import SKIP, FAIL

from metar_station.raw import (
    download,
    io,
    transform,
    validate_pandera as validator
)


@task
def build_query(station: str, period: str) -> download.StationPeriodQuery:
    logger = prefect.context.logger

    query = download.StationPeriodQuery(station, period)
    logger.info(query)
    return query


@task(max_retries=3, retry_delay=datetime.timedelta(seconds=2))
def fetch_station_data(query: download.StationPeriodQuery) -> Path:
    logger = prefect.context.logger

    filepath = io.station_raw_csv_path(query.cache_key)

    if filepath.exists():
        logger.info(f"Download file '{filepath}' already exists.")
        return filepath

    logger.info(f"Fetching raw station METAR data ({query.station}, {query.period_start.strftime('%Y-%m')}) #{prefect.context.task_run_count}...")

    url, payload = download.build_station_raw_url(query)
    resp = requests.get(url, params=payload)
    logger.info(resp.url)
    resp.raise_for_status()

    io.write_station_raw_csv(filepath, resp.content)

    return filepath


@task()
def process_data(filepath: Path) -> pd.DataFrame:
    logger = prefect.context.logger

    logger.info(f"Loading dataset '{filepath}'...")
    df = (
        pd.read_csv(filepath)
        .pipe(transform.parse_observation_dt)
        .pipe(transform.add_partition_cols)
    )

    logger.info(f"Loaded dataset ({df.shape}): {filepath}")

    return df


@task(log_stdout=True)
def validate(query: download.StationPeriodQuery, df: pd.DataFrame) -> pd.DataFrame:
    logger = prefect.context.logger

    logger.info(f"Running data validation against {query.station} raw data.")
    station_raw_schema = validator.build_station_raw_schema(query.station)
    validated_df = validator.validate_df(df, station_raw_schema)

    return validated_df


@task
def write_parquet(df: pd.DataFrame) -> None:
    logger = prefect.context.logger

    logger.info(f"Writing parquet dataset")
    root_path = io.station_raw_parquet_path()
    io.write_station_raw_parquet(root_path, df)


def make_flow():
    with Flow("Fetch monthly raw station METAR") as flow:
        station = Parameter("station", default="EGPN")
        period = Parameter("period", required=True)

        query = build_query(station, period)
        raw_filepath = fetch_station_data(query)
        raw_pdf = process_data(raw_filepath)
        validated_df = validate(query, raw_pdf)
        write_parquet(validated_df)

    return flow


@click.group()
def cli():
    pass


@cli.command()
def register():
    flow = make_flow()


@cli.command()
@click.option("--station", default="EGPN", help="METAR station to fetch")
@click.argument("period")
def run(station: str, period: str) -> None:
    flow = make_flow()
    flow.run(context=dict(), parameters=dict(station=station, period=period))


if __name__ == "__main__":
    load_dotenv()
    cli()
