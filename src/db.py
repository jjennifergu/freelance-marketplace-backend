from enum import auto
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

buyer_association_table = db.Table(
    "buyer_association",
    db.Column("listing_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("user_id"), db.Integer, db.ForeignKey("listings.id")
)

seller_association_table = db.Table(
    "seller_association",
    db.Column("listing_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("user_id"), db.Integer, db.ForeignKey("listings.id")
)

class Listing(db.Model):
    """
    Listing model

    Has a many-to-many relationship with User model
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
    sellers=db.relationship("User", secondary=seller_association_table, back_populates="seller_listings")
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
            "sellers": [s.simple_serialize() for s in self.sellers],
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
    """
    __tablename__="users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False)
    contact = db.Column(db.String, nullable=False)
    seller_listings=db.relationship("Listing", secondary=seller_association_table, back_populates="sellers")
    buyer_listings=db.relationship("Listing", secondary=buyer_association_table, back_populates="buyers")

    def __init__(self, **kwargs):
        """
        initializes User object
        """
        self.username = kwargs.get("username", "")
    
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
