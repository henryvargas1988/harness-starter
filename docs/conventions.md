# Convenciones

Stack: por definir en la feature `001`.

Hasta que el stack esté escrito aquí, no se elige framework, ni se añade
dependencia, ni se crea el directorio de producto.

## Cuando el stack ya esté definido

- Sigue el estilo del código que ya existe en el directorio de producto.
- Un cambio, una feature. No mezcles refactors oportunistas.
- Los errores que el llamador puede provocar se reportan de forma explícita.
  No los tragues ni los conviertas en un éxito silencioso.
- Nada de secretos en el repositorio. Usa `.env` local y documenta las claves
  vacías en `.env.example` si el producto las necesita.
- Los nombres de archivos y de tests describen el comportamiento, no el
  momento en que se escribieron (`test_rejects_empty_title`, no `test_1`).
- No dejes `print` de depuración, ni TODOs sin la feature a la que pertenecen.

## Specs (solo carril sdd)

Los requisitos de `specs/<id>/requirements.md` usan EARS, una frase por
criterio comprobable:

- `THE SYSTEM SHALL <respuesta>`
- `WHEN <disparador> THE SYSTEM SHALL <respuesta>`
- `WHILE <estado> THE SYSTEM SHALL <respuesta>`
- `IF <condición no deseada> THEN THE SYSTEM SHALL <respuesta>`
- `WHERE <opción> THE SYSTEM SHALL <respuesta>`

Cada requisito debe poder convertirse en un caso de prueba sin inventar
comportamiento extra.
