import logging
import pendulum
from dataclasses import dataclass, field, InitVar
from typing import Tuple, Dict, Union, Sequence


logger = logging.getLogger(__name__)


@dataclass
class StationPeriodQuery:
    """Query parameters for station monthly queries"""

    station: str
    period: InitVar[str]
    period_start: pendulum.DateTime = field(init=False)
    period_end: pendulum.DateTime = field(init=False)
    cache_key: str = field(init=False)

    def __post_init__(self, period):
        dt = pendulum.from_format(period, "YYYY-MM")
        self.period_start = dt.start_of("month")
        self.period_end = dt.end_of("month")
        self.cache_key = f"{self.station}_{self.period_start.strftime('%Y-%m')}"


def build_station_raw_url(query: StationPeriodQuery) -> Tuple[str, Dict[str, Union[str, Sequence[str]]]]:
    url = "https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py"
    payload = dict(
        station=query.station,
        data="all",
        year1=str(query.period_start.year),
        month1=str(query.period_start.month),
        day1=str(query.period_start.day),
        year2=str(query.period_end.year),
        month2=str(query.period_end.month),
        day2=str(query.period_end.day),
        tz="Etc/UTC",
        format="onlycomma",
        latlon="yes",
        elev="yes",
        missing="null",
        trace="null",
        direct="no",
        report_type=["1", "2"],
    )
    return url, payload
