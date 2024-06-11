import json
from datetime import datetime

from flask import Flask, flash, redirect, render_template, request, url_for

from utils import check_bookings, update_bookings

app = Flask(__name__)
app.secret_key = "something_special"

app.config["SERVER_NAME"] = "127.0.0.1:5000"
app.config["APPLICATION_ROOT"] = "/"
app.config["PREFERED_URL_SCHEME"] = "http"
app.config["TESTING"] = True


def load_clubs():
    with open("clubs.json") as c:
        list_of_clubs = json.load(c)["clubs"]
        return list_of_clubs


def load_competitions():
    with open("competitions.json") as comps:
        list_of_competitions = json.load(comps)["competitions"]
        return list_of_competitions


competitions = load_competitions()
clubs = load_clubs()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/show_summary", methods=["POST"])
def show_summary():
    try:
        club = [club for club in clubs if club["email"] == request.form["email"]][0]
        return render_template("welcome.html", club=club, competitions=competitions)
    except IndexError:
        flash("Email not found", "error")
        return redirect(url_for("index"))


@app.route("/book/<competition>/<club>")
def book(competition, club):
    found_club = [c for c in clubs if c["name"] == club][0]
    found_competition = [c for c in competitions if c["name"] == competition][0]

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    competition_date = found_competition["date"]
    is_past = now > competition_date

    if found_club and found_competition and not is_past:
        return render_template(
            "booking.html", club=found_club, competition=found_competition
        )
    elif is_past:
        flash("This competition is past", "error")
        return render_template(
            "welcome.html", club=found_club, competitions=competitions
        )


@app.route("/purchase_places", methods=["POST"])
def purchase_places():
    competition = [c for c in competitions if c["name"] == request.form["competition"]][
        0
    ]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    competition_places_available = int(competition["number_of_places"])
    club_points = int(club["points"])
    places_required = int(request.form["places"])

    if competition_places_available >= places_required <= club_points:
        places_already_booked = check_bookings(competition, club)

        total_booked_places = places_required + places_already_booked

        if total_booked_places <= 12:

            competition["number_of_places"] = (
                int(competition["number_of_places"]) - places_required
            )
            club["points"] = int(club["points"]) - places_required

            update_bookings(competition, club, places_required)
            flash("Great-booking complete!")
            return render_template("welcome.html", club=club, competitions=competitions)
        else:
            flash("You can not book more than 12 places")
            return redirect(
                url_for("book", club=club["name"], competition=competition["name"])
            )

    elif places_required > club_points:
        flash("Your club does not have enough points")
        return redirect(
            url_for("book", club=club["name"], competition=competition["name"])
        )

    elif places_required > competition_places_available:
        flash("Not enough places available")
        return redirect(
            url_for("book", club=club["name"], competition=competition["name"])
        )


@app.route("/display_club_points", methods=["GET"])
def display_club_points():
    return render_template("display_points.html", clubs=clubs)


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
