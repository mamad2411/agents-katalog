---
name: SDD
description: Desarrollo dirigido por especificación (Spec-Driven Development, inspirado en GitHub Spec Kit) — constitución, spec, plan, tareas, implementación y convergencia para features no triviales.
---

## Cuándo usarla

Cualquier feature nueva, cambio multi-archivo o trabajo con requisitos ambiguos que el orquestador vaya a delegar al equipo. NO la uses para typos, fixes de una línea o preguntas puntuales.

## Fases (una a la vez, sin saltarte el artefacto)

0. **Constitución** (una vez por proyecto) — crea o actualiza `.team/constitution.md` siguiendo `references/constitution.md`. Si ya existe, léela y respétala; propón cambios solo si algo choca con el trabajo actual.
1. **Specify** — escribe `.team/spec/<slug>/spec.md` con la plantilla `references/spec.md`. Define el QUÉ y el POR QUÉ, sin decisiones tecnológicas.
2. **Clarify** — solo si hay ambigüedad que bloquee: máximo 5 preguntas al usuario, agrupadas en una sola mensaje. Lo demás lo decides tú y lo documentas en la spec.
3. **Plan** — escribe `.team/spec/<slug>/plan.md` con `references/plan.md`. El CÓMO: arquitectura, stack, contratos de datos y API.
4. **Tasks** — escribe `.team/spec/<slug>/tasks.md` con `references/tasks.md`: tareas numeradas, cada una con agente responsable, alcance de archivos y criterio de aceptación verificable.
5. **Implement** — delega tarea por tarea siguiendo la skill `delegation` (briefings completos, paraleliza lo independiente, compuertas de calidad al cierre).
6. **Analyze / Converge** — verifica cada criterio de aceptación de la spec contra el código real; marca el estado en `tasks.md`; corrige lo que falle y repite hasta que todo converja.

## Reglas

- No avances de fase sin el artefacto escrito. El artefacto es la fuente de verdad, no tu memoria.
- Si el código contradice la spec, actualiza primero la spec (con el usuario si cambia alcance) y después el código.
- Specs vivas: cualquier cambio de comportamiento posterior actualiza la spec correspondiente.
- Muestra al usuario la spec y el plan antes de implementar, salvo que pida velocidad máxima.
