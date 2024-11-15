import json

import requests
from flask import Flask, jsonify, make_response, request

app = Flask(__name__)

PORT = 3201
HOST = '0.0.0.0'

# Load bookings data from JSON file
with open('{}/databases/bookings.json'.format("."), "r") as jsf:
    bookings = json.load(jsf)["bookings"]


def write(bookings):
    """
    Write the bookings data to the JSON file.

    Args:
        bookings (list): List of booking dictionaries.
    """
    data = {"bookings": bookings}
    with open('{}/databases/bookings.json'.format("."), 'w') as f:
        json.dump(data, f)


@app.route("/", methods=['GET'])
def home():
    """
    Home route that returns a welcome message.

    Returns:
        str: HTML string with a welcome message.
    """
    return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"


@app.route("/bookings", methods=['GET'])
def get_json():
    """
    Route to get all bookings.

    Returns:
        Response: JSON response containing all bookings.
    """
    res = make_response(jsonify(bookings), 200)
    return res


@app.route("/bookings/<userid>", methods=['GET'])
def get_bookings_byuserid(userid):
    """
    Route to get bookings by user ID.

    Args:
        userid (str): User ID to filter bookings.

    Returns:
        Response: JSON response containing bookings for the specified user ID or an error message.
    """
    json = ""
    for booking in bookings:
        if str(booking["userid"]) == str(userid):
            json = booking

    if not json:
        res = make_response(jsonify({"error": "User ID not found"}), 400)
    else:
        res = make_response(jsonify(json), 200)
    return res


@app.route("/bookings/<userid>", methods=['POST'])
def add_booking_byuser(userid):
    """
    Route to add a booking for a user.

    Args:
        userid (str): User ID to add the booking for.

    Returns:
        Response: JSON response indicating success or failure of the booking creation.
    """
    req = request.get_json()
    date = req['date']
    movie_id = req['movieid']

    url = f"http://{request.remote_addr}:3202/showmovies/{date}"

    showtimes = requests.get(url)

    if showtimes.status_code == 200:
        showtime_movies = showtimes.json()
        movies = showtime_movies['movies']
        for movie in movies:
            if movie_id == movie:
                user_entry = next((entry for entry in bookings if entry["userid"] == userid), None)
                if user_entry is None:
                    return make_response(jsonify({"error": "User ID not found"}), 400)
                else:
                    date_entry = next((entry for entry in user_entry["dates"] if entry["date"] == date), None)
                    if date_entry is None:
                        date_entry = {"date": date, "movies": [movie_id]}
                        user_entry["dates"].append(date_entry)
                    else:
                        date_entry["movies"].append(movie_id)

                write(bookings)
                return make_response(jsonify({"success": "Booking created"}), 200)

        return make_response(jsonify({"error": "An item already exists"}), 409)
    else:
        return make_response(jsonify({"error": "Couldn't add booking for the user"}), 400)


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
