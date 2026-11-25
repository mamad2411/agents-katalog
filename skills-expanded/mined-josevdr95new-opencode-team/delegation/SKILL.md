---
name: Delegation
description: Playbook del orquestador para delegar en subagentes — briefings completos, escalado de esfuerzo, paralelización y protocolo de artefactos, basado en las prácticas de Anthropic para sistemas multi-agente.
---

## Plantilla de briefing (úsala siempre)

Cada tarea que lances a un subagente debe incluir:

1. **Objetivo**: una frase con el resultado esperado, no el procedimiento.
2. **Contexto**: rutas relevantes, spec aplicable en `.team/`, decisiones ya tomadas.
3. **Alcance**: archivos o módulos permitidos. Todo lo demás está fuera de límites.
4. **Formato de salida**: qué debe entregar (código + tests, informe en `.team/...`, veredicto...).
5. **Criterios de aceptación**: cómo sabrás que está bien, verificables.
6. **Restricciones**: qué NO hacer (no refactorizar de más, no tocar dependencias, no commitear).
7. **Investigación**: indica si debe verificar algo concreto en internet antes de actuar.

## Escalado de esfuerzo

| Tarea | Equipo |
|---|---|
| Trivial (typo, una línea) | Tú mismo, sin subagentes |
| Bug o cambio pequeño | 1 agente adecuado |
| Feature mediana | 2–3 agentes en flujo (ej. designer → frontend → debugger) |
| Feature grande | Flujo SDD completo con compuertas de calidad |

Nunca lances más de 3–4 subagentes en paralelo salvo independencia real. Más agentes para una tarea simple desperdicia tokens y genera ruido.

## Paralelización y dependencias

- En paralelo: revisiones (debugger + security-auditor), researches independientes.
- En serie: designer → frontend → revisiones; spec → plan → tasks → implement.
- No lances la tarea dependiente "a ver qué sale": espera el reporte del predecesor e incluye sus conclusiones en el siguiente briefing.

## Protocolo de artefactos

- Los subagentes escriben salidas largas (specs, informes de auditoría, diseño) en `.team/` y devuelven SOLO resumen + ruta. Así la información no se degrada entre intermediarios.
- Tú consolidas en tu respuesta al usuario: decisiones, estado y siguientes pasos.

## Modos de fallo típicos (evítalos)

- Briefing vago → trabajo duplicado o fuera de alcance. La plantilla de arriba existe por eso.
- Lanzar 10 agentes para algo simple → presupuesta el esfuerzo (tabla de escalado).
- Confiar en el reporte del subagente sin verificar → revisa `git diff` y tests tú mismo antes de cerrar.
- Dejar que los subagentes negocien entre ellos → los conflictos los arbitras TÚ.
