import pytest
import pandas as pd
from pandera import DataFrameSchema, Column, Check
from pandera.errors import SchemaErrors
from pandas.testing import assert_frame_equal

from metar_station.raw import validate_pandera


"""
TODO: Replace with mocks and side effects to test only our wrapping function behaviour.
Using concrete implementations is an ugly hack instead of mocks and side effects,
as we're not testing pandera works (what if they change their interface), we're testing
the behaviour of our wrapping function handling the product of the pandera validation.
However I'm having issues throwing a mock SchemaErrors exception (normal exception is fine),
so because of time constraints I'll use concrete implementations for the moment and come back
to revisit this once I have a base project implementation.
"""
def test_validate_df_failed(mocker):
    df = pd.DataFrame({"colA": [1, 2, 3], "colB": ["a", "b", "c"]})

    logger_info = mocker.patch("logging.Logger.info")
    logger_warning = mocker.patch("logging.Logger.warning")

    schema = DataFrameSchema({
        "colA": Column(int, checks=[Check.in_range(2, 4)]),
        "colB": Column(str, checks=[Check.isin(["a", "b", "c", "d"])]),
        "colC": Column(str, checks=[Check.equal_to("a_constant_value")]),
    })

    result = validate_pandera.validate_df(df, schema)

    logger_info.assert_not_called()

    assert result is None

    logger_warning.assert_has_calls([
        mocker.call("Schema errors and failure cases:"),
        mocker.call(mocker.ANY)
    ], any_order=False)


def test_validate_df_success(mocker):
    input_df = pd.DataFrame({"colA": [1, 2, 3], "colB": ["a", "b", "c"]})
    output_df = pd.DataFrame({"colA": [1, 3]})

    logger_info = mocker.patch("logging.Logger.info")
    logger_warning = mocker.patch("logging.Logger.warning")

    mock_schema = mocker.Mock()
    mock_schema.validate.return_value = output_df

    result = validate_pandera.validate_df(input_df, mock_schema)

    mock_schema.validate.assert_called_once_with(input_df, lazy=True)
    logger_info.assert_called_once_with("Validation (input shape: (3, 2)) (output shape: (2, 1))")
    logger_warning.assert_not_called()

    assert_frame_equal(result, output_df)
