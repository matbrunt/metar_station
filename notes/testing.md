# Testing

We use [pytest-mock](https://github.com/pytest-dev/pytest-mock) as the mocking library for pytest.

## Commands

You can use the Makefile as a shorthand for running project commands.

`pytest -q tests/` to run all the tests.

`pytest -q -m "not slow" tests/` to run only tests not marked as 'slow'.

`pytest --markers` to display all available pytest markers (https://docs.pytest.org/en/6.2.x/mark.html).

`mypy metar_station tests` to static type check the code.

`black metar_station tests` to fix code formatting.

`flake8 metar_station tests` to run linting checks.

## Resources

- [Mocking Requests](https://requests-mock.readthedocs.io/en/latest/pytest.html)
- [PyTest: Monkey Patching](https://docs.pytest.org/en/latest/how-to/monkeypatch.html)
- [PyTest: How-To](https://docs.pytest.org/en/latest/how-to/index.html)
- [Mock assertions](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock)
- [Configuring MyPy in Poetry](https://mypy.readthedocs.io/en/stable/config_file.html#using-a-pyproject-toml-file)
- [Flake8](https://flake8.pycqa.org/en/latest/index.html)
  - note Flake8 [won't support config](https://github.com/PyCQA/flake8/issues/234) in `pyproject.toml` so we have to use a `.flake8` config file
- [Flake8: Selecting and ignoring violations](https://flake8.pycqa.org/en/latest/user/violations.html)
- [Flake8: Error / Violation Code](https://flake8.pycqa.org/en/latest/user/error-codes.html)
    - Also look at pycodestyle [error codes](https://pycodestyle.readthedocs.io/en/latest/intro.html#error-codes)

## Code Samples

**requests-mock**
```python
from correct.package import __BASE_URL
from requests import HTTPError


def test_get_employee(requests_mock):
    test_id = 'random-id'
    requests_mock.get(f'{__BASE_URL}/employee/{test_id}', json= {'name': 'awesome-mock'})
    resp = get_employee('random-id')
    assert resp == {'name': 'awesome-mock'}

def test_absent_employee(requests_mock):
    test_id = 'does_not_exist'
    requests_mock.get(f'{__BASE_URL}/employee/{test_id}', status_code=404)
    with pytest.raises(HTTPError):
        resp = get_employee(test_id)
```
