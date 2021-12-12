import logging
import pandas as pd
import pandera as pa
from pandera import Column, Check, DataFrameSchema
from pandera.errors import SchemaErrors
from typing import Optional


logger = logging.getLogger(__name__)


CLOUD_COVERAGE_CODES = [
    "CAVOK",  # Ceiling and Visibility OK (not used in US)
    "SKC",  # Sky clear (clear below 12,000 ft for ASOS/AWOS)
    "NSC",  # No significant clouds
    "FEW",  # 1/8 to 2/8 sky cover
    "SCT",  # 3/8 to 4/8 sky cover
    "BKN",  # 5/8 to 7/8 sky cover
    "OVC",  # 8/8 sky cover
    "VV",  # vertical visibility when sky obscured (VV100's of feet)
]


def build_station_raw_schema(station: str) -> DataFrameSchema:
    logger.info(f"Building validation schema for {station} raw station data.")
    return DataFrameSchema({
        "station": Column(str, checks=[Check.equal_to(station)]),  # metar station ID
        "valid": Column(pa.dtypes.Timestamp, coerce=True),  # observation datetime
        "lon": Column(float, checks=[Check.in_range(-180.0, 180.0)]),  # longitude
        "lat": Column(float, checks=[Check.in_range(-90.0, 90.0)]),  # latitude
        "elevation": Column(float, nullable=False),  # metar station elevation (m)
        "tmpf": Column(float, nullable=True),  # temperature F
        "dwpf": Column(float, nullable=True),  # dewpoint F
        "relh": Column(float, checks=[Check.less_than_or_equal_to(max_value=100.0)], nullable=True),  # relative humidity (%)
        "drct": Column(float, checks=[Check.in_range(0.0, 360.0)], nullable=True),  # wind direction (degrees)
        "sknt": Column(float, checks=[Check.greater_than_or_equal_to(min_value=0.0)], nullable=True),  # wind speed (kts)
        "alti": Column(float, checks=[Check.greater_than_or_equal_to(min_value=0.0)]),  # pressure altimeter (in)
        "mslp": Column(float, checks=[Check.greater_than_or_equal_to(min_value=0.0)], coerce=True, nullable=True),  # sea level pressure (millibar)
        "vsby": Column(float, checks=[Check.in_range(0.0, 10.0)]),  # visbility (miles)
        "skyc\d": Column(str, checks=[Check.isin(CLOUD_COVERAGE_CODES, raise_warning=True)], coerce=True, nullable=True, regex=True),  # sky coverage
        "skyl\d": Column(float, checks=[Check.in_range(0.0, 12_000.0)], coerce=True, nullable=True, regex=True),  # sky altitude (ft)
        "metar": Column(str, checks=[Check.str_startswith(station)]),
    })


def validate_df(df: pd.DataFrame, schema: DataFrameSchema) -> Optional[pd.DataFrame]:
    try:
        validated_df = schema.validate(df, lazy=True)
        logger.info(f"Validation (input shape: {df.shape}) (output shape: {validated_df.shape})")
        return validated_df
    except SchemaErrors as err:
        logger.warning("Schema errors and failure cases:")
        logger.warning(err.failure_cases)

    return None
