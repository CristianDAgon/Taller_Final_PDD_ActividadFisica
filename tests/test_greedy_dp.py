"""
TEST DE FLUJO COMPLETO: Algoritmos Voraz y Dinámico

Este archivo valida que la gramática, el parser y el transformer funcionan correctamente
para pseudocódigo de algoritmos reales.

Incluye:
  - Selección de Actividades (Voraz)
  - Fibonacci DP (Dinámico)
"""

import sys
import os

# Ajustar path si es necesario
if os.path.exists('app/parsing'):
    sys.path.insert(0, 'app')

from parsing.parser import PseudocodeParser
from parsing.transformer import PseudocodeTransformer
from parsing.ast_nodes import *

# ===========================================================
# UTILIDAD PARA MOSTRAR AST
# ===========================================================

def show_ast_summary(ast):
    print("\n📦 Objeto raíz:")
    print(f"   - Tipo: {type(ast).__name__}")
    print(f"   - Clases definidas: {len(ast.classes)}")
    print()

    algo = ast.algorithm
    print("📦 Algoritmo principal:")
    print(f"   - Subrutinas: {len(algo.subroutines)}")
    print(f"   - Main: {type(algo.main).__name__}")
    print(f"   - Sentencias en main: {len(algo.main.body)}")
    print()

# ===========================================================
# PASO 1: CREAR EL PARSER Y TRANSFORMER
# ===========================================================

print("="*70)
print("🧩 INICIALIZACIÓN")
print("="*70)

parser = PseudocodeParser()
transformer = PseudocodeTransformer()

print("✅ Parser y Transformer creados correctamente\n")

# ===========================================================
# PASO 2: ALGORITMO VORAZ
# ===========================================================

print("="*70)
print("🚀 PRUEBA 1: ALGORITMO VORAZ - Selección de Actividades")
print("="*70)

greedy_code = """
seleccionActividades(inicio, fin, n)
begin
    seleccionadas[100]
    contador := 1
    seleccionadas[1] := 1
    j := 1

    for i := 2 to n do
    begin
        if (inicio[i] >= fin[j]) then
        begin
            contador := contador + 1
            seleccionadas[contador] := i
            j := i
        end
    end

    return contador
end

begin
    inicio[6]
    fin[6]
    total := seleccionActividades(inicio, fin, 6)
end
"""

print("📝 Pseudocódigo Voraz:\n")
print(greedy_code)

print("\n📥 Parseando...")
tree = parser.parse(greedy_code)
print("✅ Árbol de Lark generado con éxito\n")
print(tree.pretty())

print("\n🔄 Transformando a objetos Python (AST)...")
ast = transformer.transform(tree)
print("✅ AST generado correctamente")
show_ast_summary(ast)
print_ast(ast)
print()

# ===========================================================
# PASO 3: ALGORITMO DINÁMICO
# ===========================================================

print("="*70)
print("⚙️  PRUEBA 2: ALGORITMO DINÁMICO - Fibonacci DP")
print("="*70)

dp_code = """
fibonacciDP(n)
begin
    dp[100]

    for i := 0 to n do
    begin
        if (i = 0) then
        begin
            dp[i] := 0
        end
        else
        begin
            if (i = 1) then
            begin
                dp[i] := 1
            end
            else
            begin
                dp[i] := dp[i-1] + dp[i-2]
            end
        end
    end

    return dp[n]
end

begin
    resultado := fibonacciDP(10)
end
"""

print("📝 Pseudocódigo Dinámico:\n")
print(dp_code)

print("\n📥 Parseando...")
tree2 = parser.parse(dp_code)
print("✅ Árbol de Lark generado con éxito\n")
print(tree2.pretty())

print("\n🔄 Transformando a objetos Python (AST)...")
ast2 = transformer.transform(tree2)
print("✅ AST generado correctamente")
show_ast_summary(ast2)
print_ast(ast2)
print()

# ===========================================================
# RESUMEN FINAL
# ===========================================================

print("="*70)
print("🎉 RESULTADO FINAL DE LAS PRUEBAS")
print("="*70)
print("""
✅ Ambos algoritmos fueron parseados y transformados correctamente.
✅ La gramática reconoce estructuras de FOR, IF, asignaciones, arreglos y llamadas.
✅ Se generó un AST completo para análisis posterior (complejidad, tipo de algoritmo, etc.).
""")
