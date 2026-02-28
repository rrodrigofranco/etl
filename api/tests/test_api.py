import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/docs")
    assert response.status_code == 200

def test_data_with_date_filter_and_returns_json():
    response = client.get(
        "/data",
        params={
            "start": "2024-01-01 00:00:00",
            "end": "2024-01-01 01:00:00",
            "variables": ["wind_speed", "power"]
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "timestamp" in data[0]
    assert "wind_speed" in data[0]
    assert "power" in data[0]

    for row in data:
        assert row["timestamp"] >= "2024-01-01"