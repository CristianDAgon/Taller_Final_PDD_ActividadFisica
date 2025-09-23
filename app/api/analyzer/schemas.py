from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class AnalyzerRequest(BaseModel):
    text: str
    want_diagram: bool = False

class Bound(BaseModel):
    big_o: str
    big_omega: str
    big_theta: Optional[str] = None
    strong_bounds: Optional[str] = None

class Step(BaseModel):
    description: str

class AnalyzerResponse(BaseModel):
    normalized_pseudocode: str
    bounds: Bound
    reasoning: List[Step]
    artifacts: Optional[Dict[str, Any]] = None
