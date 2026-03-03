import pytest
from unittest.mock import AsyncMock

def test_get_upload_url_authenticated(client, auth_headers, mocker):
    
    mock_s3 = mocker.patch("app.routes.files.generate_upload_url", new_callable=AsyncMock)
    mock_s3.return_value = {
        "upload_url": "http://fake-s3.com",
        "file_key": "uploads/test.pdf"
        }

    response = client.post(
        "/file/get_upload_url",
        files={"my_file": ("test.pdf", b"fake content", "application/pdf")},
        headers=auth_headers
    )

    assert response.status_code == 200
    assert "upload_url" in response.json()
    mock_s3.assert_called_once()


def test_get_upload_url_unauthorized(client):               # A user which is not authenticated can't get the url to upload their file
    
    response = client.post("/file/get_upload_url", files={"my_file": ("test.pdf", b"abc")})
    assert response.status_code == 401  


