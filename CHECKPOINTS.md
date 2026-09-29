# CHECKPOINTS

Se evalúa el destino, no el relato. El revisor marca cada punto en
`progress/review_<id>.md`. Un solo fallo relevante produce
`CHANGES_REQUESTED`.

## C1 — El arnés sigue entero

- Existen `AGENTS.md`, `init.sh`, `feature_list.json`, `progress/current.md` y `docs/harness.md`.
- `./init.sh` termina con código 0.

## C2 — El estado es coherente

- Hay como máximo una feature `in_progress`.
- La feature trabajada es la que declara `progress/current.md`.
- Si el carril es `sdd`, existen `specs/<id>/requirements.md`, `design.md` y `tasks.md`, y el código no se adelantó a la aprobación humana.

## C3 — El cambio cabe en la feature

- Los archivos de producto tocados estaban previstos en el acceptance o en `specs/<id>/design.md`.
- No hay refactors, dependencias ni archivos ajenos a esa feature.
- `docs/architecture.md` y `docs/conventions.md` se respetan. Si siguen en plantilla, la única feature válida es `001`.

## C4 — La verificación es real

- Cada criterio de acceptance tiene una prueba o un comando que lo demuestra.
- Si `docs/architecture.md` nombra una interfaz, la feature que la toca incluye el recorrido de usuario descrito en `docs/verification.md`. Un test que no ejercita esa interfaz no cubre el criterio.
- La evidencia está copiada o resumida en `progress/impl_<id>.md`, incluyendo el comando.
- `./init.sh` se ejecutó en esta revisión y terminó en verde.

## C5 — La sesión queda legible

- `progress/current.md` describe la sesión activa o dice `Feature en curso: ninguna`.
- No hay secretos, artefactos de depuración ni TODOs sin feature.
- El veredicto cita archivos concretos cuando pide cambios.
