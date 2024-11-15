import json

import requests
from flask import Flask, jsonify, make_response, request

app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'

# Load users data from JSON file
with open('{}/databases/users.json'.format("."), "r") as jsf:
    users = json.load(jsf)["users"]


def write(bookings):
    """
    Write the users data to the JSON file.

    Args:
        bookings (list): List of user dictionaries.
    """
    data = {"users": bookings}
    with open('{}/databases/users.json'.format("."), 'w') as f:
        json.dump(data, f)


@app.route("/", methods=['GET'])
def home():
    """
    Home route that returns a welcome message.

    Returns:
        str: HTML string with a welcome message.
    """
    return "<h1 style='color:blue'>Welcome to the User service!</h1>"


@app.route("/users", methods=['GET'])
def get_json():
    """
    Route to get all users.

    Returns:
        Response: JSON response containing all users.
    """
    res = make_response(jsonify(users), 200)
    return res


@app.route("/user/<userId>", methods=['GET'])
def get_user_by_id(userId):
    """
    Route to get a user by their ID.

    Args:
        userId (str): ID of the user to retrieve.

    Returns:
        Response: JSON response containing the user data or an error message.
    """
    for user in users:
        if str(user["id"]) == str(userId):
            res = make_response(jsonify(user), 200)
            return res
    return make_response(jsonify({"error": "No user with this ID"}), 400)


@app.route("/users/<userId>", methods=['POST'])
def add_user(userId):
    """
    Route to add a new user.

    Args:
        userId (str): ID of the new user.

    Returns:
        Response: JSON response indicating success or failure of the user addition.
    """
    req = request.get_json()

    for user in users:
        if str(user["id"]) == str(userId):
            return make_response(jsonify({"error": "user ID already exists"}), 409)

    users.append(req)
    write(users)

    return make_response(jsonify({"message": "user added"}), 200)


@app.route("/user/<userId>", methods=['DELETE'])
def del_user(userId):
    """
    Route to delete a user by their ID.

    Args:
        userId (str): ID of the user to delete.

    Returns:
        Response: JSON response containing the deleted user data or an error message.
    """
    for user in users:
        if str(user["id"]) == str(userId):
            users.remove(user)
            write(users)

            return make_response(jsonify(user), 200)

    return make_response(jsonify({"error": "user not found"}), 400)


@app.route("/user/<userId>", methods=['PUT'])
def update_user_lastactive(userId):
    """
    Route to update the last active timestamp of a user.

    Args:
        userId (str): ID of the user to update.

    Returns:
        Response: JSON response containing the updated user data or an error message.
    """
    last_active = request.args.get('last_active')

    for user in users:
        if str(user["id"]) == str(userId):
            user["last_active"] = last_active
            write(users)

            res = make_response(jsonify(user), 200)
            return res

    res = make_response(jsonify({"error": "user not found"}), 201)
    return res


@app.route("/user/<userId>/bookings/movies", methods=['GET'])
def get_movies_from_usersbooking(userId):
    """
    Route to get movies from a user's bookings.

    Args:
        userId (str): ID of the user to retrieve bookings for.

    Returns:
        Response: JSON response containing the movies data or an error message.
    """
    bookings_url = f"http://{request.remote_addr}:3201/bookings/{userId}"
    bookings = requests.get(bookings_url)

    if bookings.status_code != 200:
        return make_response(jsonify({"error": "User has no bookings"}), 409)

    bookings_list = bookings.json()
    movies = [movie for booking in bookings_list["dates"] for movie in booking["movies"]]

    if not movies:
        return make_response(jsonify({"error": "User has no bookings"}), 409)

    movies_detailed = []
    for movie in movies:
        movie_url = f"http://{request.remote_addr}:3200/movies/{movie}"
        movie_fetched = requests.get(movie_url)

        if movie_fetched.status_code == 200:
            print(movie_fetched.json())
            movies_detailed.append(movie_fetched.json())
        else:
            return make_response(jsonify({"error": "An error occurred while fetching a movie"}), 409)

    return make_response(jsonify({"movies": movies_detailed}), 200)


@app.route("/help", methods=['GET'])
def get_help_users():
    """
    Route to get help information about the available endpoints.

    Returns:
        Response: JSON response containing help information.
    """
    help = [
        {"path_and_method": "GET /users", "description": "Get all users"},
        {"path_and_method": "GET /user/<userId>", "description": "Get user by ID"},
        {"path_and_method": "GET /user/<userId>/bookings/movies",
         "description": "Retrieve all user's bookings by their ID"},
        {"path_and_method": "PUT /user/<userId>", "description": "Update user last_active timestamp by their ID"},
        {"path_and_method": "DELETE /user/<userId>", "description": "Delete user by ID"},
        {"path_and_method": "GET /help", "description": "Get help"}
    ]
    return make_response(jsonify(help), 200)


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
