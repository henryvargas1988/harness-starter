# AGENTS.md — Mapa del arnés

Este archivo es el punto de entrada. No es una biblia: es un mapa.
Lee solo el documento que necesites.

El arnés sirve para que un agente trabaje con estado en disco, una sola
feature a la vez y una verificación ejecutable. La aplicación todavía no
existe: se construye dentro de este repositorio después de la feature `001`.

## 1. Arranque

1. Ejecuta `./init.sh`. Si falla, para y arregla el entorno antes de tocar producto.
2. Lee `progress/current.md`.
3. Lee `feature_list.json`.
4. Si el directorio es un repositorio git, lee `git status` y `git log --oneline -20`. Ese historial es la otra memoria: dice qué quedó hecho y a qué commit se puede volver.
5. Si vas a orquestar o a elegir carril, lee `docs/harness.md`.

## 2. Mapa

| Ruta | Qué es | Cuándo |
| --- | --- | --- |
| `feature_list.json` | Alcance y estado de cada feature | Siempre, al empezar |
| `progress/current.md` | Sesión viva | Siempre, al empezar |
| `progress/history.md` | Bitácora append-only | Si hace falta contexto de sesiones previas |
| `docs/harness.md` | Carriles, roles y transiciones | Al orquestar |
| `docs/architecture.md` | Qué es buen trabajo en este producto | Antes de implementar |
| `docs/conventions.md` | Stack, nombres, errores | Antes de escribir código |
| `docs/verification.md` | Cómo demostrar que funciona | Antes de cerrar |
| `CHECKPOINTS.md` | Criterios de cierre | El revisor |
| `agents/` | Contratos de líder, spec, implementador y revisor | Al delegar |
| `specs/<id>/` | Spec de una feature en carril `sdd` | Solo esa feature |
| `scripts/verify.sh` | Verificación propia del producto, si existe | La usa `init.sh` |

## 3. Reglas duras

- Una sola feature `in_progress`.
- No declares `done` editando el JSON. El cierre es `./scripts/close-feature.sh <id>` y exige `**Veredicto:** APPROVED` en `progress/review_<id>.md` más `./init.sh` en verde.
- En carril `sdd`, nadie escribe código de producto mientras el estado no sea `in_progress`. La transición `spec_ready -> in_progress` es `./scripts/approve-spec.sh <id> approved`, y solo cuando el humano haya aprobado la spec en este chat.
- Hasta que `docs/architecture.md` diga `ESTADO: definido`, la única feature trabajable es `001`. No crees código de producto antes.
- Los subagentes escriben su resultado en un archivo y devuelven una sola línea con la ruta. El contenido no viaja por el chat.
- Si una herramienta falla de forma inesperada, no improvises un atajo. Anota el bloqueo en `progress/current.md`, pon la feature en `blocked` y para.

## 4. Elegir trabajo

1. Si hay una feature `in_progress`, continúa esa. No abras otra.
2. Si hay una `spec_ready`, para y pide revisión humana. No implementes.
3. Si no, toma la feature `pending` de menor `id`.
4. Anota en `progress/current.md` el id, el carril y un plan corto antes de editar.

## 5. Cierre de sesión

1. `./init.sh` en verde, o la feature queda `blocked` con el motivo escrito.
2. Si el revisor aprobó, cierra con `./scripts/close-feature.sh <id>`.
3. Deja en `progress/current.md` la plantilla vacía (`Feature en curso: ninguna`) solo cuando no quede trabajo a medias.
4. Si hay cambios y el humano no pidió lo contrario, haz un commit con mensaje descriptivo. No incluyas secretos ni `.env`. No uses `--no-verify`, `--amend` ni push forzado. Ese commit es el punto al que la sesión siguiente puede volver.
5. No dejes secretos, ni depuración temporal, ni TODOs sin contexto.
