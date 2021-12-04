import pendulum
import pytest

from metar_station.raw import download


def test_query_populated():
    query = download.StationPeriodQuery("EGPN", "2020-01")

    assert query.station == "EGPN"
    assert query.cache_key == "EGPN_2020-01"
    assert query.period_start == pendulum.datetime(2020, 1, 1, 0, 0, 0)
    assert query.period_end == pendulum.datetime(2020, 1, 31, 23, 59, 59, 999999)


def test_build_station_raw_url():
    query = download.StationPeriodQuery("EGPN", "2020-01") 
    url, _ = download.build_station_raw_url(query)
    assert url == "https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py"


def test_build_station_raw_url_payload():
    query = download.StationPeriodQuery("EGPN", "2020-01")
    _, payload = download.build_station_raw_url(query)

    expected = dict(
        station="EGPN",
        data="all",
        year1="2020",
        month1="1",
        day1="1",
        year2="2020",
        month2="1",
        day2="31",
        tz="Etc/UTC",
        format="onlycomma",
        latlon="yes",
        elev="yes",
        missing="null",
        trace="null",
        direct="no",
        report_type=["1", "2"],
    )

    assert payload == expected
