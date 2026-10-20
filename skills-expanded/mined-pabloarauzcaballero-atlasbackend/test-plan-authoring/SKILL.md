---
name: test-plan-authoring
description: Redacción del plan de prueba de una feature, carril o release — alcance y fuera de alcance, riesgos, niveles de prueba, entornos, datos, criterios de entrada y salida, matriz de trazabilidad y qué se automatiza vs qué es manual. Usar al arrancar el QA de un carril, antes de escribir el primer test, al preparar un release, o cuando nadie sabe qué se va a probar ni cuándo se considera terminado. Incluye plantilla.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Redacción de plan de prueba

Un plan de prueba responde, antes de tocar un test: **qué se prueba, cómo, con qué datos, en qué
entorno, y cuándo está terminado**. Es corto y vivo, no un documento ceremonial. La ejecución
coordinada del pipeline la maneja `qa-orchestration`; la estrategia global, `qa-strategy`; el diseño
de los casos, `test-case-design-techniques`.

## Cuándo escribirlo
- Al abrir un carril/feature no trivial, después de tener criterios de aceptación
  (ver `requirements-and-acceptance`) y antes del primer test.
- Para un release, como consolidado de los planes de las features que entran.

## Secciones (mínimas)
1. **Objetivo y alcance**: qué feature/carril, qué resultado observable valida.
2. **Fuera de alcance**: lo que explícitamente NO se prueba acá (para no discutir después).
3. **Riesgos**: qué puede salir mal y qué tan grave; guía dónde poner esfuerzo (ver testing basado en riesgo en `qa-strategy`).
4. **Niveles**: qué se cubre en unit / integración / API / E2E / performance / seguridad y por qué.
5. **Entornos**: dónde corre cada nivel (local, CI, staging), contra qué backend/base.
6. **Datos**: qué datos se necesitan, cómo se generan y limpian (ver `synthetic-test-data-generation`, `test-data-management`).
7. **Criterios de entrada**: qué debe estar listo para empezar a probar (feature desplegada, seeds cargados).
8. **Criterios de salida / DoD**: qué se debe cumplir para declarar probado (todos los criterios cubiertos, cero fallos abiertos de severidad alta, evidencia adjunta).
9. **Automatizado vs manual**: qué queda como test automatizado y qué se hace a mano (y por qué).
10. **Trazabilidad**: matriz requisito → caso(s) → estado.

## Automatizar vs manual — criterio
| Automatizar | Dejar manual |
|---|---|
| Regresión repetible, camino feliz crítico | Exploratorio de una vez (ver `exploratory-testing`) |
| Reglas de negocio y autorización | Evaluación estética/UX subjetiva |
| Casos límite estables | Flujo aún en diseño, muy cambiante |
| Lo que se rompe seguido | Setup carísimo de automatizar para un caso raro |

## Plantilla
```md
# Plan de prueba — <carril/feature>
Objetivo: <resultado observable a validar>
Fuera de alcance: <...>

## Riesgos
- <riesgo> — impacto: alto/medio/bajo — mitigación de prueba: <...>

## Niveles y entorno
- Unit: <qué> — local/CI
- API/integración: <qué> — CI contra base real
- E2E: <flujos> — staging, viewports móvil/tablet/desktop
- Performance/seguridad: <si aplica>

## Datos
<cómo se generan y limpian; seed>

## Criterios de entrada
- [ ] feature desplegada en <entorno>
- [ ] datos/seed cargados

## Criterios de salida (DoD)
- [ ] cada criterio de aceptación con caso(s) en verde
- [ ] 0 defectos abiertos severidad alta/crítica
- [ ] evidencia adjunta (ver qa-evidence-reporting)

## Trazabilidad
| REQ | Caso(s) | Nivel | Estado |
|-----|---------|-------|--------|
```

## Anti-patrones
- Plan-novela que nadie lee ni actualiza.
- Sin criterios de salida: "probar hasta que parezca bien".
- Todo manual "porque es más rápido ahora" (deuda de regresión).
- Riesgos ausentes: se prueba parejo lo crítico y lo trivial.

## Checklist
- [ ] Alcance y fuera de alcance explícitos.
- [ ] Riesgos listados y usados para priorizar.
- [ ] Cada nivel justificado; entorno y datos definidos.
- [ ] Criterios de entrada y de salida (DoD) verificables.
- [ ] Matriz de trazabilidad iniciada.
- [ ] Decisión automatizar/manual registrada por área.
