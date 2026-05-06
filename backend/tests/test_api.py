import os

from fastapi.testclient import TestClient

# Las pruebas usan flujo de desarrollo por email para no depender de token real de Google.
os.environ["ALLOW_DEV_EMAIL_LOGIN"] = "true"

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_health_deps_shape() -> None:
    response = client.get("/health/deps")
    assert response.status_code == 200
    body = response.json()
    assert "google" in body
    assert "supabase" in body
    assert "configured" in body["google"]
    assert "configured" in body["supabase"]
    assert "connected" in body["supabase"]


def test_full_registration_flow() -> None:
    login = client.post(
        "/api/auth/google-login",
        json={"email": "alumno@estudiantes.udg.mx", "full_name": "Alumno UDG"},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    pre = client.post("/api/registrations/pre-register", headers=headers)
    assert pre.status_code == 200
    assert pre.json()["status"] in {"pending_questionnaire", "completed"}

    questions = client.get("/api/questionnaires/questions")
    assert questions.status_code == 200
    assert len(questions.json()) == 4

    payload = [
        {"question_id": 1, "answer": "Me interesa aprender Python para web"},
        {"question_id": 2, "answer": "Espero salir con una app publicada"},
        {"question_id": 3, "answer": "Si, seria una gran opcion de verano"},
        {"question_id": 4, "answer": "Mas laboratorios practicos y proyectos reales"},
    ]

    submit = client.post("/api/questionnaires/responses", json=payload, headers=headers)
    assert submit.status_code == 200

    status = client.get("/api/registrations/status", headers=headers)
    assert status.status_code == 200
    assert status.json()["status"] == "completed"

