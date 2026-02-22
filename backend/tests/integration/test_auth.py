from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_signup_and_login():
    response = client.post("/api/v1/auth/signup", json={
        "email": "ci@test.com",
        "password": "Password123"
    })
    assert response.status_code == 200

    response = client.post("/api/v1/auth/login", json={
        "email": "ci@test.com",
        "password": "Password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()