# Verificación

El agente no dice que funciona. `./init.sh` lo demuestra.

## Orden que usa init.sh

1. `python3 scripts/harness.py check` — invariantes del arnés.
2. La suite de la aplicación, en este orden de preferencia:
   - `scripts/verify.sh` si existe
   - `pnpm test`, `yarn test` o `npm test` si hay `package.json`
   - `go test ./...` si hay `go.mod`
   - `cargo test` si hay `Cargo.toml`
   - `pytest` o `unittest` si hay proyecto Python o carpeta `tests/`
   - si no hay nada de eso, el arnés puede estar verde sin suite de producto

Cuando el autodetector no describa el producto (monorepo, e2e, dos lenguajes),
copia `scripts/verify.sh.example` a `scripts/verify.sh`. A partir de ese
momento `init.sh` solo corre ese script.

## Qué tiene que cubrir una feature

Cada criterio de `acceptance` necesita evidencia ejecutable: un test, un
comando o una comprobación que falle si el criterio deja de cumplirse.
Un test que solo comprueba que no hay excepción no cuenta.

## Interfaz

Si el producto tiene interfaz, una feature que la toca no se cierra con un
test unitario ni con una petición que no la ejercita. El cierre incluye un
recorrido como lo haría un usuario: abrir, actuar y comprobar el resultado.
La herramienta (navegador, automatización o el comando equivalente) se nombra
en `docs/architecture.md` durante la feature `001`. Si no hay interfaz, ese
archivo lo dice y este requisito no aplica.

## Antes de cerrar

```bash
./init.sh
./scripts/close-feature.sh <id>
```

`close-feature.sh` vuelve a ejecutar `init.sh`. Si está rojo, la feature no
queda `done`.

Si no puedes dejar la suite en verde, el estado correcto es `blocked`, con el
comando y el error escritos en `progress/current.md`.
