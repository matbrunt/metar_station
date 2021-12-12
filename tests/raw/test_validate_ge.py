import pytest
import pandas as pd
from pandera import DataFrameSchema

from metar_station.raw import validate_ge
from metar_station.raw.download import StationPeriodQuery


def test_build_validations():
   query = StationPeriodQuery("EGPN", "2020-01") 

   result = validate_ge._build_validations(query, "raw_station.warning")[0]

   assert result["batch_request"]["data_connector_query"]["batch_filter_parameters"]["year"] == "2020"
   assert result["batch_request"]["data_connector_query"]["batch_filter_parameters"]["month"] == "01"
   assert result["batch_request"]["data_connector_query"]["batch_filter_parameters"]["station"] == "EGPN"
   assert result["expectation_suite_name"] == "raw_station.warning"


def test_check_data(mocker):
    query = StationPeriodQuery("EGPN", "2020-01")

    mock_context = mocker.Mock()

    mock_validations = mocker.patch("metar_station.raw.validate_ge._build_validations")

    result = validate_ge._check_data(query, mock_context)

    mock_context.run_checkpoint.assert_called_once_with(
        checkpoint_name="chk_raw_station",
        validations=mock_validations.return_value
    )

    mock_validations.assert_called_once_with(query, "raw_station.warning")

    assert result == mock_context.run_checkpoint.return_value


def test_validate_failed(mocker):
    query = StationPeriodQuery("EGPN", "2020-01")

    mock_context = mocker.patch("great_expectations.get_context")

    mock_check_data = mocker.patch("metar_station.raw.validate_ge._check_data")
    mock_check_data.return_value.success = False

    logger = mocker.patch("logging.Logger.info")

    result = validate_ge.validate(query)

    mock_check_data.assert_called_once_with(query, mock_context.return_value)

    logger.assert_called_once_with("EGPN failed validation for download")

    assert result == False


def test_validate_success(mocker):
    query = StationPeriodQuery("EGPN", "2020-01")

    mock_context = mocker.patch("great_expectations.get_context")

    mock_check_data = mocker.patch("metar_station.raw.validate_ge._check_data")
    mock_check_data.return_value.success = True

    logger = mocker.patch("logging.Logger.info")

    result = validate_ge.validate(query)

    mock_check_data.assert_called_once_with(query, mock_context.return_value)

    assert not logger.called

    assert result == True