import os
import pytest
from fastapi.testclient import TestClient
from main import app

API_TOKEN = os.getenv("API_TOKEN", "test-token")

client = TestClient(app)

# Testing if the docs endpoint is working
def test_health_check():
    response = client.get(
        "/docs",
        headers={
            "Authorization": f"Bearer {API_TOKEN}"
        }
    )
    assert response.status_code == 200

# Testing if the date filter returns JSON correctly
def test_data_with_date_filter_and_returns_json():
    response = client.get(
        "/data",
        params={
            "start": "2024-01-01 00:00:00",
            "end": "2024-01-01 01:00:00",
            "variables": ["wind_speed", "power"],
        },
        headers={
            "Authorization": f"Bearer {API_TOKEN}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0

    assert "timestamp" in data[0]
    assert "wind_speed" in data[0]
    assert "power" in data[0]

    for row in data:
        assert row["timestamp"] >= "2024-01-01"