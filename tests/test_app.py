import pytest

from src.app import ABOUT_PAYLOAD, APP_VERSION, HOME_MESSAGE, create_app


@pytest.fixture()
def client():
    app = create_app()
    app.config.update(TESTING=True)

    with app.test_client() as test_client:
        yield test_client


def test_home_route_returns_welcome_message(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json() == {"message": HOME_MESSAGE}


def test_health_route_returns_ok_status(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_hello_route_returns_personalized_message(client):
    response = client.get("/hello/Alice")

    assert response.status_code == 200
    assert response.get_json() == {"message": "Hello, Alice!"}


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (0, 0, 0),
        (2, 3, 5),
        (10, 15, 25),
    ],
)
def test_add_route_returns_sum(client, a, b, expected):
    response = client.get(f"/add/{a}/{b}")

    assert response.status_code == 200
    assert response.get_json() == {"a": a, "b": b, "result": expected}


def test_about_route_returns_project_metadata(client):
    response = client.get("/about")

    assert response.status_code == 200
    assert response.get_json() == ABOUT_PAYLOAD


def test_version_route_returns_project_version(client):
    response = client.get("/version")

    assert response.status_code == 200
    assert "version" in response.get_json()
    assert response.get_json()["version"] == APP_VERSION


def test_app_generates_a_secret_key_when_env_is_missing(monkeypatch):
    monkeypatch.delenv("FLASK_SECRET_KEY", raising=False)

    app = create_app()

    assert isinstance(app.config["SECRET_KEY"], str)
    assert len(app.config["SECRET_KEY"]) >= 32


def test_app_reads_secret_key_from_environment(monkeypatch):
    monkeypatch.setenv("FLASK_SECRET_KEY", "tp4-test-secret")

    app = create_app()

    assert app.config["SECRET_KEY"] == "tp4-test-secret"


def test_app_reads_secret_key_from_docker_environment(monkeypatch):
    monkeypatch.delenv("FLASK_SECRET_KEY", raising=False)
    monkeypatch.setenv("SECRET_KEY", "tp5-docker-secret")

    app = create_app()

    assert app.config["SECRET_KEY"] == "tp5-docker-secret"
