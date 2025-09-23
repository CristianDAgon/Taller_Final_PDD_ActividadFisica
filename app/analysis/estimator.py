from app.analysis.models import AnalysisResultModel
from app.parsing.ast_nodes import Program, Assign

def estimate_complexity(ast: Program, with_diagram: bool = False):
    # Placeholder para que arranque: cuenta asignaciones y devuelve O(n)
    num_assigns = sum(1 for _ in ast.statements if isinstance(_, Assign))
    steps = [
        f"Se detectaron {num_assigns} asignaciones en el bloque principal.",
        "Asumiendo costo constante por asignación, el costo total es proporcional a n (número de sentencias)."
    ]
    bounds = {"big_o": "O(n)", "big_omega": "Ω(n)", "big_theta": "Θ(n)", "strong_bounds": None}
    result = AnalysisResultModel(bounds=bounds, steps=steps, artifacts={})
    return result.dict()
