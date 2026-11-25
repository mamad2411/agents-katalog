---
name: regression-suite-management
description: Gestión de la suite de regresión como activo — selección de qué correr según el impacto del cambio, organización por módulo y tags, smoke vs suite completa, cuarentena formal de tests flaky con dueño y fecha, tiempo de suite como presupuesto, serial en desarrollo vs paralelo/sharding en CI, matriz navegador × viewport × dispositivo y mantenimiento (borrar tests muertos con criterio). Usar al decidir qué regresión corre para un cambio, al armar las etapas de CI, cuando la suite se vuelve lenta o roja crónica, o al cuarentenar o eliminar un test.
effort: high
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Gestión de la suite de regresión

La regresión es un activo con costo de mantenimiento: si crece sin criterio, tarda horas y el
equipo deja de mirarla. Esta skill decide **qué corre, cuándo, dónde y qué se poda**. Cómo se
escribe cada test: `e2e-playwright`, `api-testing`, `unit-testing`. La política general de calidad:
`qa-strategy`; el pipeline completo: `qa-orchestration`.

## 1. Organización

- **Por módulo de negocio** (agenda, archivo clínico, contabilidad…), no por tipo de página ni
  por quién lo escribió. Un cambio en agenda tiene que poder correr "todo agenda" con un comando.
- **Tags** ortogonales al módulo: `@smoke` (flujo crítico, corto), `@regression` (cobertura
  completa del módulo), `@vrt` (visual), `@ui-mock` (sin backend), `@slow`, `@quarantine`.
  En Playwright: opción `tag` en `test`/`describe` y filtro con `--grep` / `--grep-invert`.
- Un test pertenece a un módulo y lleva los tags que correspondan. Sin tag = `@regression` del
  módulo por defecto.
- Nombres que describen el requisito, no el paso (`crea cita y persiste tras reload`, no `test 3`).

## 2. Qué correr según el cambio

| Cambio | Corre |
|---|---|
| Un componente o endpoint de un módulo | Test afectado → `@regression` del módulo → `@smoke` global |
| Componente compartido, token, CSS global, guard, interceptor, middleware | `@regression` de todos los módulos que lo consumen + `@vrt` |
| Modelo de datos / esquema | `integrity-testing` del área + `@regression` de los módulos que leen esas tablas |
| Dependencias, runtime, config de build | Suite completa |
| Solo docs / comentarios | Nada de E2E; el CI corre igual lo estático |

Determiná el impacto con `Grep` de importadores/consumidores, no de memoria. Si no podés acotar
el impacto con confianza, corré todo. Playwright ofrece `--only-changed` como primer filtro rápido
en PRs, pero no reemplaza el análisis de impacto de componentes compartidos.

## 3. Etapas por entorno

| Dónde | Modo | Alcance |
|---|---|---|
| Máquina de desarrollo | **Serial**: `--workers=1`, un runner a la vez, sin background (`agent-resource-control`) | Inner loop + regresión del módulo |
| PR en CI | Paralelo con `--shard=i/n` en varios jobs; base efímera por job | Estático → unit → API → `@smoke` + regresión de módulos impactados |
| Rama de integración (post-merge) | Paralelo | Suite completa + `@vrt` |
| Nightly | Paralelo | Suite completa × matriz cross-browser + `performance-load-testing` smoke + DAST |
| Pre-release | Según release | Suite completa + smoke en staging desplegado |

- Los tests tienen que ser **paralelizables por diseño** (dueños de sus datos, aislados por worker;
  `test-data-management`) aunque en desarrollo corran en serie.
- Retries: `0` en desarrollo y diagnóstico. En CI, como máximo 1 y **solo con reporte de flaky
  visible** —un test que pasó en retry cuenta como flaky, no como verde limpio.
- Trace `on-first-retry` o `retain-on-failure`, artefactos subidos siempre (`github-actions-ci`).

## 4. Matriz navegador × viewport × dispositivo

- Motor principal (Chromium) en todo. Firefox y WebKit: `@smoke` + módulos con riesgo de render
  (formularios complejos, tablas, overlays), como proyectos separados, secuenciales en desarrollo.
- Viewports: móvil estrecho, tablet, desktop en rutas visuales (`frontend-responsive-layout`).
  Emulación de dispositivo con `devices[...]` de Playwright para touch.
- Mobile nativo: la matriz de dispositivos la fija el `CLAUDE.md` de la app.
- Documentá la matriz vigente en el proyecto («definilo en el CLAUDE.md del proyecto»). Una matriz
  implícita se erosiona.

## 5. Presupuesto de tiempo

- Fijá un presupuesto por etapa (p. ej. el PR no puede tardar más de X minutos de punta a punta;
  el valor lo decide el equipo) y tratá superarlo como un fallo a resolver, no como el nuevo normal.
- Palancas, en orden: paralelizar/shardear; mover a nightly lo que no necesita correr por PR;
  bajar E2E redundantes a API/unit (`qa-strategy` trofeo); eliminar duplicados; recién al final
  optimizar tests individuales.
- Medí: duración por etapa y por test (el reporte de Playwright lo da). Los 10 tests más lentos se
  revisan cada sprint.

## 6. Cuarentena de flaky

Un flaky no se ignora, no se re-ejecuta hasta verde, no se borra a escondidas.

1. Confirmá que es flaky: `--repeat-each=N --workers=1` sobre el test; registrá la tasa.
2. Cuarentená **formalmente**: tag `@quarantine`, ticket abierto, **dueño** y **fecha límite**
   (corta). El test sigue corriendo en un job separado no bloqueante, para tener datos.
3. Diagnosticá con `e2e-failure-triage` §5 y `root-cause-debugging`. Causas típicas: carreras,
   reloj, datos compartidos, animaciones, orden.
4. Al vencer la fecha: se arregla o se elimina con justificación. Nunca queda en cuarentena
   indefinida.
5. Métrica: cantidad en cuarentena y tasa de retry del CI. Si suben, hay un problema sistémico
   (entorno, datos), no tests aislados.

## 7. Mantenimiento y poda

Se elimina un test **con criterio y en un PR explícito** cuando:
- prueba un requisito que ya no existe;
- duplica exactamente otro (mismo camino, mismas aserciones);
- su cobertura pasó a un nivel más barato (API/unit) con el mismo requisito;
- lleva más del plazo en cuarentena sin dueño capaz de arreglarlo, y se documenta la pérdida.

No se elimina porque "molesta", "es lento" o "falla". Eliminar tests para cerrar un carril está
prohibido (`finish-your-turn`). Cada eliminación cita el requisito y dónde queda cubierto.

Revisión periódica: tests muertos (nunca fallan y no afirman nada útil), aserciones vacías,
`skip` olvidados, tags desactualizados.

## Anti-patrones

- Una suite única de dos horas que corre "todo o nada".
- Retries globales altos que fabrican verde.
- Cuarentena sin fecha = cementerio.
- Correr en paralelo en la laptop y culpar al entorno por los fallos.
- Borrar tests en el mismo PR que rompe la funcionalidad.
- Elegir qué correr "de memoria" en vez de por impacto medido.

## Checklist

- [ ] Suite organizada por módulo con tags ortogonales.
- [ ] Alcance de regresión derivado del impacto real del cambio.
- [ ] Serial en desarrollo; paralelo/shard solo en CI con aislamiento por worker.
- [ ] Retries 0 en desarrollo; flaky visible en CI.
- [ ] Matriz de navegadores/viewports documentada y corrida donde corresponde.
- [ ] Presupuesto de tiempo por etapa vigilado; 10 más lentos revisados.
- [ ] Cuarentena con tag, ticket, dueño y fecha.
- [ ] Eliminaciones justificadas en PR propio.

## Evidencia / DoD

Para afirmar "regresión corrida" pegá literal: los comandos por etapa con su `--grep`/`--project`
y el resumen de cada uno (`passed / failed / flaky / skipped`), la lista de módulos incluidos y
por qué (impacto), y el estado de la cuarentena (cantidad, con tickets). `skipped > 0` o
`flaky > 0` se explican uno por uno. Ver `evidence-and-verification`.
