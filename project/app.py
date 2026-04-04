from pathlib import Path

from flask import Flask
from flask_cors import CORS

from routes import api

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None


if load_dotenv:
    # Load local project settings when a .env file is present.
    load_dotenv(Path(__file__).with_name(".env"))


def create_app():
    app = Flask(__name__)

    CORS(app)
    app.register_blueprint(api)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
