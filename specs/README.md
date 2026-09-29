# Specs

Solo las features con `"lane": "sdd"` tienen carpeta aquí.

```bash
cp -R specs/_template specs/<id>
```

El autor de la spec rellena los tres archivos y deja la feature en
`spec_ready`. El implementador no empieza hasta que alguien ejecute:

```bash
./scripts/approve-spec.sh <id> approved
```

`specs/_template/` no es una feature. El validador ignora los directorios que
no correspondan a un id en estado `spec_ready`, `in_progress` o `done`.
