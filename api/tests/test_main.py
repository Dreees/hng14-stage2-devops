import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check():
    """Test that /health endpoint returns 200 and status ok"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@patch("main.r")
def test_create_job(mock_redis):
    """Test that POST /jobs creates a job and returns 201 with job_id"""
    mock_redis.lpush.return_value = 1
    mock_redis.hset.return_value = 1

    response = client.post("/jobs")

    assert response.status_code == 201
    data = response.json()
    assert "job_id" in data
    assert isinstance(data["job_id"], str)
    assert len(data["job_id"]) > 0
    mock_redis.lpush.assert_called_once()
    mock_redis.hset.assert_called_once()


@patch("main.r")
def test_get_job_status_found(mock_redis):
    """Test that GET /jobs/{id} returns status when job exists"""
    mock_redis.hget.return_value = "completed"

    response = client.get("/jobs/test-job-123")

    assert response.status_code == 200
    data = response.json()
    assert data["job_id"] == "test-job-123"
    assert data["status"] == "completed"


@patch("main.r")
def test_get_job_not_found(mock_redis):
    """Test that GET /jobs/{id} returns 404 when job does not exist"""
    mock_redis.hget.return_value = None

    response = client.get("/jobs/nonexistent-999")

    assert response.status_code == 404


@patch("main.r")
def test_create_job_sets_queued_status(mock_redis):
    """Test that new job is stored with queued status in Redis"""
    mock_redis.lpush.return_value = 1
    mock_redis.hset.return_value = 1

    response = client.post("/jobs")
    data = response.json()
    job_id = data["job_id"]

    mock_redis.hset.assert_called_with(
        f"job:{job_id}",
        "status",
        "queued"
    )