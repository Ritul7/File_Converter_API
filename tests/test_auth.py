def test_register_user(client):             # client: Ek TestClient offer krta h jo ki fake HTTP request send krta h on our fastAPI
    response = client.post(
        '/auth/register',
        json={
            "email": "test@example.com", 
            "password": "password123"
        }
    )

    assert response.status_code == 200
    assert response.json()["message"] == "User created successfully"


def test_login_user(client):                        # Here, we again registered the use, because after every test we are clearing the tables. So, for checking the login, the user must be registered first.
    client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "test@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()

