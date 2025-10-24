"""
Clasificador de Algoritmos - VERSIÓN CORREGIDA

Módulo para detectar el tipo de algoritmo a partir del AST:
- ITERATIVE: Solo usa loops (FOR, WHILE, REPEAT)
- RECURSIVE: Contiene llamadas recursivas (en cualquier expresión)
- HYBRID: Combina loops y recursión
- SIMPLE: Sin loops ni recursión (solo operaciones básicas)
"""

from app.parsing.ast_nodes import *


class AlgorithmClassifier:
    """
    Clasifica algoritmos según su estructura de control
    """
    
    def __init__(self, ast):
        """
        Args:
            ast: Objeto Program del transformer
        """
        self.ast = ast
    
    def classify_all(self):
        """
        Clasifica todas las subrutinas del programa
        
        Returns:
            dict: {
                'main': tipo,
                'subroutines': [
                    {'name': str, 'type': str, 'details': dict}
                ]
            }
        """
        results = {
            'main': self._classify_main(),
            'subroutines': []
        }
        
        for sub in self.ast.algorithm.subroutines:
            classification = self.classify_subroutine(sub)
            results['subroutines'].append(classification)
        
        return results
    
    def classify_subroutine(self, subroutine):
        """
        Clasifica una subrutina específica
        
        Args:
            subroutine: Objeto Subroutine del AST
        
        Returns:
            dict: {
                'name': str,
                'type': 'ITERATIVE' | 'RECURSIVE' | 'HYBRID' | 'SIMPLE',
                'details': {
                    'has_loops': bool,
                    'has_recursion': bool,
                    'loop_count': int,
                    'recursive_calls': int,
                    'max_nesting': int
                }
            }
        """
        # Analizar características
        has_loops, loop_info = self._has_loops(subroutine.body)
        has_recursion, recursion_info = self._has_recursive_calls(
            subroutine.name, 
            subroutine.body
        )
        
        # Determinar tipo
        if has_recursion and has_loops:
            algo_type = "HYBRID"
        elif has_recursion:
            algo_type = "RECURSIVE"
        elif has_loops:
            algo_type = "ITERATIVE"
        else:
            algo_type = "SIMPLE"
        
        return {
            'name': subroutine.name,
            'type': algo_type,
            'parameters': [p.name for p in subroutine.parameters],
            'details': {
                'has_loops': has_loops,
                'has_recursion': has_recursion,
                'loop_count': loop_info['count'],
                'loop_types': loop_info['types'],
                'max_nesting': loop_info['max_nesting'],
                'recursive_calls': recursion_info['count'],
                'recursive_positions': recursion_info['positions']
            }
        }
    
    def _classify_main(self):
        """
        Clasifica el algoritmo principal (begin...end)
        """
        has_loops, loop_info = self._has_loops(self.ast.algorithm.main.body)
        
        if has_loops:
            return {
                'type': 'ITERATIVE',
                'loop_count': loop_info['count'],
                'max_nesting': loop_info['max_nesting']
            }
        else:
            return {
                'type': 'SIMPLE',
                'loop_count': 0
            }
    
    # ========================================================================
    # DETECCIÓN DE LOOPS
    # ========================================================================
    
    def _has_loops(self, statements, current_depth=0):
        """
        Detecta si hay loops y cuenta información sobre ellos
        
        Args:
            statements: Lista de statements a analizar
            current_depth: Profundidad actual de anidamiento
        
        Returns:
            tuple: (has_loops: bool, info: dict)
        """
        loop_count = 0
        max_nesting = current_depth
        loop_types = set()
        
        for stmt in statements:
            # Detectar tipo de loop
            if isinstance(stmt, ForLoop):
                loop_count += 1
                loop_types.add('FOR')
                # Analizar recursivamente el body del loop
                _, nested_info = self._has_loops(
                    stmt.body.statements, 
                    current_depth + 1
                )
                loop_count += nested_info['count']
                max_nesting = max(max_nesting, nested_info['max_nesting'])
                loop_types.update(nested_info['types'])
                
            elif isinstance(stmt, WhileLoop):
                loop_count += 1
                loop_types.add('WHILE')
                _, nested_info = self._has_loops(
                    stmt.body.statements, 
                    current_depth + 1
                )
                loop_count += nested_info['count']
                max_nesting = max(max_nesting, nested_info['max_nesting'])
                loop_types.update(nested_info['types'])
                
            elif isinstance(stmt, RepeatLoop):
                loop_count += 1
                loop_types.add('REPEAT')
                _, nested_info = self._has_loops(
                    stmt.statements, 
                    current_depth + 1
                )
                loop_count += nested_info['count']
                max_nesting = max(max_nesting, nested_info['max_nesting'])
                loop_types.update(nested_info['types'])
            
            # Revisar dentro de condicionales
            elif isinstance(stmt, IfStatement):
                _, then_info = self._has_loops(stmt.then_block.statements, current_depth)
                loop_count += then_info['count']
                max_nesting = max(max_nesting, then_info['max_nesting'])
                loop_types.update(then_info['types'])
                
                if stmt.else_block:
                    _, else_info = self._has_loops(stmt.else_block.statements, current_depth)
                    loop_count += else_info['count']
                    max_nesting = max(max_nesting, else_info['max_nesting'])
                    loop_types.update(else_info['types'])
        
        has_loops = loop_count > 0
        
        info = {
            'count': loop_count,
            'max_nesting': max_nesting,
            'types': list(loop_types)
        }
        
        return has_loops, info
    
    # ========================================================================
    # DETECCIÓN DE RECURSIÓN (CORREGIDO)
    # ========================================================================
    
    def _has_recursive_calls(self, function_name, statements, position="body"):
        """
        Detecta llamadas recursivas en CUALQUIER forma:
        - call factorial(n)
        - return factorial(n-1)
        - x := factorial(n-1)
        - if (factorial(n) > 0)
        
        Args:
            function_name: Nombre de la función a buscar
            statements: Lista de statements a analizar
            position: Posición en el código (para tracking)
        
        Returns:
            tuple: (has_recursion: bool, info: dict)
        """
        recursive_count = 0
        positions = []
        
        for i, stmt in enumerate(statements):
            # 1. CALL directo (call factorial(n))
            if isinstance(stmt, CallStatement):
                if stmt.function_name == function_name:
                    recursive_count += 1
                    positions.append(f"{position}[{i}].call")
            
            # 2. RETURN con recursión (return factorial(n-1))
            elif isinstance(stmt, ReturnStatement):
                if self._expression_contains_call(stmt.value, function_name):
                    recursive_count += 1
                    positions.append(f"{position}[{i}].return")
            
            # 3. ASSIGNMENT con recursión (x := factorial(n-1))
            elif isinstance(stmt, Assignment):
                if self._expression_contains_call(stmt.value, function_name):
                    recursive_count += 1
                    positions.append(f"{position}[{i}].assignment")
            
            # 4. Buscar en loops
            elif isinstance(stmt, ForLoop):
                _, nested_info = self._has_recursive_calls(
                    function_name, 
                    stmt.body.statements,
                    f"{position}[{i}].for_body"
                )
                recursive_count += nested_info['count']
                positions.extend(nested_info['positions'])
                
            elif isinstance(stmt, WhileLoop):
                _, nested_info = self._has_recursive_calls(
                    function_name, 
                    stmt.body.statements,
                    f"{position}[{i}].while_body"
                )
                recursive_count += nested_info['count']
                positions.extend(nested_info['positions'])
                
            elif isinstance(stmt, RepeatLoop):
                _, nested_info = self._has_recursive_calls(
                    function_name, 
                    stmt.statements,
                    f"{position}[{i}].repeat_body"
                )
                recursive_count += nested_info['count']
                positions.extend(nested_info['positions'])
            
            # 5. Buscar en condicionales (condición + bloques)
            elif isinstance(stmt, IfStatement):
                # Revisar la condición del IF (if (factorial(n) > 0))
                if self._expression_contains_call(stmt.condition, function_name):
                    recursive_count += 1
                    positions.append(f"{position}[{i}].if_condition")
                
                # Revisar bloque THEN
                _, then_info = self._has_recursive_calls(
                    function_name, 
                    stmt.then_block.statements,
                    f"{position}[{i}].then"
                )
                recursive_count += then_info['count']
                positions.extend(then_info['positions'])
                
                # Revisar bloque ELSE
                if stmt.else_block:
                    _, else_info = self._has_recursive_calls(
                        function_name, 
                        stmt.else_block.statements,
                        f"{position}[{i}].else"
                    )
                    recursive_count += else_info['count']
                    positions.extend(else_info['positions'])
        
        has_recursion = recursive_count > 0
        
        info = {
            'count': recursive_count,
            'positions': positions
        }
        
        return has_recursion, info
    
    def _expression_contains_call(self, expr, function_name):
        """
        Verifica RECURSIVAMENTE si una expresión contiene una llamada a la función
        
        Busca en:
        - FunctionCall directo
        - BinaryOp (left y right)
        - UnaryOp (operand)
        - Argumentos de funciones anidadas
        """
        if expr is None:
            return False
        
        # FunctionCall directo
        if isinstance(expr, FunctionCall):
            if expr.function_name == function_name:
                return True
            # Revisar argumentos recursivamente
            for arg in expr.arguments:
                if self._expression_contains_call(arg, function_name):
                    return True
        
        # BinaryOp: revisar left y right
        elif isinstance(expr, BinaryOp):
            if self._expression_contains_call(expr.left, function_name):
                return True
            if self._expression_contains_call(expr.right, function_name):
                return True
        
        # UnaryOp: revisar operand
        elif isinstance(expr, UnaryOp):
            if self._expression_contains_call(expr.operand, function_name):
                return True
        
        # Variable con índices que pueden contener llamadas: A[factorial(n)]
        elif isinstance(expr, Variable):
            if expr.indices:
                for index in expr.indices:
                    if self._expression_contains_call(index, function_name):
                        return True
        
        # Ceiling/Floor
        elif isinstance(expr, (Ceiling, Floor)):
            if self._expression_contains_call(expr.expression, function_name):
                return True
        
        return False


# ============================================================================
# FUNCIÓN AUXILIAR PARA IMPRIMIR RESULTADOS
# ============================================================================

def print_classification(classification):
    """
    Imprime de forma legible el resultado de la clasificación
    """
    print("\n" + "="*70)
    print("📊 CLASIFICACIÓN DE ALGORITMOS")
    print("="*70)
    
    # Main
    if 'main' in classification:
        print("\n🏠 ALGORITMO PRINCIPAL:")
        print(f"   Tipo: {classification['main']['type']}")
        if classification['main']['type'] == 'ITERATIVE':
            print(f"   Loops: {classification['main']['loop_count']}")
            print(f"   Anidamiento máximo: {classification['main']['max_nesting']}")
    
    # Subrutinas
    if 'subroutines' in classification and classification['subroutines']:
        print("\n📦 SUBRUTINAS:")
        for sub in classification['subroutines']:
            print(f"\n   🔹 {sub['name']}({', '.join(sub['parameters'])})")
            print(f"      Tipo: {sub['type']}")
            
            details = sub['details']
            if details['has_loops']:
                print(f"      ✓ Loops: {details['loop_count']} ({', '.join(details['loop_types'])})")
                print(f"      ✓ Anidamiento: {details['max_nesting']} niveles")
            
            if details['has_recursion']:
                print(f"      ✓ Llamadas recursivas: {details['recursive_calls']}")
                print(f"      ✓ Posiciones: {', '.join(details['recursive_positions'])}")
    
    print("\n" + "="*70)