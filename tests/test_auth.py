import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient
from app.api.main import app

client = TestClient(app)

def test_register_login():
    # Test /register
    response = client.post("/register", json={
        "username": "testuser",
        "email": "test@test.com",
        "password": "test123"
    })
    assert response.status_code in [200, 400]

    # Test /login avec OAuth2PasswordRequestForm (form-data)
    response = client.post("/login", data={
        "username": "testuser",
        "password": "test123"
    })
    assert response.status_code in [200, 401]

    if response.status_code == 200:
        json_data = response.json()
        assert "access_token" in json_data
        assert json_data["token_type"] == "bearer"