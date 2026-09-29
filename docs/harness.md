# Cómo opera el arnés

Harness engineering es el entorno alrededor del modelo: estado en el
repositorio, contexto acotado, roles separados y una verificación que no
depende de que el modelo diga que terminó.

No es la forma obligatoria de escribir cada cambio. Es el modo de trabajo
cuando el cambio merece memoria y una puerta de calidad. Un bug local o una
pregunta se responden en el chat, sin este protocolo.

## Carriles

| Carril | Cuándo | Flujo |
| --- | --- | --- |
| `fast` | Contrato ya claro, cambio local, o la propia feature `001` | `pending` → `in_progress` → `done` |
| `sdd` | Feature nueva, cambio de arquitectura, migración, comportamiento con varios casos | `pending` → `spec_ready` → (humano) → `in_progress` → `done` |

El campo es `lane` en `feature_list.json`. `sdd: true` del video equivale a
`"lane": "sdd"`. Si dudas, usa `fast` y sube a `sdd` cuando aparezcan
decisiones que no quieres redescubrir dentro del código.

## Máquina de estados

Estados válidos: `pending`, `spec_ready`, `in_progress`, `done`, `blocked`.

- Como máximo una feature en `in_progress`.
- `spec_ready` solo existe en carril `sdd`, y exige `specs/<id>/requirements.md`, `design.md` y `tasks.md`.
- `done` exige la línea `**Veredicto:** APPROVED` en `progress/review_<id>.md`.
- `blocked` es un alto explícito. Se vuelve a `pending` solo con una nota en `progress/current.md` que diga qué cambió.

Transiciones que no se hacen a mano:

- `spec_ready` → `in_progress`: `./scripts/approve-spec.sh <id> approved`
- `in_progress` → `done`: `./scripts/close-feature.sh <id>`

`approve-spec.sh` lo ejecuta el humano, o el agente únicamente después de que
el humano escriba que la spec está aprobada. El agente no se aprueba la spec.

## Roles

| Rol | Escribe | No escribe |
| --- | --- | --- |
| Líder | `progress/current.md`, coordinación | Código de producto en carril `sdd` |
| Autor de spec | `specs/<id>/` y pasa la feature a `spec_ready` | Código de producto |
| Implementador | Código, tests y `progress/impl_<id>.md` | El estado `done`, la aprobación de la spec |
| Revisor | `progress/review_<id>.md` | Código |

En Cursor, con el humano presente, el mismo agente puede hacer de líder e
implementador en carril `fast`. En carril `sdd` los roles no se mezclan: quien
redacta la spec no la implementa en esa misma pasada, y quien implementa no
se autoaprueba.

Contratos completos: `agents/leader.md`, `agents/spec-author.md`,
`agents/implementer.md`, `agents/reviewer.md`.

## Anti teléfono descompuesto

Cada subagente deja su entregable en disco y responde una sola línea:

```text
done -> progress/impl_002.md
```

```text
APPROVED -> progress/review_002.md
```

```text
spec_ready -> specs/002/
```

```text
blocked -> progress/current.md
```

El líder lee el archivo si necesita el contenido. No pide que se lo peguen en el chat.

## Aislamiento de contexto

El implementador de una feature `sdd` recibe las rutas `specs/<id>/`,
`docs/conventions.md` y `docs/verification.md`. No recibe el historial del chat
ni `progress/history.md`.

## Qué cuenta como código de producto

Todo lo que no sea el arnés. El arnés es: `AGENTS.md`, `CLAUDE.md`,
`CHECKPOINTS.md`, `README.md`, `feature_list.json`, `init.sh`, `docs/`,
`progress/`, `specs/`, `agents/`, `scripts/`, `.cursor/`, `.claude/`.

Mientras `docs/architecture.md` diga `ESTADO: plantilla`, el único trabajo
permitido es la feature `001`.

## Límite de sesión

Al abrir, el agente lee el estado en disco y, si hay git, `git status` y `git log --oneline -20`. Al cerrar, con `./init.sh` en verde, deja un commit descriptivo salvo que el humano haya pedido no commitear. El commit no sustituye a `progress/`: el archivo dice qué se intentó; el commit es el árbol al que se puede volver.

## Cómo evoluciona el arnés

Si una regla falla dos veces, no la reescribas en silencio en medio de una
feature de producto. Abre una feature `fast` cuyo acceptance sea el cambio de
instrucción. El arnés se versiona igual que el código.

## Dónde corre

| Entorno | Qué lee |
| --- | --- |
| Cursor | `AGENTS.md` y `.cursor/rules/harness.mdc`. El hook `stop` corre `init.sh` solo si hay una feature en curso. |
| Claude Code | `CLAUDE.md` y `.claude/agents/`. Cada agente tiene que leer su contrato en `agents/`. |

El protocolo no cambia con el modelo. En Cursor Auto el carril `fast` lo hace
el mismo agente del chat. El carril `sdd` reparte los contratos de `agents/`,
en Cursor o en Claude Code. Quien recibe el trabajo no hereda el historial.
