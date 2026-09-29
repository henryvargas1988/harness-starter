#!/usr/bin/env bash
# Verificación del arnés y, si existe, de la aplicación.
# Se ejecuta al empezar una sesión y antes de cerrar una feature.
# Si falla, no se avanza y no se marca nada como done.

set -u

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

ok() { printf "${GREEN}[OK]${NC} %s\n" "$1"; }
warn() { printf "${YELLOW}[WARN]${NC} %s\n" "$1"; }
fail() { printf "${RED}[FAIL]${NC} %s\n" "$1"; }

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
EXIT_CODE=0

echo "── 1. Entorno ─────────────────────────────────────────"

if ! command -v python3 >/dev/null 2>&1; then
  fail "python3 no está instalado (el arnés lo usa para validar feature_list.json)"
  exit 1
fi
ok "python3 -> $(python3 --version)"

echo ""
echo "── 2. Invariantes del arnés ───────────────────────────"

if python3 scripts/harness.py check; then
  ok "Estado de features coherente"
else
  fail "El arnés no está en un estado válido"
  EXIT_CODE=1
fi

echo ""
echo "── 3. Verificación de la aplicación ───────────────────"

run_and_capture() {
  if "$@"; then
    ok "Suite de aplicación en verde ($1)"
  else
    fail "Suite de aplicación en rojo ($1)"
    EXIT_CODE=1
  fi
}

if [[ -f scripts/verify.sh ]]; then
  if [[ -x scripts/verify.sh ]]; then
    run_and_capture ./scripts/verify.sh
  else
    fail "scripts/verify.sh existe pero no es ejecutable (chmod +x scripts/verify.sh)"
    EXIT_CODE=1
  fi
elif [[ -f package.json ]]; then
  if ! command -v node >/dev/null 2>&1; then
    fail "Hay package.json pero node no está instalado"
    EXIT_CODE=1
  elif [[ -f pnpm-lock.yaml ]] && command -v pnpm >/dev/null 2>&1; then
    run_and_capture pnpm test
  elif [[ -f yarn.lock ]] && command -v yarn >/dev/null 2>&1; then
    run_and_capture yarn test
  else
    run_and_capture npm test
  fi
elif [[ -f go.mod ]]; then
  run_and_capture go test ./...
elif [[ -f Cargo.toml ]]; then
  run_and_capture cargo test
elif [[ -f pyproject.toml || -f pytest.ini || -d tests ]]; then
  if python3 -c "import pytest" >/dev/null 2>&1; then
    run_and_capture python3 -m pytest -q
  elif [[ -d tests ]]; then
    run_and_capture python3 -m unittest discover -s tests -q
  else
    warn "Hay config de Python pero no se encontró una suite ejecutable"
  fi
else
  warn "Todavía no hay suite de aplicación. Cuando exista, créala o añade scripts/verify.sh."
  ok "Arnés coherente sin suite de producto"
fi

echo ""
echo "── 4. Resumen ─────────────────────────────────────────"

if [[ "$EXIT_CODE" -eq 0 ]]; then
  ok "Entorno listo. Puedes trabajar."
else
  fail "Entorno NO listo. Resuelve los errores antes de avanzar."
fi

exit "$EXIT_CODE"
