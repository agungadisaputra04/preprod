def test_create_user(client):
    response = client.post(
        "/user",
        json={
            "nama": "Test User",
            "umur": 25
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["message"] == "User berhasil disimpan"
    assert data["data"]["id"] is not None
    assert data["data"]["nama"] == "Test User"
    assert data["data"]["umur"] == 25


def test_get_user(client):
    create_response = client.post(
        "/user",
        json={
            "nama": "Agung",
            "umur": 24
        }
    )

    user_id = create_response.json()["data"]["id"]

    response = client.get(
        f"/users/{user_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == user_id
    assert data["nama"] == "Agung"
    assert data["umur"] == 24


def test_put_user(client):
    create_response = client.post(
        "/user",
        json={
            "nama": "Agung",
            "umur": 24
        }
    )

    user_id = create_response.json()["data"]["id"]

    response = client.put(
        f"/users/{user_id}",
        json={
            "nama": "Agung PUT",
            "umur": 30
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "User berhasil diupdate"
    assert data["data"]["id"] == user_id
    assert data["data"]["nama"] == "Agung PUT"
    assert data["data"]["umur"] == 30


def test_patch_user(client):
    create_response = client.post(
        "/user",
        json={
            "nama": "Agung",
            "umur": 24
        }
    )

    user_id = create_response.json()["data"]["id"]

    response = client.patch(
        f"/users/{user_id}",
        json={
            "umur": 31
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["data"]["id"] == user_id
    assert data["data"]["nama"] == "Agung"
    assert data["data"]["umur"] == 31


def test_delete_user(client):
    create_response = client.post(
        "/user",
        json={
            "nama": "Agung",
            "umur": 24
        }
    )

    user_id = create_response.json()["data"]["id"]

    response = client.delete(
        f"/users/{user_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "User berhasil dihapus"
    assert data["data"]["id"] == user_id

    response = client.get(
        f"/users/{user_id}"
    )

    assert response.status_code == 404
