def test_create_famiglia(client, famiglia_data):
    resp = client.post("/famiglie/", json=famiglia_data)
    assert resp.status_code == 201
    body = resp.json()
    assert body["cognome"] == famiglia_data["cognome"]
    assert body["num_adulti"] == famiglia_data["num_adulti"]
    assert "id" in body


def test_list_famiglie(client, famiglia_data):
    client.post("/famiglie/", json=famiglia_data)
    resp = client.get("/famiglie/")
    assert resp.status_code == 200
    items = resp.json()
    assert len(items) == 1
    assert items[0]["cognome"] == famiglia_data["cognome"]


def test_get_famiglia(client, famiglia_data):
    created = client.post("/famiglie/", json=famiglia_data).json()
    resp = client.get(f"/famiglie/{created['id']}")
    assert resp.status_code == 200
    body = resp.json()
    assert body["cognome"] == famiglia_data["cognome"]
    assert "visitatori" in body
    assert isinstance(body["visitatori"], list)


def test_get_famiglia_not_found(client):
    resp = client.get("/famiglie/999")
    assert resp.status_code == 404


def test_update_famiglia(client, famiglia_data):
    created = client.post("/famiglie/", json=famiglia_data).json()
    resp = client.patch(f"/famiglie/{created['id']}", json={"cognome": "Bianchi"})
    assert resp.status_code == 200
    assert resp.json()["cognome"] == "Bianchi"
    assert resp.json()["num_adulti"] == famiglia_data["num_adulti"]


def test_delete_famiglia(client, famiglia_data):
    created = client.post("/famiglie/", json=famiglia_data).json()
    resp = client.delete(f"/famiglie/{created['id']}")
    assert resp.status_code == 204
    resp = client.get(f"/famiglie/{created['id']}")
    assert resp.status_code == 404
