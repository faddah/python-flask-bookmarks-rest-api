"""Database models for User and Bookmark."""
# from enum import unique
from datetime import datetime
import string
import random
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """User model for storing user account information."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.Text(), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    bookmarks = db.relationship("Bookmark", backref="user")

    def get_bookmarks_count(self):
        """Return the count of bookmarks for this user."""
        return len(self.bookmarks)

    def __repr__(self):
        return f"User>>> {self.username}"


class Bookmark(db.Model):
    """Bookmark model for storing user bookmarks with short URLs."""
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text(), nullable=True)
    url = db.Column(db.Text(), nullable=False)
    short_url = db.Column(db.String(3), nullable=False)
    visits = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def generate_short_characters(self):
        """Generate a unique 3-character short URL code."""
        characters = string.digits + string.ascii_letters
        picked_chars = "".join(random.choices(characters, k=3))

        link = self.query.filter_by(short_url=picked_chars).first()

        if link:
            # If collision exists, generate a new one recursively
            return self.generate_short_characters()
        else:
            return picked_chars

    def __init__(self, **kwargs):
        """Initialize bookmark with auto-generated short URL."""
        super().__init__(**kwargs)
        self.short_url = self.generate_short_characters()

    def __repr__(self):
        return f"Bookmark>>> {self.url}"
