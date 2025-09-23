from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_analyze_min():
    body = {"text": "begin x <- 1 end", "want_diagram": False}
    r = client.post("/api/analyzer/analyze", json=body)
    assert r.status_code == 200
    data = r.json()
    assert data["bounds"]["big_o"] == "O(n)"
    assert "Se detectaron 1 asignaciones" in " ".join([s["description"] for s in data["reasoning"]])

def test_grammar_validate():
    r = client.post("/api/grammar/validate", json={"text": "begin end"})
    assert r.status_code == 200
    assert r.json()["valid"] is True
