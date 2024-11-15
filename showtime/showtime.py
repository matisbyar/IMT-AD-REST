import json

from flask import Flask, jsonify, make_response

app = Flask(__name__)

PORT = 3202
HOST = '0.0.0.0'

# Load schedules data from JSON file
with open('{}/databases/times.json'.format("."), "r") as jsf:
    schedules = json.load(jsf)["schedule"]


@app.route("/", methods=['GET'])
def home():
    """
    Home route that returns a welcome message.

    Returns:
        Response: HTML response with a welcome message.
    """
    return make_response("<h1 style='color:blue'>Welcome to the Showtime service!</h1>", 200)


@app.route("/showtimes", methods=['GET'])
def get_schedule():
    """
    Route to get all showtimes.

    Returns:
        Response: JSON response containing all showtimes.
    """
    return make_response(jsonify(schedules), 200)


@app.route("/showmovies/<date>", methods=['GET'])
def get_movie_bydate(date):
    """
    Route to get movies by date.

    Args:
        date (str): Date to filter showtimes.

    Returns:
        Response: JSON response containing showtimes for the specified date or an error message.
    """
    for schedule in schedules:
        if str(schedule["date"]) == str(date):
            res = make_response(jsonify(schedule), 200)
            return res
    return make_response(jsonify({"error": "bad input parameter"}), 400)


if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
