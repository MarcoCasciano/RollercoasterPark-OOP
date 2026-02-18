def test_create_giro(client, attrazione_data, visitatore_data, giro_data):
    attr = client.post("/attrazioni/", json=attrazione_data).json()
    vis = client.post("/visitatori/", json=visitatore_data).json()
    giro_data["attrazione_id"] = attr["id"]
    giro_data["visitatore_id"] = vis["id"]
    resp = client.post("/giri/", json=giro_data)
    assert resp.status_code == 201
    body = resp.json()
    assert body["attrazione_id"] == attr["id"]
    assert body["visitatore_id"] == vis["id"]
    assert "id" in body


def test_list_giri(client, attrazione_data, visitatore_data, giro_data):
    attr = client.post("/attrazioni/", json=attrazione_data).json()
    vis = client.post("/visitatori/", json=visitatore_data).json()
    giro_data["attrazione_id"] = attr["id"]
    giro_data["visitatore_id"] = vis["id"]
    client.post("/giri/", json=giro_data)
    resp = client.get("/giri/")
    assert resp.status_code == 200
    items = resp.json()
    assert len(items) == 1


def test_get_giro(client, attrazione_data, visitatore_data, giro_data):
    attr = client.post("/attrazioni/", json=attrazione_data).json()
    vis = client.post("/visitatori/", json=visitatore_data).json()
    giro_data["attrazione_id"] = attr["id"]
    giro_data["visitatore_id"] = vis["id"]
    created = client.post("/giri/", json=giro_data).json()
    resp = client.get(f"/giri/{created['id']}")
    assert resp.status_code == 200
    body = resp.json()
    assert "timestamp" in body
    assert body["ciclo"] == giro_data["ciclo"]


def test_get_giro_not_found(client):
    resp = client.get("/giri/999")
    assert resp.status_code == 404


def test_delete_giro(client, attrazione_data, visitatore_data, giro_data):
    attr = client.post("/attrazioni/", json=attrazione_data).json()
    vis = client.post("/visitatori/", json=visitatore_data).json()
    giro_data["attrazione_id"] = attr["id"]
    giro_data["visitatore_id"] = vis["id"]
    created = client.post("/giri/", json=giro_data).json()
    resp = client.delete(f"/giri/{created['id']}")
    assert resp.status_code == 204
    resp = client.get(f"/giri/{created['id']}")
    assert resp.status_code == 404
