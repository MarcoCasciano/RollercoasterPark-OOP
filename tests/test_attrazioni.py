def test_create_attrazione(client, attrazione_data):
    resp = client.post("/attrazioni/", json=attrazione_data)
    assert resp.status_code == 201
    body = resp.json()
    assert body["nome"] == attrazione_data["nome"]
    assert body["per_bambini"] == attrazione_data["per_bambini"]
    assert body["capienza_massima"] == attrazione_data["capienza_massima"]
    assert "id" in body


def test_list_attrazioni(client, attrazione_data):
    client.post("/attrazioni/", json=attrazione_data)
    resp = client.get("/attrazioni/")
    assert resp.status_code == 200
    items = resp.json()
    assert len(items) == 1
    assert items[0]["nome"] == attrazione_data["nome"]


def test_get_attrazione(client, attrazione_data):
    created = client.post("/attrazioni/", json=attrazione_data).json()
    resp = client.get(f"/attrazioni/{created['id']}")
    assert resp.status_code == 200
    assert resp.json()["nome"] == attrazione_data["nome"]


def test_get_attrazione_not_found(client):
    resp = client.get("/attrazioni/999")
    assert resp.status_code == 404


def test_update_attrazione(client, attrazione_data):
    created = client.post("/attrazioni/", json=attrazione_data).json()
    resp = client.patch(f"/attrazioni/{created['id']}", json={"nome": "Tornado"})
    assert resp.status_code == 200
    assert resp.json()["nome"] == "Tornado"
    assert resp.json()["capienza_massima"] == attrazione_data["capienza_massima"]


def test_delete_attrazione(client, attrazione_data):
    created = client.post("/attrazioni/", json=attrazione_data).json()
    resp = client.delete(f"/attrazioni/{created['id']}")
    assert resp.status_code == 204
    resp = client.get(f"/attrazioni/{created['id']}")
    assert resp.status_code == 404
