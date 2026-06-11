from fastapi.testclient import TestClient

from jrebel.app import app


def test_index_renders() -> None:
    response = TestClient(app).get("/")

    assert response.status_code == 200
    assert "JRebel License Server" in response.text
    assert "服务运行中" in response.text


def test_health_check() -> None:
    response = TestClient(app).get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "version": "2.0.0",
        "service": "jrebel-license-server",
    }
