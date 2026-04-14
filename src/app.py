from flask import Flask, jsonify

HOME_MESSAGE = "Bienvenue sur l'application Flask du TP 2."
ABOUT_PAYLOAD = {
    "application": "tp2-ci-flask",
    "framework": "Flask",
    "ci": "GitHub Actions",
}


def create_app():
    app = Flask(__name__)

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
    app.run(debug=True)
