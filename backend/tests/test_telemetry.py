def create_device(client):
    response = client.post(
        "/api/v1/devices/",
        json={
            "name": "Temperature Sensor",
            "mac_address": "AA:BB:CC:DD:EE:01",
            "device_type": "temperature_sensor",
            "location": "Warsaw",
            "firmware_version": "1.0.0",
        },
    )

    assert response.status_code == 201
    return response.json()["id"]


def test_create_telemetry(client):
    device_id = create_device(client)

    response = client.post(
        f"/api/v1/devices/{device_id}/telemetry/",
        json={
            "metric": "temperature",
            "value": 23.7,
            "unit": "C",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["device_id"] == device_id
    assert data["metric"] == "temperature"
    assert data["value"] == 23.7
    assert data["unit"] == "C"
    assert "id" in data
    assert "recorded_at" in data


def test_get_device_telemetry(client):
    device_id = create_device(client)

    client.post(
        f"/api/v1/devices/{device_id}/telemetry/",
        json={
            "metric": "temperature",
            "value": 23.7,
            "unit": "C",
        },
    )

    client.post(
        f"/api/v1/devices/{device_id}/telemetry/",
        json={
            "metric": "humidity",
            "value": 45.0,
            "unit": "%",
        },
    )

    response = client.get(
        f"/api/v1/devices/{device_id}/telemetry/"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["metric"] == "humidity"
    assert data[1]["metric"] == "temperature"
