import pytest
import app.main as m  # import the module so we can reset its fake DB
from fastapi.testclient import TestClient

client = TestClient(m.app)


# Reset the in-memory store before each test so tests don't affect each other
@pytest.fixture(autouse=True)
def reset_store():
    m.TASKS.clear()
    m.NEXT_ID = 1


def test_create_and_list():
    r = client.post("/tasks", json={"title": "Buy milk", "status": "todo"})
    assert r.status_code == 201
    tid = r.json()["id"]

    r = client.get("/tasks")
    assert r.status_code == 200
    ids = [t["id"] for t in r.json()]
    assert tid in ids


def test_validation():
    r = client.post("/tasks", json={"title": "", "status": "todo"})
    assert r.status_code == 422  # title is required (min length 1)


def test_get_update_delete():
    created = client.post("/tasks", json={"title": "A", "status": "todo"}).json()
    tid = created["id"]

    assert client.get(f"/tasks/{tid}").status_code == 200

    r = client.put(f"/tasks/{tid}", json={"title": "A2", "status": "doing"})
    assert r.status_code == 200
    assert r.json()["status"] == "doing"

    assert client.delete(f"/tasks/{tid}").status_code == 204
    assert client.get(f"/tasks/{tid}").status_code == 404
