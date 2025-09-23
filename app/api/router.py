# Este enroutador 'api_router' sirve como punto central para agregar routers por feature.
# Por ahora, solo incluye una ruta de salud ('/health') para verificar que el servidor corre.

from fastapi import APIRouter

api_router = APIRouter()

@api_router.get("/health")
def health_check():
    """
    Endpoint mínimo para verificar que la API está levantada.
    - Responde con un objeto JSON simple.
    - Útil para pruebas de despliegue e integración continua.
    """
    return {"status": "ok"}
