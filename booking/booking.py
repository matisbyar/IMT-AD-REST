import json

import requests
from flask import Flask, jsonify, make_response, request

app = Flask(__name__)

PORT = 3201
HOST = '0.0.0.0'

with open('{}/databases/bookings.json'.format("."), "r") as jsf:
    bookings = json.load(jsf)["bookings"]


def write(bookings):
    data = {"bookings": bookings}
    with open('{}/databases/bookings.json'.format("."), 'w') as f:
        json.dump(data, f)


@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"


@app.route("/bookings", methods=['GET'])
def get_json():
    res = make_response(jsonify(bookings), 200)
    return res


@app.route("/bookings/<userid>", methods=['GET'])
def get_bookings_byuserid(userid):
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
    req = request.get_json()
    date = req['date']
    movie_id = req['movieid']

    url = f"http://{request.remote_addr}:3202/showmovies/{date}"

    # get the showtimes information
    showtimes = requests.get(url)

    # check if the date exists
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

                #print({"bookings": bookings})
                write(bookings)
                return make_response(jsonify({"ok": "Booking created"}), 200)

        return make_response(jsonify({"error": "An item already exists"}), 409)
    else:
        return make_response(jsonify({"error": "Couldn't add booking for the user"}), 400)


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
