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
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
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

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

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
        listed_bookmarks = Bookmark.query.filter_by(
            user_id=current_user
        ).paginate(page=page, per_page=per_page)

        data = []

        for bookmark in listed_bookmarks.items:
            data.append({
                'id': bookmark.id,
                'url': bookmark.url,
                'short_url': bookmark.short_url,
                'visits': bookmark.visits,
                'body': bookmark.body,
                'created_at': bookmark.created_at,
                'updated_at': bookmark.updated_at
        })

        meta = {
            "page": listed_bookmarks.page,
            "pages": listed_bookmarks.pages,
            "total_count": listed_bookmarks.total,
            "per_page": listed_bookmarks.per_page,
            "prev_page": listed_bookmarks.prev_num,
            "next_page": listed_bookmarks.next_num,
            "has_prev": listed_bookmarks.has_prev,
            "has_next": listed_bookmarks.has_next
        }

    return jsonify({"data": data, "meta": meta}), HTTP_200_OK

@bookmarks.get("/<int:bookmark_id>")
@jwt_required()
def get_bookmark(bookmark_id):
    """Get a specific bookmark by ID for the current user."""
    current_user = get_jwt_identity()
    bookmark = Bookmark.query.filter_by(
        id=bookmark_id,
        user_id=current_user
    ).first()

    if not bookmark:
        return jsonify({
            "error": "Bookmark not found."
        }), HTTP_404_NOT_FOUND

    return jsonify ({
        'id': bookmark.id,
        'url': bookmark.url,
        'short_url': bookmark.short_url,
        'visits': bookmark.visits,
        'body': bookmark.body,
        'created_at': bookmark.created_at,
        'updated_at': bookmark.updated_at
    }), HTTP_200_OK


@bookmarks.put("/<int:bookmark_id>")
@bookmarks.patch("/<int:bookmark_id>")
@jwt_required()
def edit_bookmark(bookmark_id):
    """Edit a specific bookmark by ID for the current user."""
    current_user = get_jwt_identity()
    bookmark = Bookmark.query.filter_by(
        id=bookmark_id,
        user_id=current_user
    ).first()

    if not bookmark:
        return jsonify({
            "error": "Bookmark not found."
        }), HTTP_404_NOT_FOUND

    body = request.get_json().get('body', '')
    url = request.get_json().get('url', '')

    if not validators.url(url):
        return jsonify({
            "error": "Not a valid URL, please enter a valid URL."
        }), HTTP_400_BAD_REQUEST

    bookmark.body = body
    bookmark.url = url

    db.session.commit()

    return jsonify ({
        'id': bookmark.id,
        'url': bookmark.url,
        'short_url': bookmark.short_url,
        'visits': bookmark.visits,
        'body': bookmark.body,
        'created_at': bookmark.created_at,
        'updated_at': bookmark.updated_at
    }), HTTP_200_OK

@bookmarks.delete("/<int:bookmark_id>")
@jwt_required()
def delete_bookmark(bookmark_id):
    """Delete a specific bookmark by ID for the current user."""
    current_user = get_jwt_identity()
    bookmark = Bookmark.query.filter_by(
        id=bookmark_id,
        user_id=current_user
    ).first()

    if not bookmark:
        return jsonify({
            "error": "Bookmark not found."
        }), HTTP_404_NOT_FOUND

    bookmark_id_deleted = bookmark.id
    db.session.delete(bookmark)
    db.session.commit()

    return jsonify({"message": "Bookmark " + str(bookmark_id_deleted) + " deleted successfully."}), HTTP_204_NO_CONTENT

@bookmarks.route("/ping", methods=["GET"])
def ping():
    """Ping route to check if bookmarks blueprint is working."""
    return {"message": "Pong! Bookmarks blueprint is working."}
