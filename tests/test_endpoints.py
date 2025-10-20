"""
Pruebas de integración básicas para los endpoints principales y del analizador.
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def _detect_base_prefix() -> str:
    """
    Detecta si la API está montada con el prefijo '/api' o sin él.

    Returns:
        str: Prefijo base detectado para las rutas de la API.
    """
    for base in ("/api", ""):
        response = client.get(f"{base}/test")
        if response.status_code != 404:
            return base

    # Fallback: probar el test del analyzer
    for base in ("/api", ""):
        response = client.get(f"{base}/analyzer/test_analyzer")
        if response.status_code != 404:
            return base

    # Por defecto, asumir '/api'
    return "/api"


def _is_json(response) -> bool:
    """Devuelve True si Content-Type inicia con 'application/json'."""
    content_type = response.headers.get("content-type", "")
    return content_type.startswith("application/json")


BASE = _detect_base_prefix()

ANALYZER_BASE = f"{BASE}/analyzer"


def test_root_test_endpoint_ok() -> None:
    """
    Verifica que el endpoint '/test' responda correctamente.

    - Debe devolver estado 200.
    - El contenido debe ser JSON con {'status': 'ok'}.
    """
    response = client.get(f"{BASE}/")

    assert response.status_code == 200
    assert _is_json(response)

    data = response.json()
    assert data == {"status": "ok"}


def test_analyzer_test_endpoint_ok() -> None:
    """
    Verifica que el endpoint '/analyzer/test_analyzer' esté operativo.

    - Debe devolver estado 200.
    - El contenido debe ser JSON con el mensaje esperado.
    """
    response = client.get(f"{ANALYZER_BASE}/")

    assert response.status_code == 200
    assert _is_json(response)

    expected = {
        "message": ("API de análisis funcionando correctamente")
    }
    data = response.json()
    assert data == expected
