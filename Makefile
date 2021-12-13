mypy:
	mypy metar_station tests

black:
	black metar_station tests

flake:
	flake8 metar_station tests

unit:
	pytest -q -m "not slow" tests

test: mypy black flake
	pytest -q tests

.PHONY: mypy black flake unit
