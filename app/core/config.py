# Este módulo centraliza la configuración de la app.
# Lee variables de entorno (por ejemplo desde .env) y las expone como 'settings'.
# Aquí también puedes inicializar clientes compartidos (p. ej., Supabase) cuando los vayas a usar.

import os
from pydantic import BaseModel
from dotenv import load_dotenv

# Carga variables desde .env si existe
load_dotenv()

class Settings(BaseModel):
    app_name: str = os.getenv("APP_NAME", "Analizador de Algoritmos")
    env: str = os.getenv("APP_ENV", "development")
    host: str = os.getenv("APP_HOST", "0.0.0.0")
    port: int = int(os.getenv("APP_PORT", "8000"))
    # Placeholders para tecnologías futuras (sin inicializarlas aquí)
    supabase_url: str | None = os.getenv("SUPABASE_URL")
    supabase_key: str | None = os.getenv("SUPABASE_KEY")
    enable_diagrams: bool = os.getenv("ENABLE_DIAGRAMS", "false").lower() == "true"

# Instancia única de configuración
settings = Settings()
