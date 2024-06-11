import pytest


@pytest.fixture
def load_competitions_mock(mocker):
    load_competitions = mocker.patch("server.load_competitions")
    load_competitions.return_value = [
        {
            "name": "Spring Festival",
            "date": "2025-03-27 10:00:00",
            "number_of_places": "25"
        },
        {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "number_of_places": "13"
        },
        {
            "name": "Fall Classic 2",
            "date": "2020-10-22 13:30:00",
            "number_of_places": "13"
        },
        {
            "name": "Test Tournament",
            "date": "2025-10-22 13:30:00",
            "number_of_places": "2"
        }
    ]


@pytest.fixture
def load_clubs_mock(mocker):
    load_clubs = mocker.patch("server.load_clubs")
    load_clubs.return_value = [
        {
            "name": "Simply Lift",
            "email": "john@simplylift.co",
            "points": "13",
            "bookings": []
        },
        {
            "name": "Iron Temple",
            "email": "admin@irontemple.com",
            "points": "4",
            "bookings": []
        },
        {
            "name": "She Lifts",
            "email": "kate@shelifts.co.uk",
            "points": "12",
            "bookings": []
        }
    ]
