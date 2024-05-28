import pytest
from flask import url_for

from server import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_index_route(client):
    with app.app_context():
        response = client.get(url_for("index"))
    assert response.status_code == 200
