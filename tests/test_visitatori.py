def test_create_visitatore(client, visitatore_data):
    resp = client.post("/visitatori/", json=visitatore_data)
    assert resp.status_code == 201
    body = resp.json()
    assert body["nome"] == visitatore_data["nome"]
    assert body["cognome"] == visitatore_data["cognome"]
    assert body["tipo"] == "adulto"
    assert "id" in body


def test_create_visitatore_con_famiglia(client, visitatore_data, famiglia_data):
    fam = client.post("/famiglie/", json=famiglia_data).json()
    visitatore_data["famiglia_id"] = fam["id"]
    resp = client.post("/visitatori/", json=visitatore_data)
    assert resp.status_code == 201
    assert resp.json()["famiglia_id"] == fam["id"]


def test_list_visitatori(client, visitatore_data):
    client.post("/visitatori/", json=visitatore_data)
    resp = client.get("/visitatori/")
    assert resp.status_code == 200
    items = resp.json()
    assert len(items) == 1
    assert items[0]["nome"] == visitatore_data["nome"]


def test_get_visitatore(client, visitatore_data):
    created = client.post("/visitatori/", json=visitatore_data).json()
    resp = client.get(f"/visitatori/{created['id']}")
    assert resp.status_code == 200
    body = resp.json()
    assert body["nome"] == visitatore_data["nome"]
    assert "giri" in body
    assert isinstance(body["giri"], list)


def test_get_visitatore_not_found(client):
    resp = client.get("/visitatori/999")
    assert resp.status_code == 404


def test_update_visitatore(client, visitatore_data):
    created = client.post("/visitatori/", json=visitatore_data).json()
    resp = client.patch(f"/visitatori/{created['id']}", json={"nome": "Luca"})
    assert resp.status_code == 200
    assert resp.json()["nome"] == "Luca"
    assert resp.json()["cognome"] == visitatore_data["cognome"]


def test_delete_visitatore(client, visitatore_data):
    created = client.post("/visitatori/", json=visitatore_data).json()
    resp = client.delete(f"/visitatori/{created['id']}")
    assert resp.status_code == 204
    resp = client.get(f"/visitatori/{created['id']}")
    assert resp.status_code == 404


def test_tipo_validazione(client, visitatore_data):
    visitatore_data["tipo"] = "alieno"
    resp = client.post("/visitatori/", json=visitatore_data)
    assert resp.status_code == 422
