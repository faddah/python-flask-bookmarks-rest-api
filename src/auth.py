from flask import Blueprint, jsonify, request  # type: ignore
from werkzeug.security import generate_password_hash  # type: ignore

from src.constants.http_status_codes import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_409_CONFLICT,
)
from src.database import User, db

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.post("/register")
def register():
    return "User created & registered."


@auth.get("/me")
def me():
    return {"user": "me"}
