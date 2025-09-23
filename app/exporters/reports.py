from pathlib import Path
from typing import Dict, Any

def build_html_report(pseudocode: str, result: Dict[str, Any]):
    # Crea un HTML mínimo en /mnt/data para pruebas
    out = Path('/mnt/data/analysis_report.html')
    html = f"""
    <html><body>
    <h1>Reporte de Análisis</h1>
    <h2>Pseudocódigo</h2>
    <pre>{pseudocode}</pre>
    <h2>Resultados</h2>
    <pre>{result}</pre>
    </body></html>
    """
    out.write_text(html, encoding='utf-8')
    return type("Report", (), {"path": str(out)})
