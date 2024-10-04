from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound


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

@app.route("/user/<userId>", methods = ['GET'])
def get_user_by_id(userId):
   for user in users:
      if str(user["id"]) == str(userId):
         res = make_response(jsonify(user), 200)
         return res
   return make_response(jsonify({"error": "No user with this ID"}), 400)


if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
