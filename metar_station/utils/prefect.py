import pendulum
from typing import Dict, Union


def build_backfill_dt_context(backfill: str):
    run_dt = pendulum.from_format(backfill, "YYYY-MM-DD")

    yesterday = run_dt.subtract(days=1)
    tomorrow = run_dt.add(days=1)

    context: Dict[str, Union[str, pendulum.DateTime]] = {}

    context["date"] = run_dt
    context["today"] = run_dt.strftime("%Y-%m-%d")
    context["today_nodash"] = run_dt.strftime("%Y%m%d")
    context["yesterday"] = yesterday.strftime("%Y-%m-%d")
    context["yesterday_nodash"] = yesterday.strftime("%Y%m%d")
    context["tomorrow"] = tomorrow.strftime("%Y-%m-%d")
    context["tomorrow_nodash"] = tomorrow.strftime("%Y%m%d")

    return context
