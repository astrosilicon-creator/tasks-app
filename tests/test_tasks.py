from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_list_update_delete(client):
    # create
    r = client.post("/tasks", json={"title": "Buy milk", "status": "todo"})
    assert r.status_code == 201
    tid = r.json()["id"]

    # list
    r = client.get("/tasks")
    ids = [t["id"] for t in r.json()]
    assert tid in ids

    # update
    r = client.put(f"/tasks/{tid}", json={"title": "Buy milk", "status": "doing"})
    assert r.status_code == 200
    assert r.json()["status"] == "doing"

    # delete
    r = client.delete(f"/tasks/{tid}")
    assert r.status_code == 204
