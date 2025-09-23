# Script de desarrollo para Windows PowerShell
$env:PYTHONPATH = "."
$host = $env:APP_HOST
$port = $env:APP_PORT
if (-not $host) { $host = "0.0.0.0" }
if (-not $port) { $port = "8000" }
uvicorn app.main:app --reload --host $host --port $port
