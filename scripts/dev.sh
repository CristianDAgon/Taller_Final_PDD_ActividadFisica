#!/usr/bin/env bash
# Script de desarrollo: arranca la app con recarga automática
set -euo pipefail
export PYTHONPATH=.
uvicorn app.main:app --reload --host ${APP_HOST:-0.0.0.0} --port ${APP_PORT:-8000}
