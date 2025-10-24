"""
TEST DE DEBUG: Verificar qué retorna el transformer
"""

from app.parsing.parser import PseudocodeParser
from app.parsing.transformer import Transformer

parser = PseudocodeParser()
transformer = Transformer()

code = """
factorial(n)
begin
    if (n = 0) then
    begin
        return 1
    end
    else
    begin
        return n * factorial(n - 1)
    end
end

begin
    resultado := factorial(5)
end
"""

print("1. Parseando código...")
tree = parser.parse(code)
print(f"   Tipo de tree: {type(tree)}")
print(f"   tree = {tree}")
print()

print("2. Transformando a AST...")
ast = transformer.transform(tree)
print(f"   Tipo de ast: {type(ast)}")
print(f"   ast = {ast}")
print()

print("3. Verificando estructura del AST...")
print(f"   ¿Tiene atributo 'algorithm'? {hasattr(ast, 'algorithm')}")

if hasattr(ast, 'algorithm'):
    print(f"   ast.algorithm = {ast.algorithm}")
    print(f"   ¿Tiene atributo 'main'? {hasattr(ast.algorithm, 'main')}")
    
    if hasattr(ast.algorithm, 'main'):
        print(f"   ast.algorithm.main = {ast.algorithm.main}")
        print(f"   Tipo: {type(ast.algorithm.main)}")
        print(f"   ¿Tiene atributo 'body'? {hasattr(ast.algorithm.main, 'body')}")
        
        if hasattr(ast.algorithm.main, 'body'):
            print(f"   ast.algorithm.main.body = {ast.algorithm.main.body}")
            print(f"   Cantidad de statements: {len(ast.algorithm.main.body)}")
else:
    print("   ❌ ERROR: El AST no tiene atributo 'algorithm'")
    print(f"   Atributos disponibles: {[a for a in dir(ast) if not a.startswith('_')]}")