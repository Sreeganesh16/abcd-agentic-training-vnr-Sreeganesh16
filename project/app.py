from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

from backend import create_app


if load_dotenv:
    # Load local project settings when a .env file is present.
    load_dotenv(Path(__file__).with_name(".env"))


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
