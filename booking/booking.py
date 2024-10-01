import json

from flask import Flask, jsonify, make_response, request

app = Flask(__name__)

PORT = 3201
HOST = '0.0.0.0'

with open('{}/databases/bookings.json'.format("."), "r") as jsf:
    bookings = json.load(jsf)["bookings"]


def write(bookings):
    data = {"bookings": bookings}
    with open('{}/databases/bookings.json'.format("."), 'w') as f:
        json.dump(data, f, ident=4)


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
def add_booking(userid):
    req = request.get_json()

    date = req["date"]
    movieid = req["movieid"]

    # todo: check with the showtimes service if the booking is valid
    return make_response(jsonify({"message": "Booking added"}), 200)


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
