# Analizador de Algoritmos — Backend (FastAPI)

> Proyecto base para análisis y experimentación algorítmica con **FastAPI**.  
> Incluye configuración mínima, entorno virtual, variables de entorno, dependencias y estructura modular lista para extender.

---

## ⚙️ 1) Requisitos previos

Antes de comenzar, asegúrate de tener instalado:

- **Python 3.10+**
- **Git**
- (Opcional pero recomendado) **VS Code** con la extensión _Python_ y _Pylance_
- (Opcional) **Postman** o **cURL** para probar los endpoints

---

## 🚀 2) Instalación y configuración del entorno

### Linux / macOS / Git Bash

```bash
# Clonar el repositorio
git clone <URL_DEL_REPO>
cd algorithm-analysis

# Crear entorno virtual
python -m venv .venv

# Activar entorno
source .venv/Scripts/activate  # en Git Bash (Windows)
# o
source .venv/bin/activate      # en Linux/Mac

# Desactivar entorno
deactivate

# Actualizar pip e instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# Crear archivo de entorno
cp .env.example .env
```

### Windows PowerShell

```bash
# Clonar el repositorio
git clone <URL_DEL_REPO>
cd algorithm-analysis

# Crear y activar entorno virtual
python -m venv .venv
.venv\Scripts\Activate.ps1

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# Copiar archivo de entorno
copy .env.example .env
```

---

## ▶️ 3) Ejecutar el servidor FastAPI

Asegúrate de estar en la raíz del proyecto (donde está `app/` y `.venv`).

### Linux / Git Bash

```bash
# Asegúrate de estar en el raíz del proyecto
export PYTHONPATH=.
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Windows PowerShell

```bash
setx PYTHONPATH "."
# Cierra y vuelve a abrir la terminal para aplicar el cambio
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

El servidor quedará corriendo en:

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

---

## 🧩 4) Estructura del proyecto

```
algorithm-analysis/
│
├── app/
│   ├── main.py          # Punto de entrada de FastAPI (crea instancia y monta rutas)
│   ├── api/
│   │   └── router.py    # Router raíz (se importan las rutas por módulo)
│   ├── core/
│   │   └── config.py    # Configuración y carga de variables de entorno
│   ├── common/          # Utilidades compartidas (respuestas, excepciones, middlewares)
│   ├── parsing/         # (Placeholder) Gramáticas Lark y parser de entrada
│   ├── analysis/        # (Placeholder) Motor de análisis de complejidad
│   ├── storage/         # (Placeholder) Repositorios (memoria o Supabase)
│   └── exporters/       # (Placeholder) Reportes, gráficas o diagramas
│
├── .env.example          # Variables de entorno base
├── requirements.txt      # Dependencias del proyecto
├── README.md             # Este archivo
└── .gitignore
```

---

## 🤝 5) Flujo de trabajo colaborativo (Git)

- Crea una rama por feature:  
  `feat/parser-lark`, `feat/complexity-engine`, `fix/config-loader`, etc.
- Usa commits pequeños y descriptivos.
- Aplica linters y formateadores antes de hacer push (`ruff`, `black`, `isort`, `mypy`).
- Haz _Pull Requests_ para revisión por pares.
- Solo mergea a `main` mediante PR aprobado.

---

## 🧠 6) Siguientes pasos (cuando comiences desarrollo)

1. **Definir gramática:**  
   Crea la gramática Lark en `app/parsing/grammar/`.
2. **Implementar parser:**  
   Desarrolla el parser sintáctico/semántico en `app/parsing/`.
3. **Diseñar analizador:**  
   Construye el estimador de complejidad en `app/analysis/`.
4. **Exponer endpoints:**  
   Define rutas específicas dentro de `app/api/` y conéctalas en `router.py`.
5. **Persistencia opcional:**  
   Si usas Supabase, configura conexión y repos en `app/storage/`.
6. **Visualización:**  
   Agrega reportes o diagramas en `app/exporters/`.

---

## 🧪 7) Pruebas rápidas

Para probar el servidor:

```bash
curl http://127.0.0.1:8000/api/test
```

Si devuelve `{"ok": true}`, el backend está funcionando correctamente.

---

## 🧰 8) Herramientas útiles

| Propósito       | Herramienta | Comando                         |
| --------------- | ----------- | ------------------------------- |
| Linter          | ruff        | `ruff check .`                  |
| Formato         | black       | `black .`                       |
| Orden imports   | isort       | `isort .`                       |
| Tipos estáticos | mypy        | `mypy app/`                     |
| Servidor local  | uvicorn     | `uvicorn app.main:app --reload` |
