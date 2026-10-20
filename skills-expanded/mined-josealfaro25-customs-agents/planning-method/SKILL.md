---
name: planning-method
description: "Método para planificar tareas de desarrollo: aclarar el objetivo, investigar el código, descomponer en pasos verificables, estimar riesgo y definir criterios de aceptación. Cargar al planificar una feature, bug complejo, migración o cualquier tarea de más de un archivo."
---

# planning-method

Un buen plan permite que otra persona (o agente) implemente sin volver a preguntar y que alguien revise sin adivinar qué se buscaba.

## Paso 1 — Entender el objetivo

Responde por escrito antes de investigar:

- **Qué** se quiere lograr (resultado observable para el usuario o el sistema).
- **Por qué** (problema que resuelve) — cambia las decisiones.
- **Alcance**: qué entra y, explícitamente, qué **no** entra.
- **Restricciones**: fechas, compatibilidad, rendimiento, seguridad, stack obligatorio.

Si alguna respuesta cambia el plan y no se puede deducir del código, **pregunta** (máximo 3 preguntas concretas, con opción recomendada). Si no, asume lo razonable y déjalo escrito como supuesto.

## Paso 2 — Investigar antes de proponer

1. Carga `core:project-context` y resume el stack.
2. Localiza el código afectado: puntos de entrada, módulos, modelos de datos, tests existentes.
3. Busca **precedentes**: ¿hay algo parecido ya implementado? El plan debe reutilizar ese patrón.
4. Identifica dependencias: otros servicios, migraciones, variables de entorno, contratos de API consumidos por web/mobile.
5. Revisa ADRs y CLAUDE.md por decisiones que restrinjan la solución.

Cita archivos concretos (`ruta:línea`) en el plan. Un plan sin rutas es una suposición.

## Paso 3 — Opciones (solo si hay decisión real)

Si hay más de una forma razonable, compara 2–3 opciones en una tabla (esfuerzo, riesgo, impacto, reversibilidad) y **recomienda una**. Si la decisión es arquitectónica (nuevo servicio, nueva librería central, cambio de modelo de datos), deriva a `core:architect` y registra un ADR.

## Paso 4 — Descomponer

Reglas para los pasos:

- Cada paso es **pequeño** (idealmente un commit), **verificable** (cómo sé que está bien) y deja el sistema funcionando.
- Orden por dependencias: modelo de datos → lógica/servicio → API → cliente (web/mobile) → docs.
- Marca qué pasos se pueden hacer en paralelo y qué agente especialista conviene (`backend:fastapi-developer`, `frontend:nextjs-developer`, ...).
- Tests junto al paso que implementan, no al final.
- Incluye pasos de migración/feature flag/rollback si el cambio toca datos o producción.

## Paso 5 — Riesgos y criterios de aceptación

- **Riesgos**: qué puede salir mal, probabilidad/impacto y mitigación.
- **Criterios de aceptación**: lista verificable (Dado / Cuando / Entonces o checklist). Son el contrato para `core:tester` y `core:reviewer`.

## Plantilla de salida

Usa la plantilla de [references/plan-template.md](references/plan-template.md). Para tareas pequeñas (1–2 archivos, sin decisiones), usa solo: Objetivo · Archivos · Pasos · Verificación.

## Estimación

Usa tallas relativas, no horas: **S** (< medio día, 1–3 archivos), **M** (1–2 días, un módulo), **L** (varios módulos o servicios; conviene dividir), **XL** (dividir obligatoriamente en entregas independientes).

## Antipatrones

- Planear sin haber abierto el código.
- Pasos vagos: "implementar backend", "hacer el frontend".
- Un único paso gigante al final: "probar todo".
- Mezclar refactor grande con feature nueva en el mismo plan sin separarlos.
- Esconder supuestos: si asumiste algo, escríbelo.
