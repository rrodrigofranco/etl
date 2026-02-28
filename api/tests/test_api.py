import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/docs")
    assert response.status_code == 200

def test_data_endpoint_returns_json():
    response = client.get("/data")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_data_contains_expected_fields():
    response = client.get("/data")
    data = response.json()

    assert "timestamp" in data[0]
    assert "wind_speed" in data[0]
    assert "power" in data[0]

def test_data_with_date_filter():
    response = client.get(
        "/data",
        params={
            "start": "2024-01-01 00:00:00",
            "end": "2024-01-01 01:00:00"
        }
    )

    assert response.status_code == 200
    data = response.json()

    for row in data:
        assert row["timestamp"] >= "2024-01-01"