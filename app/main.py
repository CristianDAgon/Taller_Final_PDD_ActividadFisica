# Este archivo es el punto de entrada de FastAPI.
# Su responsabilidad es crear la instancia de la aplicación y montar las rutas base.

from fastapi import FastAPI
from app.api.router import api_router

def create_app() -> FastAPI:
    # Crea la aplicación principal. Aquí puedes añadir middlewares, eventos, etc.
    app = FastAPI(title="Analizador de Algoritmos (Base mínima)")
    # Monta el router raíz de la API bajo /api
    app.include_router(api_router, prefix="/api")
    return app

# Instancia global que uvicorn utiliza para levantar el servidor (app:module)
app = create_app()
