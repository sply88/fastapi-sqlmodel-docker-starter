from fastapi.testclient import TestClient

from api.routers.health import router

client = TestClient(router)


def test_ping():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"msg": "ok"}
