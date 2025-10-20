"""
Punto de entrada principal de la aplicación FastAPI.

Responsabilidades:
- Crear la instancia global de FastAPI.
- Montar el router base de la API.
- Permitir que Uvicorn levante la aplicación (app:module).
"""

from fastapi import FastAPI
from app.api.router import api_router


def create_app() -> FastAPI:
    """
    Crea y configura la instancia principal de FastAPI.

    Returns:
        FastAPI: Objeto de aplicación configurado con sus rutas y metadatos.
    """
    app = FastAPI(title="Analizador de Algoritmos (Base mínima)")
    app.include_router(api_router, prefix="/api")
    return app


# Instancia global que Uvicorn utiliza para ejecutar el servidor (app:module)
app = create_app()
