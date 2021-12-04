import pendulum
import pytest

from metar_station.utils import prefect


def test_build_backfill_context():
    today = "2020-01-15"
    expected = dict(
        date=pendulum.datetime(2020, 1, 15),
        today=today,
        today_nodash="20200115",
        yesterday="2020-01-14",
        yesterday_nodash="20200114",
        tomorrow="2020-01-16",
        tomorrow_nodash="20200116",
    )

    assert prefect.build_backfill_dt_context(today) == expected
