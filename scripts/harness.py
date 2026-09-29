#!/usr/bin/env python3
"""Invariantes y transiciones del arnés.

El agente no inventa el cierre de una feature: lo hace este script
después de un veredicto APPROVED y de una verificación en verde.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FEATURE_LIST = ROOT / "feature_list.json"
VALID_STATUS = {"pending", "spec_ready", "in_progress", "done", "blocked"}
VALID_LANE = {"fast", "sdd"}
SPEC_FILES = ("requirements.md", "design.md", "tasks.md")
REQUIRED = (
    "AGENTS.md",
    "CHECKPOINTS.md",
    "feature_list.json",
    "init.sh",
    "progress/current.md",
    "progress/history.md",
    "docs/architecture.md",
    "docs/conventions.md",
    "docs/verification.md",
    "docs/harness.md",
)


def load_features() -> dict:
    try:
        data = json.loads(FEATURE_LIST.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"feature_list.json inválido: {exc}")
    if not isinstance(data, dict) or not isinstance(data.get("features"), list):
        fail("feature_list.json debe tener un array features")
    return data


def save_features(data: dict) -> None:
    FEATURE_LIST.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def fail(message: str) -> None:
    print(f"[FAIL] {message}", file=sys.stderr)
    raise SystemExit(1)


def verdict_of(feature_id: str) -> str | None:
    review = ROOT / "progress" / f"review_{feature_id}.md"
    if not review.is_file():
        return None
    for line in review.read_text(encoding="utf-8").splitlines():
        if line.startswith("**Veredicto:**"):
            return line.removeprefix("**Veredicto:**").strip()
    return None


def missing_specs(feature_id: str) -> list[str]:
    missing = []
    for name in SPEC_FILES:
        if not (ROOT / "specs" / feature_id / name).is_file():
            missing.append(f"specs/{feature_id}/{name}")
    return missing


def check() -> int:
    errors: list[str] = []
    for rel in REQUIRED:
        if not (ROOT / rel).is_file():
            errors.append(f"Falta archivo base: {rel}")

    if not FEATURE_LIST.is_file():
        for error in errors:
            print(f"[FAIL] {error}")
        return 1

    try:
        data = json.loads(FEATURE_LIST.read_text(encoding="utf-8"))
        features = data["features"]
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
        print(f"[FAIL] feature_list.json inválido: {exc}")
        return 1

    ids = [str(feature.get("id")) for feature in features]
    if len(ids) != len(set(ids)):
        errors.append("Hay ids duplicados en feature_list.json")

    in_progress = [feature for feature in features if feature.get("status") == "in_progress"]
    if len(in_progress) > 1:
        names = ", ".join(str(feature.get("id")) for feature in in_progress)
        errors.append(f"Hay {len(in_progress)} features in_progress ({names}); el máximo es 1")

    for feature in features:
        feature_id = str(feature.get("id"))
        status = feature.get("status")
        lane = feature.get("lane")
        acceptance = feature.get("acceptance")
        if status not in VALID_STATUS:
            errors.append(f"{feature_id}: status inválido ({status})")
        if lane not in VALID_LANE:
            errors.append(f"{feature_id}: lane inválido ({lane})")
        if not isinstance(acceptance, list) or not acceptance:
            errors.append(f"{feature_id}: acceptance debe ser una lista no vacía")
        if lane == "fast" and status == "spec_ready":
            errors.append(f"{feature_id}: spec_ready solo existe en el carril sdd")
        if lane == "sdd" and status in {"spec_ready", "in_progress", "done"}:
            for path in missing_specs(feature_id):
                errors.append(f"{feature_id}: falta {path}")
        if status == "done" and verdict_of(feature_id) != "APPROVED":
            errors.append(
                f"{feature_id}: done sin la línea '**Veredicto:** APPROVED' "
                f"en progress/review_{feature_id}.md"
            )

    if errors:
        for error in errors:
            print(f"[FAIL] {error}")
        return 1

    print(
        f"[OK] feature_list.json válido "
        f"({len(features)} features, {len(in_progress)} in_progress)"
    )
    return 0


def find_feature(data: dict, feature_id: str) -> dict:
    for feature in data["features"]:
        if str(feature.get("id")) == feature_id:
            return feature
    fail(f"No existe la feature {feature_id}")
    raise AssertionError("unreachable")


def append_history(line: str) -> None:
    history = ROOT / "progress" / "history.md"
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    with history.open("a", encoding="utf-8") as handle:
        handle.write(f"\n- {stamp} — {line}\n")


def approve_spec(feature_id: str, confirmation: str) -> int:
    if confirmation != "approved":
        fail("Uso: ./scripts/approve-spec.sh <id> approved")
    data = load_features()
    feature = find_feature(data, feature_id)
    if feature.get("lane") != "sdd":
        fail(f"{feature_id} está en carril fast; no tiene puerta de especificación")
    if feature.get("status") != "spec_ready":
        fail(f"{feature_id} está en {feature.get('status')}; se esperaba spec_ready")
    missing = missing_specs(feature_id)
    if missing:
        fail("Faltan specs: " + ", ".join(missing))
    in_progress = [
        str(item.get("id"))
        for item in data["features"]
        if item.get("status") == "in_progress"
    ]
    if in_progress:
        fail(f"Ya hay una feature in_progress: {', '.join(in_progress)}")
    feature["status"] = "in_progress"
    save_features(data)
    append_history(f"spec aprobada por humano, feature {feature_id} -> in_progress")
    print(f"[OK] {feature_id}: spec_ready -> in_progress")
    return 0


def close_feature(feature_id: str) -> int:
    data = load_features()
    feature = find_feature(data, feature_id)
    if feature.get("status") != "in_progress":
        fail(f"{feature_id} está en {feature.get('status')}; se esperaba in_progress")
    if verdict_of(feature_id) != "APPROVED":
        fail(
            f"Falta '**Veredicto:** APPROVED' en progress/review_{feature_id}.md. "
            "El revisor tiene que escribir ese archivo antes del cierre."
        )
    if feature.get("lane") == "sdd":
        missing = missing_specs(feature_id)
        if missing:
            fail("Faltan specs: " + ", ".join(missing))
    feature["status"] = "done"
    save_features(data)
    append_history(f"feature {feature_id} cerrada ({feature.get('lane')})")
    print(f"[OK] {feature_id}: in_progress -> done")
    return 0


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] in {"check", "--check"}:
        return check()
    command = argv[1]
    if command == "approve-spec":
        if len(argv) != 4:
            fail("Uso: ./scripts/approve-spec.sh <id> approved")
        return approve_spec(argv[2], argv[3])
    if command == "close":
        if len(argv) != 3:
            fail("Uso: ./scripts/close-feature.sh <id>")
        return close_feature(argv[2])
    fail(f"Comando desconocido: {command}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
