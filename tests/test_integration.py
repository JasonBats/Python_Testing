import pytest
from flask import url_for

from server import app, load_clubs


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_login_to_book_route(client):
    """
    Login as john@simplylift.co, choose “Spring Festival” event,
    books 5 places, checks booking confirmation and number_of_places update.
    Checks newly implemented view with consistent information.
    """
    with app.app_context():
        # Login
        data = {"email": "john@simplylift.co"}
        response = client.post(url_for("show_summary"), data=data)
        assert response.status_code == 200
        assert "Welcome" in str(response.data)

        # Book competition places
        competition = "Spring Festival"
        club = "Simply Lift"
        number_of_places = 5
        club_points = load_clubs()[0]['points']

        response = client.get(
            url_for(
                "book",
                competition=competition,
                club=club
            )
        )
        assert response.status_code == 200

        response = client.post(
            url_for("purchase_places"),
            data={
                "competition": competition,
                "club": club,
                "places": number_of_places
            }
        )

        assert response.status_code == 200
        assert "Great" in str(response.data)
        assert f"Points available: {
            str(int(club_points) - int(number_of_places))
        }" in str(response.data)

        # Display club points in newly implemented view
        response = client.get(url_for("display_club_points"))
        assert response.status_code == 200
        assert f"Club : Simply Lift | Points : {
            str(int(club_points) - int(number_of_places))
        }" in str(response.data)


def test_book_route(client):
    with app.app_context():
        response = client.post(
            url_for("purchase_places"),
            data={
                "competition": "Spring Festival",
                "club": "She Lifts",
                "places": 5
            }
        )
        assert response.status_code == 200
        assert b"Great-booking complete!" in response.data
        assert b"Welcome, kate@shelifts.co.uk" in response.data
        assert b"Points available: 7" in response.data
