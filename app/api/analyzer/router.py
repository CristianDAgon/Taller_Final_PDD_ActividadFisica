from fastapi import APIRouter, HTTPException
from app.api.analyzer.schemas import AnalyzerRequest, AnalyzerResponse, Bound, Step
from app.parsing.parser import parse_pseudocode
from app.analysis.estimator import estimate_complexity

router = APIRouter()

@router.post("/analyze", response_model=AnalyzerResponse)
def analyze(req: AnalyzerRequest):
    try:
        ast = parse_pseudocode(req.text)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error de sintaxis: {e}")

    result = estimate_complexity(ast, with_diagram=req.want_diagram)

    return AnalyzerResponse(
        normalized_pseudocode=req.text,
        bounds=Bound(**result["bounds"]),
        reasoning=[Step(description=s) for s in result["steps"]],
        artifacts=result.get("artifacts", {}),
    )
