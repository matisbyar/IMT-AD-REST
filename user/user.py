import json

import requests
from flask import Flask, jsonify, make_response, request

app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'

with open('{}/databases/users.json'.format("."), "r") as jsf:
    users = json.load(jsf)["users"]


@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the User service!</h1>"


@app.route("/users", methods=['GET'])
def get_json():
    res = make_response(jsonify(users), 200)
    return res


@app.route("/user/<userId>", methods=['GET'])
def get_user_by_id(userId):
    for user in users:
        if str(user["id"]) == str(userId):
            res = make_response(jsonify(user), 200)
            return res
    return make_response(jsonify({"error": "No user with this ID"}), 400)


@app.route("/user/<userId>/bookings/movies", methods=['GET'])
def get_movies_from_usersbooking(userId):
    bookings_url = f"http://{request.remote_addr}:3201/bookings/{userId}"
    bookings = requests.get(bookings_url)

    if bookings.status_code == 200:
        bookings_list = bookings.json()

        print(bookings_list)

        movies = []
        for booking in bookings_list["dates"]:
            print(booking["movies"])
            for movie in booking["movies"]:
                movies.append(movie)

        if len(movies) == 0:
            return make_response(jsonify({"error": "User has no bookings"}), 409)

        movies_detailed = []
        for movie in movies:
            print(movie)

            movie_url =  f"http://{request.remote_addr}:3200/movie/{movie}"
            movie_fetched = requests.get(movie_url)

            if movie_fetched.status_code == 200:
                movies_detailed.append(movie_fetched.json()["movie"])
                #todo: fix
                print(movie_fetched.json()["movie"])
            else:
                return make_response(jsonify({"error": "An error occurred while fetching a movie"}), 409)

    else:
        return make_response(jsonify({"error": "User has no bookings"}), 409)


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
