"""
Router raíz de la API.

Punto central para agregar routers por feature.
"""

from fastapi import APIRouter
from app.api.analyzer.router import router as analyzer_router

__all__ = ["api_router"]

api_router = APIRouter()

# Registrar routers por dominio/feature
api_router.include_router(
    analyzer_router,
    prefix="/analyzer",
    tags=["analyzer"],
)


@api_router.get("/")
def test_check() -> dict[str, str]:
    """
    Endpoint mínimo para verificar que la API está levantada.

    Returns:
        dict[str, str]: Objeto JSON simple con la clave "status".
    """
    return {"status": "ok"}
