import os
import secrets

from flask import Flask, jsonify

HOME_MESSAGE = "Bienvenue sur l'application Flask du TP 2."
ABOUT_PAYLOAD = {"app": "Mon projet Flask", "version": "1.0"}


def get_secret_key():
    return os.getenv("FLASK_SECRET_KEY") or secrets.token_hex(32)


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = get_secret_key()

    @app.get("/")
    def index():
        return jsonify({"message": HOME_MESSAGE})

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.get("/hello/<name>")
    def hello(name):
        return jsonify({"message": f"Hello, {name}!"})

    @app.get("/add/<int:a>/<int:b>")
    def add(a, b):
        return jsonify({"a": a, "b": b, "result": a + b})

    @app.get("/about")
    def about():
        return jsonify(ABOUT_PAYLOAD)

    return app


app = create_app()


if __name__ == "__main__":  # pragma: no cover
    app.run()
