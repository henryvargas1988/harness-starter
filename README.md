# Arnés de entrada

Plantilla para empezar un repositorio en el que un agente pueda trabajar con
estado en disco, una feature a la vez y una verificación ejecutable.

No trae aplicación. El producto se define en la feature `001` y se construye
después, en el stack que elijas. Sirve igual para un CLI, una API o una app
web: el arnés no asume el lenguaje.

Está pensado para Cursor y también lo puede tomar Claude Code.

## Empezar un proyecto

```bash
cp -R harness-starter mi-proyecto
cd mi-proyecto
chmod +x init.sh scripts/*.sh .cursor/hooks/on-stop.py
./init.sh
```

Abre la carpeta en Cursor y pide:

> Sigue AGENTS.md y trabaja la feature 001.

Cuando `001` esté cerrada, el repositorio ya tiene arquitectura, convenciones
y la siguiente feature de producto en `feature_list.json`.

## Cuándo usar cada carril

| Situación | Qué pedir |
| --- | --- |
| Definir el producto, bug local, cambio pequeño | Carril `fast`. El agente implementa y cierra con verificación. |
| Feature nueva o cambio de diseño | Añade la feature con `"lane": "sdd"` y pide la spec. El trabajo se detiene en `spec_ready` hasta que apruebes. |
| Pregunta o experimento | Dilo. No hace falta abrir una feature. |

Aprobar una spec:

```bash
./scripts/approve-spec.sh 002 approved
```

Ese comando es la puerta humana. El agente no debe lanzarlo solo.

## Qué mantiene el orden

- `feature_list.json` es el alcance. `./init.sh` rechaza dos features `in_progress`, un `done` sin revisión, y una spec `sdd` a medias.
- `progress/` es la memoria entre sesiones. El chat no lo es.
- `./scripts/close-feature.sh <id>` es la única forma de marcar `done`. Vuelve a correr `./init.sh`.
- En Cursor, si dejas una feature en curso y `init.sh` falla al terminar el turno, el hook de parada devuelve el error al agente. Si no hay feature activa, no corre la suite.

## Mapa corto

```text
AGENTS.md                 mapa para el agente
docs/harness.md           carriles, roles, transiciones
docs/architecture.md      el producto (empieza en plantilla)
feature_list.json         una feature a la vez
init.sh                   arnés + tests del producto
scripts/verify.sh         opcional, si el autodetector no basta
agents/                   contratos de líder, spec, implementador, revisor
specs/<id>/               solo carril sdd
progress/                 sesión, informes y bitácora
```

La precedencia de tests está en `docs/verification.md`. Si más adelante el
proyecto tiene varios paquetes, `scripts/verify.sh` sustituye al autodetector.

## De dónde sale

Las piezas que sostienen el trabajo largo están tomadas de la ingeniería publicada por Anthropic:

- [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents): lista de features en JSON, una a la vez, `init.sh`, notas de progreso y un commit al que se puede volver.
- [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents): la memoria vive en archivos; el subagente devuelve un resumen, no el transcript.
- [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps): quien implementa no se evalúa solo, y cada pieza del arnés se quita cuando el modelo ya no la necesita.
- [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents): la ceremonia se añade solo cuando mejora el resultado.

Esta plantilla no es el arnés autónomo de esos posts. Hay un humano en el chat, el carril `fast` es el camino por defecto y `sdd` es la puerta para un cambio de diseño. El ejemplo [ejemplo-harness-subagentes](https://github.com/betta-tech/ejemplo-harness-subagentes) muestra el mismo patrón atado a un CLI en Python; aquí el verificador no asume el lenguaje.

Las reglas se tratan como código versionado. Cuando un modelo nuevo haga innecesaria una pieza, se abre una feature para quitarla.
