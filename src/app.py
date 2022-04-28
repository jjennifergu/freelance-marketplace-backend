import json
from unicodedata import category
from urllib import request

from flask import Flask
from flask import request

from db import db
from db import Listing
from db import User

app = Flask(__name__)
db_filename = "todo.db"

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_filename}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False

db.init_app(app)
with app.app_context():
    db.create_all()


# generalized response formats
def success_response(data, code=200):
    return json.dumps(data), code

def failure_response(message, code=404):
    return json.dumps({"error": message}), code


@app.route("/")
def hello_world():
    return json.dumps("Hai :3")

#homepage
@app.route("/listings/")
def get_all_listings():
    """
    Endpoint for getting all listings
    """
    pass

#listing details
@app.route("/listings/<int:listing_id>/")
def get_listing(listing_id):
    """
    Endpoint for getting a listing by id
    """
    pass

#create listing, should have associated seller id & populate association table
@app.route("/listings/", methods=["POST"])
def create_listing():
    """
    Endpoint for creating a listing
    """
    pass

#delete listing, need to implement authentication
@app.route("/listings/<int:listing_id>/", methods=["DELETE"])
def delete_listing():
    """
    Endpoint for deleting a listing by id
    """
    pass

#used for testing
@app.route("/users/")
def get_all_users():
    """
    Endpoint for getting all users
    """
    pass

#sign up
@app.route("/users/", methods=["POST"])
def create_user():
    """
    Endpoint for creating a user
    """
    pass

#view profile
@app.route("/users/<int:user_id>/")
def get_user():
    """
    Endpoint for getting a user by id
    """
    pass

#need to add log in route, idk how to do it :P

#purchase listing, give user id in body?
@app.route("/listings/<int:listing_id>/purchase/", methods=["POST"])
def purchase_listing(listing_id):
    """
    Endpoint for purchasing a listing by listing id
    """
    pass

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)