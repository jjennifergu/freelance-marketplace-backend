from enum import auto
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import datetime
import hashlib
import os

import bcrypt

db = SQLAlchemy()

buyer_association_table = db.Table(
    "buyer_association",
    db.Model.metadata,
    db.Column("listing_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("listings.id"))
)

class Listing(db.Model):
    """
    Listing model

    Has a one-to-many relationship with sellers
    Has a many-to-many relationship with buyers
    """
    __tablename__="listings"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #frontend gives unixTime, backend returns date and time
    unixTime = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String, nullable=False)
    category=db.Column(db.String, nullable=False)
    description=db.Column(db.String, nullable=False)
    availability=db.Column(db.String, nullable=False)
    location=db.Column(db.String, nullable=False)
    price=db.Column(db.Integer, nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    buyers=db.relationship("User", secondary=buyer_association_table, back_populates="buyer_listings")

    def __init__(self, **kwargs):
        """
        initialize Listing object
        """
        self.unixTime = kwargs.get("unixTime")
        self.title = kwargs.get("title")
        self.description = kwargs.get("description")
        self.availability = kwargs.get("availability")
        self.location = kwargs.get("location")
        self.price = kwargs.get("price")

    def serialize(self):        
        """
        serialize a Listing object
        """
        seller = User.query.filter_by(id=self.seller_id).first()
        return {      
            "id": self.id,      
            "date": datetime.fromtimestamp(self.unixTime).strftime("%m/%d/%Y"),            
            "time": datetime.fromtimestamp(self.unixTime).strftime("%H:%M"),
            "title": self.title,
            "category": self.category,            
            "description": self.description,
            "availability": self.availability,
            "location": self.location,
            "price": self.price,
            "seller": seller.simple_serialize(),  
            "buyers": [b.simple_serialize() for b in self.buyers]
        }

    def simple_serialize(self):
        """
        Simple serializes a Listing object
        """
        return {
            "id": self.id,      
            "date": datetime.fromtimestamp(self.unixTime).strftime("%m/%d/%Y"),            
            "time": datetime.fromtimestamp(self.unixTime).strftime("%H:%M"),
            "title": self.title,
            "category": self.category,            
            "description": self.description,
            "availability": self.availability,
            "location": self.location,
            "price": self.price
        }
    

class User(db.Model):
    """
    User model
    Sellers have a one-to-many relationship with Listings
    Buyers have a many-to-many relationship with Listings
    contact, username, password_digest, session_token, session_expiration, update_token
    """
    __tablename__="users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contact = db.Column(db.String, nullable=False)
    seller_listings=db.relationship("Listing", cascade="delete")
    buyer_listings = db.relationship("Listing", secondary=buyer_association_table, back_populates="buyers")

    # User information
    username = db.Column(db.String, nullable=False, unique=True)
    password_digest = db.Column(db.String, nullable=False)

    # Session information
    session_token = db.Column(db.String, nullable=False, unique=True)
    session_expiration = db.Column(db.DateTime, nullable=False)
    update_token = db.Column(db.String, nullable=False, unique=True)

    def __init__(self, **kwargs):
        """
        initializes User object
        """
        self.contact = kwargs.get("contact")
        self.username = kwargs.get("username", "")
        self.password_digest = bcrypt.hashpw(kwargs.get("password").encode("utf8"), bcrypt.gensalt(rounds=13))
        self.renew_session()
    
    def serialize(self):        
        """
        serialize a User object
        """
        return {      
            "id": self.id,      
            "username": self.username,
            "contact": self.contact,
            "seller_listings": [s.simple_serialize() for s in self.seller_listings],
            "buyers_listings": [b.simple_serialize() for b in self.buyer_listings]
        }

    def simple_serialize(self):
        """
        Simple serializes a User object
        """
        return {
            "id": self.id,      
            "username": self.username,
            "contact": self.contact
        }

    #authentication methods
    def _urlsafe_base_64(self):
        """
        Randomly generates hashed tokens (used for session/update tokens)
        """
        return hashlib.sha1(os.urandom(64)).hexdigest()

    def renew_session(self):
        """
        Renews the sessions, i.e.
        1. Creates a new session token
        2. Sets the expiration time of the session to be a day from now
        3. Creates a new update token
        """
        self.session_token = self._urlsafe_base_64()
        self.session_expiration = datetime.datetime.now() + datetime.timedelta(days=1)
        self.update_token = self._urlsafe_base_64()

    def verify_password(self, password):
        """
        Verifies the password of a user
        """
        return bcrypt.checkpw(password.encode("utf8"), self.password_digest)

    def verify_session_token(self, session_token):
        """
        Verifies the session token of a user
        """
        return session_token == self.session_token and datetime.datetime.now() < self.session_expiration

    def verify_update_token(self, update_token):
        """
        Verifies the update token of a user
        """
        return update_token == self.update_token
