import json

from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

PORT = 3200
HOST = '0.0.0.0'

# Load movies data from JSON file
with open('{}/databases/movies.json'.format("."), 'r') as jsf:
    movies = json.load(jsf)["movies"]


def write(movies):
    """
    Write the movies data to the JSON file.

    Args:
        movies (list): List of movie dictionaries.
    """
    data = {"movies": movies}
    with open('{}/databases/movies.json'.format("."), 'w') as f:
        json.dump(data, f, indent=4)


@app.route("/", methods=['GET'])
def home():
    """
    Home route that returns a welcome message.

    Returns:
        Response: HTML response with a welcome message.
    """
    return make_response("<h1 style='color:blue'>Welcome to the Movie service!</h1>", 200)


@app.route("/json", methods=['GET'])
def get_json():
    """
    Route to get all movies.

    Returns:
        Response: JSON response containing all movies.
    """
    res = make_response(jsonify(movies), 200)
    return res


@app.route("/movies/<movieid>", methods=['GET'])
def get_movie_byid(movieid):
    """
    Route to get a movie by its ID.

    Args:
        movieid (str): ID of the movie to retrieve.

    Returns:
        Response: JSON response containing the movie data or an error message.
    """
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            res = make_response(jsonify(movie), 200)
            return res
    return make_response(jsonify({"error": "Movie ID not found"}), 400)


@app.route("/moviesbytitle", methods=['GET'])
def get_movie_bytitle():
    """
    Route to get a movie by its title.

    Returns:
        Response: JSON response containing the movie data or an error message.
    """
    json = ""
    if request.args:
        req = request.args
        for movie in movies:
            if str(movie["title"]) == str(req["title"]):
                json = movie

    if not json:
        res = make_response(jsonify({"error": "movie title not found"}), 400)
    else:
        res = make_response(jsonify(json), 200)
    return res


@app.route("/movie/<movieid>", methods=['POST'])
def add_movie(movieid):
    """
    Route to add a new movie.

    Args:
        movieid (str): ID of the new movie.

    Returns:
        Response: JSON response indicating success or failure of the movie addition.
    """
    req = request.get_json()

    for movie in movies:
        if str(movie["id"]) == str(movieid):
            return make_response(jsonify({"error": "movie ID already exists"}), 409)

    movies.append(req)
    write(movies)
    res = make_response(jsonify({"message": "movie added"}), 200)
    return res


@app.route("/movies/<movieid>/<rate>", methods=['PUT'])
def update_movie_rating(movieid, rate):
    """
    Route to update the rating of a movie.

    Args:
        movieid (str): ID of the movie to update.
        rate (str): New rating of the movie.

    Returns:
        Response: JSON response containing the updated movie data or an error message.
    """
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movie["rating"] = rate
            res = make_response(jsonify(movie), 200)
            return res

    res = make_response(jsonify({"error": "movie ID not found"}), 201)
    return res


@app.route("/movies/<movieid>", methods=['DELETE'])
def del_movie(movieid):
    """
    Route to delete a movie by its ID.

    Args:
        movieid (str): ID of the movie to delete.

    Returns:
        Response: JSON response containing the deleted movie data or an error message.
    """
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movies.remove(movie)
            return make_response(jsonify(movie), 200)

    res = make_response(jsonify({"error": "movie ID not found"}), 400)
    return res


@app.route("/help", methods=['GET'])
def get_help_movies():
    """
    Route to get help information about the available endpoints.

    Returns:
        Response: JSON response containing help information.
    """
    help = [
        {"path_and_method": "GET /json", "description": "Get all movies"},
        {"path_and_method": "GET /movies/<movieid>", "description": "Get movie by ID"},
        {"path_and_method": "GET /moviesbytitle?title=<title>", "description": "Get movie by title"},
        {"path_and_method": "POST /movie/<movieid>", "description": "Add movie by ID"},
        {"path_and_method": "PUT /movies/<movieid>/<rate>", "description": "Update movie rating by ID"},
        {"path_and_method": "DELETE /movies/<movieid>", "description": "Delete movie by ID"},
        {"path_and_method": "GET /help", "description": "Get help"}
    ]
    return make_response(jsonify(help), 200)


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
