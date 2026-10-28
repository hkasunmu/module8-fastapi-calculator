"""Integration tests covering all endpoints and operations in main.py."""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_home_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "FastAPI Calculator" in response.text


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_operations_endpoint():
    response = client.get("/operations")
    assert response.status_code == 200
    assert set(response.json()["operations"]) == {
        "add", "subtract", "multiply", "divide", "power", "root"
    }


@pytest.mark.parametrize("operation,a,b,expected", [
    ("add", 6, 4, 10),
    ("subtract", 6, 4, 2),
    ("multiply", 6, 4, 24),
    ("divide", 6, 4, 1.5),
    ("power", 2, 4, 16),
    ("root", 81, 4, 3),
])
def test_calculate_operations(operation, a, b, expected):
    response = client.post("/calculate", json={"operation": operation, "a": a, "b": b})
    assert response.status_code == 200
    data = response.json()
    assert data["operation"] == operation
    assert data["result"] == pytest.approx(expected)


def test_calculate_division_by_zero():
    response = client.post("/calculate", json={"operation": "divide", "a": 5, "b": 0})
    assert response.status_code == 400
    assert "divide by zero" in response.json()["detail"]


def test_calculate_invalid_operation():
    response = client.post("/calculate", json={"operation": "unknown", "a": 1, "b": 2})
    assert response.status_code == 400
    assert response.json()["detail"] == "Unsupported operation"


def test_calculate_missing_field():
    response = client.post("/calculate", json={"operation": "add", "a": 1})
    assert response.status_code == 422


def test_calculate_invalid_root():
    response = client.post("/calculate", json={"operation": "root", "a": -16, "b": 2})
    assert response.status_code == 400


def test_static_css_is_served():
    response = client.get("/static/styles.css")
    assert response.status_code == 200
    assert "background" in response.text


def test_static_js_is_served():
    response = client.get("/static/app.js")
    assert response.status_code == 200
    assert "fetch" in response.text


def test_successful_calculation_is_logged(caplog):
    with caplog.at_level("INFO", logger="calculator"):
        response = client.post("/calculate", json={"operation": "add", "a": 7, "b": 8})
    assert response.status_code == 200
    assert "Calculated add" in caplog.text


def test_failed_calculation_is_logged(caplog):
    with caplog.at_level("WARNING", logger="calculator"):
        response = client.post("/calculate", json={"operation": "divide", "a": 7, "b": 0})
    assert response.status_code == 400
    assert "Calculation failed" in caplog.text
