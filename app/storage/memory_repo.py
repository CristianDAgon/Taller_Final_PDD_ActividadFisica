import uuid
from typing import Dict, Any

_DB: Dict[str, Dict[str, Any]] = {}


def save_analysis(payload: Dict[str, Any]) -> str:
    id_ = str(uuid.uuid4())
    _DB[id_] = payload
    return id_


def get_analysis(id_: str) -> Dict[str, Any]:
    return _DB[id_]


def list_examples() -> list[str]:
    return ["sumatoria", "burbuja", "factorial", "mergesort"]
