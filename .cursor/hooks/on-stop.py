#!/usr/bin/env python3
"""Stop hook: si hay una feature en curso e init.sh falla, pide corrección.

No imprime nada más que JSON por stdout. El diagnóstico va a stderr.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CURRENT = ROOT / "progress" / "current.md"


def emit(payload: dict) -> None:
    sys.stdout.write(json.dumps(payload, ensure_ascii=False))
    raise SystemExit(0)


def main() -> None:
    raw = sys.stdin.read()
    try:
        event = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        emit({})
        return

    if event.get("status") != "completed":
        emit({})
        return

    try:
        text = CURRENT.read_text(encoding="utf-8")
    except OSError:
        emit({})
        return

    if any(line.strip() == "Feature en curso: ninguna" for line in text.splitlines()):
        emit({})
        return

    result = subprocess.run(
        ["./init.sh"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        emit({})
        return

    tail = "\n".join((result.stdout + "\n" + result.stderr).splitlines()[-30:])
    print(tail, file=sys.stderr)
    emit(
        {
            "followup_message": (
                "init.sh falló con una feature en curso. "
                "No marques la feature como done. Corrige el fallo dentro del alcance "
                "o deja la feature en blocked con el error en progress/current.md.\n\n"
                + tail
            )
        }
    )


if __name__ == "__main__":
    main()
