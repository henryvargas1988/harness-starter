# Arquitectura

ESTADO: plantilla

Este archivo lo rellena la feature `001`. Hasta entonces no es una
especificación de producto: es un formulario.

## Problema

Qué duele y para quién. Una frase, luego el detalle mínimo.

## Usuarios

Quién lo usa y qué intenta conseguir.

## Fuera de alcance

Qué no se va a construir en esta etapa. Escribe tres límites concretos.

## Dirección de código

- Stack:
- Directorio de código:
- Directorio de tests:
- Comando de verificación: `./init.sh` y, si hace falta, `scripts/verify.sh`
- Interfaz: hay / no hay. Si hay, herramienta del recorrido de usuario:

## Qué significa hacer un buen trabajo

Sustituye esta lista cuando el producto exista. Mientras tanto:

- El cambio cabe en la feature que está `in_progress`.
- El comportamiento nuevo tiene una prueba o un comando que falla si se rompe.
- Las dependencias nuevas se justifican en la feature, no se añaden de paso.

## Flujo de datos

Dibuja aquí el camino de una petición o de un comando cuando ya se conozca.
No adelantes capas (servicios, repositorios, colas) sin una feature que las pida.
