import pytest
from fastapi.testclient import TestClient

from app import main

client = TestClient(main.app)


@pytest.fixture(autouse=True)
def limpiar_db():
    main._db.clear()
    main._next_id = 1


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_crear_y_obtener_tarea():
    r = client.post("/tareas", json={"titulo": "Estudiar CI"})
    assert r.status_code == 201
    assert r.json() == {"id": 1, "titulo": "Estudiar CI", "hecha": False}
    assert client.get("/tareas/1").json()["titulo"] == "Estudiar CI"


def test_listar_tareas():
    client.post("/tareas", json={"titulo": "A"})
    client.post("/tareas", json={"titulo": "B"})
    assert len(client.get("/tareas").json()) == 2


def test_titulo_vacio_es_invalido():
    assert client.post("/tareas", json={"titulo": ""}).status_code == 422


def test_obtener_inexistente_da_404():
    assert client.get("/tareas/99").status_code == 404


def test_borrar_tarea():
    client.post("/tareas", json={"titulo": "X"})
    assert client.delete("/tareas/1").status_code == 204
    assert client.get("/tareas/1").status_code == 404


def test_borrar_inexistente_da_404():
    assert client.delete("/tareas/99").status_code == 404
