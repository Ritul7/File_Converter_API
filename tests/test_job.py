import pytest
from unittest.mock import MagicMock

def test_create_job_success(client, auth_headers, mocker, db):

    mock_celery = mocker.patch("app.routes.jobs.process_job.delay")

    job_data = {
        "input_file_key": "uploads/my_file.py",
        "input_format": "pdf",
        "output_format": "docx"
    }

    response = client.post("/auth/jobs", json=job_data, headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "pending"
    assert data["input_format"] == "pdf"

    mock_celery.assert_called_once()





