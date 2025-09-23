from dataclasses import dataclass
from typing import List, Union, Optional

@dataclass
class Program:
    statements: List["Stmt"]

@dataclass
class Assign:
    target: str
    value: Union[str, int]

Stmt = Assign  # por ahora
