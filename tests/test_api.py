from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 201
    assert response.json() == {
        "message": "API is running",
	"version": "1.0"
    }


def test_get_users():
    response = client.get("/users")

    assert response.status_code == 200

    data = response.json()

    assert "total" in data
    assert "data" in data
    assert isinstance(data["total"], int)
    assert isinstance(data["data"], list)


def test_get_user_not_found():
    response = client.get("/users/999999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "User tidak ditemukan"
    }


def test_create_user_validation_error():
    response = client.post(
        "/user",
        json={
            "nama": "Testing",
            "umur": "abc"
        }
    )

    assert response.status_code == 422


def test_create_user_missing_field():
    response = client.post(
        "/user",
        json={
            "nama": "Testing"
        }
    )

    assert response.status_code == 422


def test_create_user_invalid_type():
    response = client.post(
        "/user",
        json={
            "nama": "Testing",
            "umur": "bukan angka"
        }
    )

    assert response.status_code == 422

def test_info():
    response = client.get("/info")

    assert response.status_code == 200
    assert response.json() == {
        "name": "API Lab",
        "description": "REST API untuk belajar DevOps"
	}

def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy"
    }
