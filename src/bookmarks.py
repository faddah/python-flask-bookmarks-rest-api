"""Bookmarks routes and management."""
import validators
from flask import (
    Blueprint,
    request,
    jsonify
)
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)
# type: ignore
from src.constants.http_status_codes import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_409_CONFLICT
)
from src.database import (
    Bookmark,
    db
)
# type: ignore



bookmarks = Blueprint("bookmarks", __name__, url_prefix="/api/v1/bookmarks")


@bookmarks.route("/", methods=["POST", "GET"])
@jwt_required()
def handle_bookmarks():
    """Get all bookmarks for the current user."""
    current_user = get_jwt_identity()

    if request.method == "POST":
        body = request.get_json().get('body', '')
        url = request.get_json().get('url', '')
        if not validators.url(url):
            return jsonify({
                "error": "Not a valid URL, please enter a valid URL."
            }), HTTP_400_BAD_REQUEST

        if Bookmark.query.filter_by(url=url).first() is not None:
            return jsonify({
                "error": "Bookmark URL already exists."
            }), HTTP_409_CONFLICT

        bookmark = Bookmark(
            url=url,
            body=body,
            user_id=current_user
        )

        db.session.add(bookmark)
        db.session.commit()

        return jsonify ({
            'id': bookmark.id,
            'url': bookmark.url,
            'short_url': bookmark.short_url,
            'visits': bookmark.visits,
            'body': bookmark.body,
            'created_at': bookmark.created_at,
            'updated_at': bookmark.updated_at
        }), HTTP_201_CREATED

    else:

        listed_bookmarks = Bookmark.query.filter_by(user_id=current_user).all()

        data = []

        for bookmark in listed_bookmarks:
            data.append({
                'id': bookmark.id,
                'url': bookmark.url,
                'short_url': bookmark.short_url,
                'visits': bookmark.visits,
                'body': bookmark.body,
                'created_at': bookmark.created_at,
                'updated_at': bookmark.updated_at
        })

    return jsonify({"data": data}), HTTP_200_OK


@bookmarks.route("/ping", methods=["GET"])
def ping():
    """Ping route to check if bookmarks blueprint is working."""
    return {"message": "Pong! Bookmarks blueprint is working."}
