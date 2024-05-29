import pytest
from flask import url_for

from server import app, load_clubs


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


def test_book_route(client):
    with app.app_context():
        response = client.get(
            url_for(
                "book",
                competition="Spring Festival",
                club="Simply Lift"
            )
        )

    assert response.status_code == 200


def test_purchase_places_route(client):
    with app.app_context():
        response = client.post(
            url_for("purchase_places"),
            data={
                "competition": "Spring Festival",
                "club": "Iron Temple",
                "places": 2
            }
        )

        assert response.status_code == 200
        assert b"Great-booking complete!" in response.data


def test_purchase_too_much_places_for_club(client):
    with app.app_context():
        response = client.post(
            url_for("purchase_places"),
            data={
                "competition": "Spring Festival",
                "club": "Iron Temple",
                "places": 5
            },
            follow_redirects=True
        )

        assert response.status_code == 200
        assert b"Your club does not have enough points" in response.data


def test_purchase_too_much_places_for_event(client):
    with app.app_context():
        response = client.post(
            url_for("purchase_places"),
            data={
                "competition": "Test Tournament",
                "club": "She Lifts",
                "places": 4
            },
            follow_redirects=True
        )

        assert response.status_code == 200
        assert b"Not enough places available" in response.data


def test_book_more_than_12_places(client):
    with app.app_context():
        response = client.post(
            url_for("purchase_places"),
            data={
                "competition": "Spring Festival",
                "club": "Simply Lift",
                "places": 13
            },
            follow_redirects=True
        )

        assert response.status_code == 200
        assert b"You can not book more than 12 places" in response.data


def test_book_past_event(client):
    with app.app_context():
        response = client.get(
            url_for('book',
                    competition='Fall Classic',
                    club="Simply Lift"
                    )
        )
    assert response.status_code == 200
    assert b'This competition is past' in response.data


def test_display_points_board(client):

    clubs = load_clubs()

    with app.app_context():
        response = client.get(url_for("display_club_points"))

        assert response.status_code == 200
        for club in clubs:
            assert club["name"] in str(response.data)
