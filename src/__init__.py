"""Flask application factory and configuration."""
import os
import importlib.metadata
from flask import Flask  # pylint: disable=no-name-in-module
from flask_jwt_extended import JWTManager  # pylint: disable=no-name-in-module
from src.auth import auth
from src.bookmarks import bookmarks
from src.database import db


def list_installed_packages():
    """Return sorted list of installed Python packages with versions."""
    installed_packages = importlib.metadata.distributions()
    return sorted([f"{i.metadata['Name']}=={i.version}" for i in installed_packages])


def create_app(test_config=None):
    """Create and configure Flask application instance."""
    app = Flask(__name__, instance_relative_config=True, static_folder='static')

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DATABASE_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY"),
        )
    else:
        app.config.from_mapping(test_config)

    db.app = app
    db.init_app(app)

    JWTManager(app)

    # Add this block to create the database tables
    with app.app_context():
        db.create_all()

    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)

    @app.get("/")
    def index():
        """Render home page."""
        return (
            "<div style=\""
            "background-color: cornsilk; "
            "color: navy; "
            "display: flex; "
            "flex-direction: column; "
            "font-size: 30px; "
            "justify-content: center; "
            "align-items: center; "
            "height: 100vh;\">" 
            "<h1>Hello, This Is Faddah's World!</h1>"
            "<h2>'N' Yr Jez Livin' Innit.</h2>"
            "<h3>Version 1.0.0</h3>"
            "</div>"
        )

    @app.get("/hello")
    def say_hello():
        """Return hello message JSON."""
        return {
            "message": "Hello — This Is Faddah's World!",
            "sub-message": "'N' Yr Jez Livin' Innit.",
            "version": "0.0.1",
        }

    @app.get("/packages")
    def list_packages():
        """Return list of installed packages."""
        packages = list_installed_packages()
        return {"packages": packages}

    @app.route('/favicon.ico')
    def favicon():
        """Serve the favicon."""
        return app.send_static_file('favicon.ico')

    return app
