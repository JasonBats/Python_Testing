def check_bookings(competition, club):
    competition_name = competition['name']

    places_already_booked = 0
    for booking in club['bookings']:
        if competition_name in booking:
            places_already_booked = booking[competition_name]
        else:
            placess_already_booked = 0
    return places_already_booked


def update_bookings(competition, club, places_required):

    competition_name = competition['name']
    booking = {competition_name: places_required}

    if not club['bookings']:
        club['bookings'].append(booking)
    for booking in club['bookings']:
        if competition_name in booking:
            booking[competition_name] += places_required
