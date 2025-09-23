from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class AnalysisResultModel(BaseModel):
    bounds: Dict[str, Optional[str]]  # big_o, big_omega, big_theta, strong_bounds
    steps: List[str]
    artifacts: Dict[str, Any] = {}
