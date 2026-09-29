#!/usr/bin/env bash
# Única transición legal hacia done. Exige veredicto APPROVED.
# init.sh se corre antes y después: la feature solo queda done si sigue en verde.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ $# -ne 1 ]]; then
  echo "Uso: ./scripts/close-feature.sh <id>" >&2
  exit 1
fi

./init.sh
python3 scripts/harness.py close "$1"
./init.sh
