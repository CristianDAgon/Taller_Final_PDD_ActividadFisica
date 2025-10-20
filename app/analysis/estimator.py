"""
Módulo de estimación de complejidad algorítmica.

Define funciones para analizar un AST y devolver los límites de
complejidad temporal estimados.
"""

from app.analysis.models import AnalysisResultModel
from app.parsing.ast_nodes import Program, Assignment


def estimate_complexity(ast: Program, with_diagram: bool = False) -> dict:
    """
    Estima la complejidad temporal de un programa en forma de AST.

    Actualmente se implementa un análisis básico:
    - Cuenta el número de asignaciones en el bloque principal.
    - Asume costo constante por asignación.
    - Retorna complejidad O(n).

    Args:
        ast (Program): Árbol sintáctico abstracto del pseudocódigo.
        with_diagram (bool): Si es True, incluirá datos para diagrama.

    Returns:
        dict: Resultado del análisis con cotas y pasos de razonamiento.
    """
    stmts = getattr(ast, "statements", [])
    num_assigns = sum(
        1
        for stmt in stmts
        if isinstance(stmt, Assignment)
    )

    steps = [
        f"Se detectaron {num_assigns} asignaciones en el bloque principal.",
        (
            "Asumiendo costo constante por asignación, el costo total es "
            "proporcional a n (número de sentencias)."
        ),
    ]

    bounds = {
        "big_o": "O(n)",
        "big_omega": "Ω(n)",
        "big_theta": "Θ(n)",
        "strong_bounds": None,
    }

    result = AnalysisResultModel(
        bounds=bounds,
        steps=steps,
        artifacts={},
    )
    return result.dict()
