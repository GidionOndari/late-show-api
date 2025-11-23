from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

# Initialize SQLAlchemy
db = SQLAlchemy()

# ----------------- Episode Model -----------------
class Episode(db.Model, SerializerMixin):
    __tablename__ = "episodes"
    serialize_rules = ('-appearances.episode',)

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    number = db.Column(db.Integer, nullable=False)

    # Relationship: One episode has many appearances
    appearances = db.relationship(
        "Appearance",
        back_populates="episode",
        cascade="all, delete-orphan"
    )

# ----------------- Guest Model -----------------
class Guest(db.Model, SerializerMixin):
    __tablename__ = "guests"
    serialize_rules = ('-appearances.guest',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    occupation = db.Column(db.String, nullable=False)

    # Relationship: One guest can have many appearances
    appearances = db.relationship(
        "Appearance",
        back_populates="guest",
        cascade="all, delete-orphan"
    )

# ----------------- Appearance Model -----------------
class Appearance(db.Model, SerializerMixin):
    __tablename__ = "appearances"
    serialize_rules = ('-episode.appearances', '-guest.appearances')

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'), nullable=False)

    # Relationships
    episode = db.relationship("Episode", back_populates="appearances")
    guest = db.relationship("Guest", back_populates="appearances")

    # Validation: rating must be integer between 1 and 5
    @validates('rating')
    def validate_rating(self, key, rating):
        if not isinstance(rating, int):
            raise ValueError("Rating must be an integer")
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        return rating
