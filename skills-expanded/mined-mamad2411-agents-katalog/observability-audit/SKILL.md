---
name: observability-audit
description: Auditoría de observabilidad del backend Atlas (logs estructurados, correlation/trace id, métricas RED, trazas OTel, health liveness/readiness, redacción de PII en logs, observabilidad de workers, handlers de proceso). Úsala para evaluar la madurez de observabilidad con evidencia archivo:línea.
---

# observability-audit

**Propósito.** Evaluar la capacidad de operar y diagnosticar el backend en producción.

**Cuándo usarla.** Antes de un release, tras incidentes, o al preparar dashboards/alertas.
**Cuándo NO.** Para optimizar rendimiento (usa `performance-audit`).

**Fuentes obligatorias.** `src/common/logging/`, `src/common/observability/`, `src/observability/`, `src/modules/health/`, `src/common/filters/`, `src/main.ts`, `ops/observability/`, `docs/runbooks/`.

**Entradas.** Alcance opcional.

**Condiciones de parada.** Detente si evaluar algo exige levantar el servidor con config real de producción.

**Flujo por fases.**
1. Logs: ¿estructurados (JSON)? ¿niveles consistentes? ¿logger único?
2. Correlación: ¿`correlationId` y `trace_id` propagados a cada línea (AsyncLocalStorage)?
3. Métricas: `/metrics`, RED por endpoint, cardinalidad de labels; ¿se ven 401/403/429?
4. Trazas: config OTel opt-in, sampling documentado, flush en SIGTERM/SIGINT.
5. Health: liveness/readiness separados; readiness devuelve 503 real; verifica Postgres/Redis.
6. Redacción: PII enmascarada en TODOS los caminos de log (no solo persistencia estructurada).
7. Workers/jobs: ¿emiten logs y métricas de progreso/fallo, o solo estado en DB?
8. Handlers de proceso: `unhandledRejection`/`uncaughtException` que loguean con stack + flush + exit≠0.
9. Alertas/runbooks/dashboards versionados.

**Comandos permitidos.** Lectura, grep, `graphify`, `yarn type-check`.
**Comandos prohibidos.** Levantar el servidor contra recursos de producción.

**Evidencia requerida.** `archivo:línea` por hallazgo; nivel de madurez (inicial/intermedio/avanzado) justificado.

**Entregables.** Informe: resumen con madurez, hallazgos por severidad, aspectos positivos, no verificado.

**Formato.** Español, por severidad, con archivo:línea.

**Checklist final.** ¿Logs, correlación, métricas, trazas, health, redacción, workers, handlers cubiertos?

**Limitaciones.** Estática; no valida el pipeline de logs/trazas en runtime.

**Trazabilidad.** `CLAUDE_ORGANIZAR_SKILLS_BACKEND.md` §11 + auditoría 2026-07-21 (Observabilidad).
