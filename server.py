import json

from flask import Flask, flash, redirect, render_template, request, url_for


def load_clubs():
    with open("clubs.json") as c:
        list_of_clubs = json.load(c)["clubs"]
        return list_of_clubs


def load_competitions():
    with open("competitions.json") as comps:
        list_of_competitions = json.load(comps)["competitions"]
        return list_of_competitions


app = Flask(__name__)
app.secret_key = "something_special"

app.config['SERVER_NAME'] = '127.0.0.1:5000'
app.config['APPLICATION_ROOT'] = '/'
app.config['PREFERED_URL_SCHEME'] = 'http'

competitions = load_competitions()
clubs = load_clubs()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/show_summary", methods=["POST"])
def show_summary():
    try:
        club = [club for club in clubs if
                club['email'] == request.form['email']][0]
        return render_template(
            'welcome.html',
            club=club, competitions=competitions
        )
    except IndexError:
        flash('Email not found', 'error')
        return redirect(url_for('index'))


@app.route("/book/<competition>/<club>")
def book(competition, club):
    found_club = [c for c in clubs if c["name"] == club][0]
    found_competition = [c for c in competitions if
                         c["name"] == competition][0]
    if found_club and found_competition:
        return render_template(
            "booking.html",
            club=found_club,
            competition=found_competition
        )
    else:
        flash("Something went wrong-please try again")
        return render_template(
            "welcome.html",
            club=club,
            competitions=competitions
        )


@app.route("/purchase_places", methods=["POST"])
def purchase_places():
    competition = [c for c in competitions if
                   c["name"] == request.form["competition"]][0]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    places_required = int(request.form["places"])
    competition["number_of_places"] = (
        int(competition["number_of_places"]) - places_required
    )
    flash("Great-booking complete!")
    return render_template(
        "welcome.html",
        club=club,
        competitions=competitions
    )


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
