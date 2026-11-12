
def test_create_device(client):
    response = client.post(
        "/api/v1/devices/",
        json={
            "name": "Temperature Sensor 01",
            "mac_address": "AA:BB:CC:DD:EE:01",
            "device_type": "Temperature Sensor",
            "location": "Warsaw",
            "firmware_version": "1.0.0",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Temperature Sensor 01"
    assert data["mac_address"] == "AA:BB:CC:DD:EE:01"
    assert data["device_type"] == "Temperature Sensor"
    assert data["location"] == "Warsaw"
    assert data["firmware_version"] == "1.0.0"
    assert data["status"] == "OFFLINE"
    assert "id" in data


def test_get_devices(client):
    client.post(
        "/api/v1/devices/",
        json={
            "name": "Temperature Sensor 01",
            "mac_address": "AA:BB:CC:DD:EE:01",
            "device_type": "Temperature Sensor",
        },
    )

    response = client.get("/api/v1/devices/")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Temperature Sensor 01"


def test_get_device_by_id(client):
    create_response = client.post(
        "/api/v1/devices/",
        json={
            "name": "Humidity Sensor 01",
            "mac_address": "AA:BB:CC:DD:EE:02",
            "device_type": "Humidity Sensor",
        },
    )

    device_id = create_response.json()["id"]

    response = client.get(f"/api/v1/devices/{device_id}")

    assert response.status_code == 200
    assert response.json()["name"] == "Humidity Sensor 01"


def test_get_nonexistent_device(client):
    response = client.get("/api/v1/devices/9999")

    assert response.status_code == 404


def test_update_device(client):
    create_response = client.post(
        "/api/v1/devices/",
        json={
            "name": "Temperature Sensor 01",
            "mac_address": "AA:BB:CC:DD:EE:03",
            "device_type": "Temperature Sensor",
        },
    )

    device_id = create_response.json()["id"]

    response = client.patch(
        f"/api/v1/devices/{device_id}",
        json={
            "name": "Updated Temperature Sensor",
            "location": "Krakow",
            "firmware_version": "1.1.0",
        },
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Updated Temperature Sensor"
    assert response.json()["location"] == "Krakow"
    assert response.json()["firmware_version"] == "1.1.0"


def test_update_nonexistent_device(client):
    response = client.patch(
        "/api/v1/devices/9999",
        json={"name": "Updated Sensor"},
    )

    assert response.status_code == 404


def test_delete_device(client):
    create_response = client.post(
        "/api/v1/devices/",
        json={
            "name": "Temperature Sensor 01",
            "mac_address": "AA:BB:CC:DD:EE:04",
            "device_type": "Temperature Sensor",
        },
    )

    device_id = create_response.json()["id"]

    response = client.delete(f"/api/v1/devices/{device_id}")

    assert response.status_code == 204

    get_response = client.get(f"/api/v1/devices/{device_id}")

    assert get_response.status_code == 404


def test_delete_nonexistent_device(client):
    response = client.delete("/api/v1/devices/9999")

    assert response.status_code == 404


def test_create_device_with_duplicate_mac_address(client):
    payload = {
        "name": "Temperature Sensor 01",
        "mac_address": "AA:BB:CC:DD:EE:05",
        "device_type": "Temperature Sensor",
    }

    first_response = client.post("/api/v1/devices/", json=payload)
    second_response = client.post("/api/v1/devices/", json=payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 409


def test_create_device_with_invalid_data(client):
    response = client.post(
        "/api/v1/devices/",
        json={
            "name": "",
            "mac_address": "AA:BB:CC:DD:EE:06",
            "device_type": "Temperature Sensor",
        },
    )

    assert response.status_code == 422

def test_create_device_with_invalid_mac_address(client):
    response = client.post(
        "/api/v1/devices/",
        json={
            "name": "Invalid Sensor",
            "mac_address": "ZZ:ZZ:ZZ:ZZ:ZZ:ZZ",
            "device_type": "Temperature Sensor",
        },
    )

    assert response.status_code == 422


def test_update_device_with_null_name(client):
    create_response = client.post(
        "/api/v1/devices/",
        json={
            "name": "Temperature Sensor",
            "mac_address": "AA:BB:CC:DD:EE:11",
            "device_type": "Temperature Sensor",
        },
    )

    device_id = create_response.json()["id"]

    response = client.patch(
        f"/api/v1/devices/{device_id}",
        json={"name": None},
    )

    assert response.status_code == 422


def test_update_device_with_null_device_type(client):
    create_response = client.post(
        "/api/v1/devices/",
        json={
            "name": "Temperature Sensor",
            "mac_address": "AA:BB:CC:DD:EE:12",
            "device_type": "Temperature Sensor",
        },
    )

    device_id = create_response.json()["id"]

    response = client.patch(
        f"/api/v1/devices/{device_id}",
        json={"device_type": None},
    )

    assert response.status_code == 422



def test_update_device_with_null_location(client):
    create_response = client.post(
        "/api/v1/devices/",
        json={
            "name": "Temperature Sensor",
            "mac_address": "AA:BB:CC:DD:EE:13",
            "device_type": "Temperature Sensor",
            "location": "Warsaw",
        },
    )

    device_id = create_response.json()["id"]

    response = client.patch(
        f"/api/v1/devices/{device_id}",
        json={"location": None},
    )

    assert response.status_code == 200
    assert response.json()["location"] is None