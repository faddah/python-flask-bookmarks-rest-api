import validators  # type: ignore
from flask import Blueprint, jsonify, request  # type: ignore
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
)
from werkzeug.security import (
    check_password_hash,
    generate_password_hash,  # type: ignore
)

from src.constants.http_status_codes import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_409_CONFLICT,
)
from src.database import User, db

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.post("/register")
def register():
    username = request.json.get("username")
    email = request.json.get("email")
    password = request.json.get("password")

    if len(password) < 6:
        return jsonify(
            {"error": "Password is too short, < 6 characters."}
        ), HTTP_400_BAD_REQUEST

    if len(username) < 3:
        return jsonify(
            {"error": "User Name is too short, < 3 characters."}
        ), HTTP_400_BAD_REQUEST

    if not username.isalnum() or " " in username:
        return jsonify(
            {"error": "User Name should be alpha-numeric and without spaces."}
        ), HTTP_400_BAD_REQUEST

    if not validators.email(email):
        return jsonify(
            {"error": "Email is not a valid email address."}
        ), HTTP_400_BAD_REQUEST

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email is already in use."}), HTTP_409_CONFLICT

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "User Name is already in use."}), HTTP_409_CONFLICT

    pwd_hash = generate_password_hash(password)

    user = User(username=username, password=pwd_hash, email=email)
    db.session.add(user)
    db.session.commit()

    return jsonify(
        {
            "message": "User created & registered.",
            "user": {"username": username, "email": email},
        }
    ), HTTP_201_CREATED


@auth.post("/login")
def login():
    email = request.json.get("email", "")
    password = request.json.get("password", "")

    user = User.query.filter_by(email=email).first()

    if user:
        is_pass_correct = check_password_hash(user.password, password)

        if is_pass_correct:
            refresh = create_refresh_token(identity=user.id)
            access = create_access_token(identity=user.id)

            return jsonify(
                {
                    "user": {
                        "refresh": refresh,
                        "access": access,
                        "username": str(user.username),
                        "email": user.email,
                    }
                }
            ), HTTP_200_OK
    return jsonify(
        {"error": "Wrong email or password credentials."}
    ), HTTP_400_BAD_REQUEST


@auth.get("/me")
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    return jsonify({"username": user.username, "email": user.email}), HTTP_200_OK
