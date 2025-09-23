from lark import Transformer, v_args
from app.parsing.ast_nodes import Program, Assign

@v_args(inline=True)
class PseudocodeTransformer(Transformer):
    def program(self, *stmts):
        return Program(statements=list(stmts))

    def assign_stmt(self, name, value):
        # Lark tokens -> Python str/int
        target = str(name)
        try:
            val = int(value)
        except Exception:
            val = str(value)
        return Assign(target=target, value=val)
