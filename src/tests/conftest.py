import pytest
from starlette.testclient import TestClient

from api.main import app

# https://docs.pytest.org/en/latest/how-to/fixtures.html


@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client