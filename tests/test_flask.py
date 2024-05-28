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


def test_show_summary_route_known_email(client):
    with app.app_context():
        response = client.post(
            url_for("show_summary"),
            data={"email": "john@simplylift.co"},
        )
    assert response.status_code == 200
    assert b'Welcome' in response.data


def test_show_summary_route_unknown_email(client):
    with app.app_context():
        response = client.post(
            url_for("show_summary"),
            data={"email": "unknown@email.test"},
            follow_redirects=True
        )
        assert response.status_code == 200
        assert b'Email not found' in response.data


def test_show_summary_route_empty_email(client):
    with app.app_context():
        response = client.post(
            url_for("show_summary"),
            data={"email": ""},
            follow_redirects=True
        )
        assert response.status_code == 200
        assert b'Email not found' in response.data
