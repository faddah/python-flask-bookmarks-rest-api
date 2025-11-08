"""Bookmarks routes and management."""

from flask import Blueprint


bookmarks = Blueprint("bookmarks", __name__, url_prefix="/api/v1/bookmarks")


@bookmarks.get("/")
def get_all():
    """Get all bookmarks for the current user."""
    return {"bookmarks": []}


@bookmarks.route("/ping", methods=["GET"])
def ping():
    """Ping route to check if bookmarks blueprint is working."""
    return {"message": "Pong! Bookmarks blueprint is working."}
