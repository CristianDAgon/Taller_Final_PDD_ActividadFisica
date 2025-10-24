"""
TEST DEL CLASIFICADOR DE ALGORITMOS

Prueba el módulo classifier.py con diferentes tipos de algoritmos
"""

# Ajustar imports según tu estructura
from app.parsing.parser import PseudocodeParser
from app.parsing.transformer import PseudocodeTransformer
from app.analysis.classifier import AlgorithmClassifier, print_classification

parser = PseudocodeParser()
transformer = PseudocodeTransformer()

# ============================================================================
# TEST 1: ALGORITMO ITERATIVO - Cambio de Monedas (Voraz)
# ============================================================================

print("="*70)
print("TEST 1: ALGORITMO ITERATIVO (VORAZ)")
print("="*70)

code_iterative = """
cambioMonedas(monto, monedas, n)
begin
    resultado[100]
    contador := 0
    
    for i := n to 1 do
    begin
        while (monto >= monedas[i]) do
        begin
            monto := monto - monedas[i]
            resultado[contador] := monedas[i]
            contador := contador + 1
        end
    end
    
    return contador
end

begin
    monedas[5]
    cambio := cambioMonedas(63, monedas, 5)
end
"""

tree = parser.parse(code_iterative)
ast = transformer.transform(tree)

classifier = AlgorithmClassifier(ast)
result = classifier.classify_all()

print_classification(result)

print("\n✅ Esperado: ITERATIVE (FOR + WHILE anidado)")
print(f"✅ Obtenido: {result['subroutines'][0]['type']}")


# ============================================================================
# TEST 2: ALGORITMO RECURSIVO - Factorial
# ============================================================================

print("\n\n" + "="*70)
print("TEST 2: ALGORITMO RECURSIVO")
print("="*70)

code_recursive = """
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

tree = parser.parse(code_recursive)
ast = transformer.transform(tree)

classifier = AlgorithmClassifier(ast)
result = classifier.classify_all()

print_classification(result)

print("\n✅ Esperado: RECURSIVE (llamada a sí mismo)")
print(f"✅ Obtenido: {result['subroutines'][0]['type']}")


# ============================================================================
# TEST 3: ALGORITMO HÍBRIDO - Merge Sort (simplificado)
# ============================================================================

print("\n\n" + "="*70)
print("TEST 3: ALGORITMO HÍBRIDO")
print("="*70)

code_hybrid = """
mergeSort(arr, inicio, fin)
begin
    if (inicio < fin) then
    begin
        medio := (inicio + fin) div 2
        
        call mergeSort(arr, inicio, medio)
        call mergeSort(arr, medio + 1, fin)
        
        for i := inicio to fin do
        begin
            arr[i] := arr[i] + 1
        end
    end
end

begin
    datos[10]
    call mergeSort(datos, 1, 10)
end
"""

tree = parser.parse(code_hybrid)
ast = transformer.transform(tree)

classifier = AlgorithmClassifier(ast)
result = classifier.classify_all()

print_classification(result)

print("\n✅ Esperado: HYBRID (recursión + loop)")
print(f"✅ Obtenido: {result['subroutines'][0]['type']}")


# ============================================================================
# TEST 4: ALGORITMO SIMPLE - Sin loops ni recursión
# ============================================================================

print("\n\n" + "="*70)
print("TEST 4: ALGORITMO SIMPLE")
print("="*70)

code_simple = """
sumar(a, b)
begin
    resultado := a + b
    return resultado
end

begin
    total := sumar(5, 10)
end
"""

tree = parser.parse(code_simple)
ast = transformer.transform(tree)

classifier = AlgorithmClassifier(ast)
result = classifier.classify_all()

print_classification(result)

print("\n✅ Esperado: SIMPLE (solo operaciones básicas)")
print(f"✅ Obtenido: {result['subroutines'][0]['type']}")


# ============================================================================
# TEST 5: LOOPS ANIDADOS - Programación Dinámica
# ============================================================================

print("\n\n" + "="*70)
print("TEST 5: LOOPS ANIDADOS (DP)")
print("="*70)

code_nested = """
mochila(pesos, valores, n, capacidad)
begin
    dp[100]
    
    for i := 0 to n do
    begin
        for w := 0 to capacidad do
        begin
            if (i = 0) then
            begin
                dp[i] := 0
            end
            else
            begin
                dp[i] := valores[i]
            end
        end
    end
    
    return dp[n]
end

begin
    resultado := mochila(pesos, valores, 5, 10)
end
"""

tree = parser.parse(code_nested)
ast = transformer.transform(tree)

classifier = AlgorithmClassifier(ast)
result = classifier.classify_all()

print_classification(result)

print("\n✅ Esperado: ITERATIVE con anidamiento = 2")
print(f"✅ Obtenido: {result['subroutines'][0]['type']}, anidamiento = {result['subroutines'][0]['details']['max_nesting']}")


# ============================================================================
# RESUMEN
# ============================================================================

print("\n\n" + "="*70)
print("🎉 RESUMEN DE PRUEBAS")
print("="*70)
print("""
✅ El clasificador puede detectar:
   - Algoritmos ITERATIVOS (solo loops)
   - Algoritmos RECURSIVOS (llamadas a sí mismo)
   - Algoritmos HÍBRIDOS (loops + recursión)
   - Algoritmos SIMPLES (sin loops ni recursión)
   - Nivel de anidamiento de loops
   - Cantidad de llamadas recursivas
   - Tipos de loops (FOR, WHILE, REPEAT)

🚀 Siguiente paso: Implementar analizadores de complejidad específicos
""")