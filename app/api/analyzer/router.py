"""
Módulo del enrutador del analizador.

Expone los endpoints para analizar pseudocódigo y verificar
el estado del servicio.
"""

from fastapi import APIRouter, HTTPException
from app.api.analyzer.schemas import (
    AnalyzerRequest,
    AnalyzerResponse,
    Bound,
    Step,
)
from app.parsing.parser import parse_pseudocode
from app.analysis.estimator import estimate_complexity

router = APIRouter()


@router.post("/analyze", response_model=AnalyzerResponse)
def analyze(req: AnalyzerRequest) -> AnalyzerResponse:
    """
    Analiza el pseudocódigo recibido y estima su complejidad temporal.

    Args:
        req (AnalyzerRequest): Objeto con el texto del pseudocódigo y la
            opción de generar diagrama.

    Raises:
        HTTPException: Si ocurre un error de sintaxis durante el análisis.

    Returns:
        AnalyzerResponse: Resultado con límites, pasos de razonamiento
        y artefactos generados.
    """
    try:
        ast = parse_pseudocode(req.text)
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Error de sintaxis: {exc}",
        ) from exc

    result = estimate_complexity(ast, with_diagram=req.want_diagram)

    return AnalyzerResponse(
        normalized_pseudocode=req.text,
        bounds=Bound(**result["bounds"]),
        reasoning=[Step(description=s) for s in result["steps"]],
        artifacts=result.get("artifacts", {}),
    )


@router.get("/")
def test() -> dict[str, str]:
    """
    Verifica que la API del analizador esté funcionando correctamente.

    Returns:
        dict[str, str]: Mensaje de confirmación del servicio.
    """
    return {"message": "API de análisis funcionando correctamente"}
