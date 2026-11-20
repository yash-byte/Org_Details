"""API tests for the Org Details web service."""

from pathlib import Path

import pytest

from web_service.app import create_app


@pytest.fixture()
def data_dir(tmp_path: Path) -> Path:
    (tmp_path / "name.txt").write_text("Acme Corp\n", encoding="utf-8")
    (tmp_path / "address.txt").write_text("Mumbai office address: Bhandup\n", encoding="utf-8")
    (tmp_path / "employees.txt").write_text("employee file\n", encoding="utf-8")
    return tmp_path


@pytest.fixture()
def client(data_dir: Path):
    app = create_app(data_dir)
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


def test_health_ok(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_api_org(client):
    response = client.get("/api/org")
    assert response.status_code == 200
    assert response.get_json() == {
        "name": "Acme Corp",
        "address": "Mumbai office address: Bhandup",
        "employees": "employee file",
    }


def test_api_field_endpoints(client):
    assert client.get("/api/name").get_json() == {"name": "Acme Corp"}
    assert client.get("/api/address").get_json() == {
        "address": "Mumbai office address: Bhandup"
    }
    assert client.get("/api/employees").get_json() == {"employees": "employee file"}


def test_index_html(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Acme Corp" in response.data
    assert b"Org Details" in response.data


def test_index_json_via_accept(client):
    response = client.get("/", headers={"Accept": "application/json"})
    assert response.status_code == 200
    assert response.get_json()["name"] == "Acme Corp"


def test_missing_file_returns_404(tmp_path: Path):
    (tmp_path / "name.txt").write_text("Only name", encoding="utf-8")
    app = create_app(tmp_path)
    app.config["TESTING"] = True
    with app.test_client() as client:
        response = client.get("/api/address")
        assert response.status_code == 404
        assert "Missing data file" in response.get_json()["error"]
