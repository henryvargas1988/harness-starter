#!/usr/bin/env bash
# Puerta humana del carril sdd. El agente no la invoca por su cuenta.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
exec python3 scripts/harness.py approve-spec "$@"
