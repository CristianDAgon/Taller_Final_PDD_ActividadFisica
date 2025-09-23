# Analizador de Algoritmos — Backend (Base mínima de configuración)

> Esta plantilla contiene **solo lo necesario** para que el proyecto arranque en FastAPI
> y quede listo para desarrollo colaborativo. No incluye lógica de negocio; únicamente
> estructura, configuración, dependencias y comentarios en español sobre qué va en cada carpeta.

## 1) Requisitos previos
- Python 3.10+
- Git

## 2) Instalación (desarrollo)

```bash
# Crear y activar entorno virtual (bash)
python -m venv .venv
source .venv/bin/activate

# En Windows PowerShell:
# python -m venv .venv
# .venv\Scripts\Activate.ps1

pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
```

## 3) Ejecutar servidor

```bash
# Asegúrate de estar en el raíz del proyecto
export PYTHONPATH=.
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Windows PowerShell:
# setx PYTHONPATH "."  (ejecútalo una vez y abre nueva terminal)
# uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Abre: http://localhost:8000/docs

## 4) Estructura (mínima)

```
app/
  main.py        # Punto de entrada FastAPI — monta rutas base
  api/
    router.py    # Enroutador raíz — aquí se agregan routers por feature
  core/
    config.py    # Carga de variables de entorno y settings generales
  common/
    __init__.py  # (Opcional) Utilidades compartidas (responses, exceptions, etc.)
  parsing/       # (Placeholder) Aquí irá la gramática Lark y su parser
  analysis/      # (Placeholder) Aquí irá el motor de análisis de complejidad
  storage/       # (Placeholder) Repositorios (memoria/Supabase)
  exporters/     # (Placeholder) Reportes/diagramas (si se usan)
```

## 5) Flujo colaborativo sugerido (Git)
- Rama por feature: `feat/grammar-lark`, `feat/analysis-estimator`, etc.
- Commits pequeños y descriptivos (usa `ruff/black/isort/mypy` antes de PR).
- Pull Request con revisión entre pares.
- Merge a `main` solo mediante PR.

## 6) Siguientes pasos (cuando empieces la lógica)
- Define tu gramática en `app/parsing/grammar/` y el parser con Lark.
- Implementa el AST y el estimador en `app/analysis/`.
- Crea routers por feature en `app/api/` y conéctalos desde `app/api/router.py`.
- Si vas a usar Supabase, crea un cliente en `app/core/` y repos en `app/storage/`.
```

