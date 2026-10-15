---
name: commits-convencionales
description: Guía local para redactar mensajes de commit usando Conventional Commits en español. Usar cuando haya que proponer, revisar o generar mensajes de commit, squash, merge o revert en este repositorio siguiendo la especificación oficial.
---

# Commits Convencionales

Usa este skill para redactar mensajes de Git con formato Conventional Commits en español y con criterio consistente.

## Base de la especificación

- Sigue la estructura `<tipo>[ambito opcional]: <descripcion>`.
- Usa `feat` para nuevas funcionalidades.
- Usa `fix` para correcciones de errores.
- Usa `BREAKING CHANGE:` en el pie, o `!` en el encabezado, cuando el cambio rompa compatibilidad.
- Tipos adicionales permitidos y recomendados para este repo: `docs`, `refactor`, `test`, `build`, `ci`, `chore`, `style`, `perf`, `revert`.

## Reglas para este repositorio

- Escribe siempre el mensaje en español.
- Mantén `tipo` y `ambito` en minúsculas para consistencia.
- Redacta la descripción como un resumen corto, concreto y orientado al resultado.
- Evita terminar la descripción con punto final.
- Usa ámbito cuando mejore la lectura, por ejemplo `feat(ui): ...`, `fix(datos): ...`, `docs(agente): ...`.
- Si el cambio mezcla varias intenciones, separa en varios commits cuando sea viable.

## Selección de tipo

- `feat`: agrega una capacidad nueva visible para el producto o para el desarrollo del proyecto.
- `fix`: corrige un bug o comportamiento incorrecto.
- `docs`: cambia documentación, guías o convenciones sin alterar comportamiento de la app.
- `refactor`: reorganiza código sin cambiar comportamiento observable.
- `style`: cambios de formato o estilo sin impacto funcional.
- `test`: agrega o ajusta pruebas.
- `build`: cambia SDK, paquetes, tooling o configuración de compilación.
- `ci`: cambia pipelines o automatizaciones de integración.
- `chore`: tareas de mantenimiento que no encajan mejor en otro tipo.
- `perf`: mejora rendimiento.
- `revert`: revierte uno o más commits previos.

## Plantillas

- Encabezado simple: `tipo: descripcion`
- Con ámbito: `tipo(ambito): descripcion`
- Con cambio incompatible:
  `tipo(ambito)!: descripcion`

  `BREAKING CHANGE: detalle del cambio incompatible`

## Ejemplos válidos

- `feat(ui): agrega el mockup inicial del layout principal`
- `fix(shell): corrige la selección de tema oscuro`
- `docs(agente): define reglas de documentación y git en español`
- `build(dotnet): migra la solución a .net 10`
- `refactor(viewmodels): separa la navegación mock del acceso a datos`
- `revert: revierte la integración inicial de sqlite`

## Criterio operativo

- Antes de proponer un mensaje, identifica qué cambió realmente: funcionalidad, bug, documentación, tooling o refactor.
- Si el cambio es mayormente visual pero agrega una nueva pantalla o flujo, prioriza `feat`.
- Si el cambio solo prepara infraestructura futura sin exponer una capacidad nueva, evalúa `build`, `refactor` o `chore` según corresponda.
- Si hay dudas entre `feat` y `refactor`, pregunta si cambió la capacidad del sistema; si sí, usa `feat`.

## Revisión rápida

Antes de cerrar un mensaje, verifica:

1. ¿Sigue el formato `tipo(ambito opcional): descripcion`?
2. ¿Está en español?
3. ¿El tipo refleja la intención principal?
4. ¿La descripción es breve y específica?
5. ¿Hay cambio incompatible que requiera `!` o `BREAKING CHANGE:`?

## Recurso asociado

- Consulta `references/especificacion.md` para el resumen de la especificación oficial y sus reglas clave.
