---
name: prompt-update
description: Actualiza un prompt canónico sin degradar su contrato. Clasifica el cambio como MAJOR, MINOR o PATCH, ajusta versión, relaciones e índices, registra el changelog y ejecuta las validaciones documentales. Úsala cuando haya que cambiar reglas, fases, entregables, restricciones o redacción de un prompt estable, o cuando se pida versionar, deprecar o corregir un prompt del catálogo.
license: MIT
allowed-tools: Read Grep Glob Edit
metadata:
  framework: "agents-first"
  asset-id: "ai-agent-engineering.prompt-update"
  asset-version: "1.1.0"
  domain: "ai-agent-engineering"
  status: "stable"
  repo-compatibility: "model-agnostic"
  canonical: "library/domains/ai-agent-engineering/skills/prompt-update/SKILL.md"
---

# Skill: Actualización de Prompt

## Objetivo

Modificar un prompt sin degradar su universalidad, seguridad, contrato ni trazabilidad.

## Problema que resuelve

Los prompts cambian como software: una edición aparentemente pequeña puede alterar autoridad, fases o resultados sin quedar versionada.

## Cuándo utilizarla

Para cambiar reglas, fases, entregables, restricciones o redacción de un prompt estable.

## Cuándo no utilizarla

Para crear un activo de otro tipo o hacer cambios editoriales fuera de prompts.

## Entradas esperadas

- solicitud y resultado esperado;
- prompt actual y activos relacionados;
- política de versionado;
- reglas del repositorio.

## Dependencias

- Política de versionado.
- Changelog.
- Validaciones documentales del repositorio.

## Casos de uso

- agregar una fase compatible;
- corregir un contrato ambiguo;
- deprecar una regla con transición.

## Resultado esperado

Prompt actualizado, versión clasificada, changelog registrado y validaciones reportadas.

## Restricciones

- Leer el prompt completo antes de editar.
- No acoplarlo a un modelo o stack salvo que su alcance lo declare.
- No relajar aprobación, pruebas o seguridad para simplificar la ejecución.
- No inventar comandos ni rutas.

## Procedimiento

1. Lee el prompt, relacionados y [política de versionado](../../PROMPT_VERSIONING.md).
2. Explica el cambio de contrato y clasifícalo como MAJOR, MINOR o PATCH.
3. Aplica el cambio mínimo coherente.
4. Actualiza `version`, relacionados e índices cuando corresponda.
5. Registra el cambio en [CHANGELOG](../../docs/CHANGELOG.md).
6. Ejecuta las [pruebas documentales](../../docs/agent/TESTS.md).
7. Revisa el diff para descartar cambios fuera de alcance.

## Buenas prácticas

- Separar condiciones obligatorias de ejemplos.
- Usar fases y salidas verificables.
- Reutilizar checklists o templates mediante enlaces cuando eviten duplicación.

## Checklist

- [ ] El objetivo permanece claro.
- [ ] Entradas, restricciones y salida son coherentes.
- [ ] Lee antes de modificar y prohíbe comandos inventados.
- [ ] Exige plan y evidencia cuando puede causar cambios.
- [ ] No reduce controles de prueba o seguridad.
- [ ] Versión, catálogo e historial están alineados.

## Errores frecuentes

- Agregar casos específicos al núcleo universal.
- Cambiar comportamiento y clasificarlo como PATCH.
- Duplicar reglas que ya tienen una fuente canónica.
- Actualizar el prompt sin validar sus enlaces.

## Documentos relacionados

- [Prompt maestro](../../prompts/agents-first-documentation-review.prompt.md)
- [Guía de contribución](../../docs/CONTRIBUTING_ASSETS.md)

## Prompts compatibles

- Todos los prompts del catálogo que sigan el contrato común.

## Skills relacionadas

- [Auditoría documental](../../library/domains/documentation-knowledge/skills/documentation-audit/SKILL.md)

## Ejemplo

Agregar una salida opcional es MINOR; corregir ortografía sin cambiar obligaciones es PATCH. En ambos casos se actualiza versión, changelog y evidencia.

## Procedencia

Proyección generada del activo canónico [`library/domains/ai-agent-engineering/skills/prompt-update/SKILL.md`](../../library/domains/ai-agent-engineering/skills/prompt-update/SKILL.md).

No edites este archivo: modifica la fuente en `library/` y ejecuta `npm run build:skills`.
La puerta de calidad falla si esta proyección queda desactualizada.
