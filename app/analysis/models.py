"""
Modelo de datos para los resultados del análisis de complejidad.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class AnalysisResultModel(BaseModel):
    """
    Representa el resultado del análisis de complejidad de un programa.

    Attributes:
        bounds (Dict[str, Optional[str]]): Diccionario con las cotas
            teóricas de complejidad (O, Ω, Θ, etc.).
        steps (List[str]): Lista de pasos o razonamientos usados
            durante el análisis.
        artifacts (Dict[str, Any]): Elementos adicionales generados
            por el análisis (p. ej. diagramas).
    """

    bounds: Dict[str, Optional[str]]
    steps: List[str]
    artifacts: Dict[str, Any] = {}
