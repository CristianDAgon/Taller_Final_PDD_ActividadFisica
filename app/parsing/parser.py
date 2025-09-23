from lark import Lark
from pathlib import Path
from app.parsing.transformer import PseudocodeTransformer

_GRAMMAR = (Path(__file__).parent / "grammar" / "pseudocode.lark").read_text(encoding="utf-8")
_lark = Lark(_GRAMMAR, start="program", parser="lalr")

def parse_pseudocode(text: str):
    tree = _lark.parse(text)
    return PseudocodeTransformer().transform(tree)
