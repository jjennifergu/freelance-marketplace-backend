import json
import users_dao
import datetime
from unicodedata import category
from urllib import request

from flask import Flask
from flask import request

from db import db, Listing, User

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

def extract_token(request):
    """
    Helper function that extracts the token from the header of a request
    """
    auth_header = request.headers.get("Authorization")
    
    if auth_header is None:
        return False, json.dumps({"Missing authorization header"})

    bearer_token = auth_header.replace("Bearer", "").strip()

    return True, bearer_token


@app.route("/")
def hello_world():
    return json.dumps("Hai :3")

#homepage
@app.route("/listings/", methods=["GET"])
def get_all_listings():
    """
    Endpoint for getting all listings
    """        
    return success_response(
        {"listings": [l.serialize() for l in Listing.query.all()]}
    )

#listing details
@app.route("/listings/<int:listing_id>/", methods=["GET"])
def get_listing(listing_id):
    """
    Endpoint for getting a listing by id
    """
    listing = Listing.query.filter_by(id=listing_id).first()
    if listing is None:
        return failure_response("Listing not found!")
    return success_response(listing.serialize())

#create listing, should have associated seller id & populate association table
@app.route("/listings/<int:seller_id>/", methods=["POST"])
def create_listing(seller_id):
    """
    Endpoint for creating a listing
    """
    was_successful, session_token = extract_token(request)

    if not was_successful:
        return session_token

    clown = users_dao.get_user_by_session_token (session_token)
    if not clown or not clown.verify_session_token(session_token):
        return failure_response("Invalid session token")

    body = json.loads(request.data)
    try:
        new_listing = Listing(
            title = body.get("title"),
            category = body.get("category"),
            description = body.get("description"),
            availability = body.get("availability"),
            location = body.get("location"),
            price = body.get("price"),
            picture = body.get("picture"),
            seller_id = seller_id,
        )
        db.session.add(new_listing)
        db.session.commit()
        return success_response(new_listing.serialize(), 201)
    except Exception as e:
        return failure_response(f"Invalid fields, {e}", 400)
    

#delete listing, need to implement authentication
@app.route("/listings/<int:listing_id>/", methods=["DELETE"])
def delete_listing(listing_id):
    """
    Endpoint for deleting a listing by id
    """
    was_successful, session_token = extract_token(request)

    if not was_successful:
        return session_token

    clown = users_dao.get_user_by_session_token (session_token)
    if not clown or not clown.verify_session_token(session_token):
        return failure_response("Invalid session token")

    listing = Listing.query.filter_by(id=listing_id).first()
    if listing is None:
        return failure_response("Listing not found!")
    db.session.delete(listing)
    db.session.commit()
    return success_response(listing.serialize())


@app.route("/listings/<int:listing_id>/", methods=["POST"])
def edit_listing(listing_id):
    """
    Endpoint for updating a listing by id
    """
    was_successful, session_token = extract_token(request)

    if not was_successful:
        return session_token

    clown = users_dao.get_user_by_session_token (session_token)
    if not clown or not clown.verify_session_token(session_token):
        return failure_response("Invalid session token")

    listing = Listing.query.filter_by(id=listing_id).first()
    if listing is None:
        return failure_response("Listing not found!")
    # process request body if listing is found
    body = json.loads(request.data)
    
    listing.title = body.get("title")
    listing.category = body.get("category"),
    listing.description = body.get("description"),
    listing.availability = body.get("availability"),
    listing.location = body.get("location"),
    listing.price = body.get("price"),
    listing.picture = body.get("picture")
    db.session.commit()
    return success_response(listing.serialize())


#used for testing
@app.route("/users/")
def get_all_users():
    """
    Endpoint for getting all users
    """
    was_successful, update_token = extract_token(request)

    if not was_successful:
        return update_token

    try:
        user = users_dao.renew_session(update_token)
    except Exception as e:
        return failure_response(f"Invalid update token: {str(e)}")
        
    return success_response(
        {"users": [u.serialize() for u in User.query.all()]}
    )

#sign up, register new user
@app.route("/users/", methods=["POST"])
def create_user():
    """
    Endpoint for creating a user
    """
    body = json.loads(request.data)
    username = body.get("username")
    password = body.get("password")
    name = body.get("name")
    bio = body.get("bio")
    contact = body.get("contact")
    
    if username is None or password is None: 
        return failure_response("Missing username or password")

    try:
        was_successful, user = users_dao.create_user(username, password, contact)

        if not was_successful:
            return failure_response("User already exists")
        # return success_response(new_course.serialize(), 201)
    except Exception as e:
        return failure_response(f"Invalid fields, {e}", 400)

    

    return success_response(
        {
            "session_token": user.session_token,
            "session_expiration": str(user.session_expiration),
            "update_token": user.update_token
        }, 201
    )

#view profile with authentication
@app.route("/users/<int:user_id>/", methods=["GET"])
def get_user(user_id):
    """
    Endpoint for getting a user by id
    """
    was_successful, session_token = extract_token(request)

    if not was_successful:
        return session_token

    user = users_dao.get_user_by_session_token(session_token) 
    if not user or not user.verify_session_token(session_token):
        return failure_response("Invalid session token")

    return success_response(user.serialize())


@app.route("/users/<int:user_id>/", methods=["POST"])    
def edit_user(user_id):
    """
    Endpoint for updating a listing by id
    """
    was_successful, session_token = extract_token(request)

    if not was_successful:
        return session_token

    clown = users_dao.get_user_by_session_token (session_token)
    if not clown or not clown.verify_session_token(session_token):
        return failure_response("Invalid session token")

    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found!")
    # process request body if listing is found
    body = json.loads(request.data)
    
    user.name = body.get("name")
    user.bio = body.get("bio")
    user.contact = body.get("contact")
    db.session.commit()
    return success_response(user.serialize())

#log in route
@app.route("/login/", methods=["POST"])
def login():
    """
    Endpoint for logging in a user
    """
    body = json.loads(request.data)
    username = body.get("username")
    password = body.get("password")

    if username is None or password is None:
        return failure_response("Missing username or password", 400)

    was_successful, user = users_dao.verify_credentials(username,password)

    if not was_successful:
        return failure_response("Incorrect username or password", 401)

    return success_response(
        {
            "session_token": user.session_token,
            "session_expiration": str(user.session_expiration),
            "update_token": user.update_token

        }
    )

#purchase listing, give user id in body?
@app.route("/listings/<int:listing_id>/<int:user_id>/purchase/", methods=["POST"])
def purchase_listing(listing_id, user_id):
    """
    Endpoint for purchasing a listing by listing id
    """
    was_successful, session_token = extract_token(request)

    if not was_successful:
        return session_token

    clown = users_dao.get_user_by_session_token (session_token)
    if not clown or not clown.verify_session_token(session_token):
        return failure_response("Invalid session token")

    #############
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found!")
    # process request body if course is found
    body = json.loads(request.data)
    listing_id = body.get("listing_id")
    # user_type = body.get("type")
    # assign user to course
    listing = Listing.query.filter_by(id=listing_id).first()
    if listing is None:
        return failure_response("User not found!")
    user.buyer_listings.append(listing)
    db.session.commit()
    return success_response(user.serialize())



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)