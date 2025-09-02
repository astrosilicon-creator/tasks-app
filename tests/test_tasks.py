from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_list_update_delete():
    # create
    r = client.post("/tasks", json={"title": "Buy milk", "status": "todo"})
    assert r.status_code == 201
    tid = r.json()["id"]

    # list (don't assume empty DB; just assert our id is present)
    r = client.get("/tasks")
    assert r.status_code == 200
    ids = [t["id"] for t in r.json()]
    assert tid in ids

    # update
    r = client.put(f"/tasks/{tid}", json={"title": "Buy milk", "status": "doing"})
    assert r.status_code == 200
    assert r.json()["status"] == "doing"

    # delete
    r = client.delete(f"/tasks/{tid}")
    assert r.status_code == 204
