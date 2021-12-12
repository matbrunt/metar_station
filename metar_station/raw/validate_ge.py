import logging
import great_expectations as ge
from great_expectations.data_context.data_context import DataContext
from great_expectations.checkpoint.types.checkpoint_result import CheckpointResult
from pathlib import Path

from metar_station.raw.download import StationPeriodQuery


logger = logging.getLogger(__name__)


def _build_validations(query: StationPeriodQuery, expectation_suite_name: str) -> list:
    return [
        {
            "batch_request": {
                "datasource_name": "ds_root",
                "data_connector_name": "dc_data",
                "data_asset_name": "raw_csv",
                "data_connector_query": {
                    "batch_filter_parameters": {
                        "year": query.period_start.strftime("%Y"),
                        "month": query.period_start.strftime("%m"),
                        "station": query.station,
                    }
                }
            },
            "expectation_suite_name": expectation_suite_name,
        },
    ]

def _check_data(query: StationPeriodQuery, context: DataContext) -> CheckpointResult:
    checkpoint_name = "chk_raw_station"
    expectation_suite_name = "raw_station.warning"

    checkpoint_run_result: CheckpointResult = context.run_checkpoint(
        checkpoint_name=checkpoint_name,
        validations=_build_validations(query, expectation_suite_name),
    )

    return checkpoint_run_result


def validate(query: StationPeriodQuery) -> bool:
    context = ge.get_context()

    checkpoint_run_result = _check_data(query, context)
    if not checkpoint_run_result.success:
        logger.info(f"{query.station} failed validation for download")

    return checkpoint_run_result.success
