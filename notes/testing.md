# Testing

We use [pytest-mock](https://github.com/pytest-dev/pytest-mock) as the mocking library for pytest.

## Commands

`pytest -q tests/` to run all the tests.

`pytest -q -m "not slow" tests/` to run only tests not marked as 'slow'.

`pytest --markers` to display all available pytest markers (https://docs.pytest.org/en/6.2.x/mark.html).

`mypy metar_station tests` to static type check the code.

## Resources

https://requests-mock.readthedocs.io/en/latest/pytest.html

https://docs.pytest.org/en/latest/how-to/monkeypatch.html

https://docs.pytest.org/en/latest/how-to/index.html

[Mock assertions](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock)

https://mypy.readthedocs.io/en/stable/config_file.html#using-a-pyproject-toml-file

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
