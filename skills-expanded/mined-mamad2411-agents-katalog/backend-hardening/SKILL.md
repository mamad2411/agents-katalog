---
name: backend-hardening
description: Auditoría de endurecimiento por fases (correctitud, seguridad, integridad de datos, observabilidad, rendimiento, pruebas, despliegue) del backend Atlas. Úsala para revisar el estado de producción del código sin modificarlo; cada conclusión exige evidencia citada archivo:línea.
---

# backend-hardening

**Propósito.** Auditar el backend por áreas y producir un informe priorizado de fallas y mejoras con evidencia.

**Cuándo usarla.** Antes de un release, tras un cambio grande, o cuando se pida una "revisión completa por área".
**Cuándo NO.** Para arreglar un bug puntual (usa `/debug`) o para implementar una feature (usa `backend-production`).

**Fuentes obligatorias.** `docs/audit/` (auditorías previas), `CLAUDE.md`, `.claude/rules/`, `package.json` (comandos reales), el grafo graphify.

**Entradas.** Alcance (todo el backend o módulos concretos). Sin entrada explícita, audita todo.

**Condiciones de parada.** Detente y reporta si: falta una fuente crítica, hay contradicción entre docs y código, o una acción requeriría ejecutar contra una base real / tocar producción.

**Flujo por fases.**
1. Inventario: stack real (package.json, lockfile), módulos (`src/modules/`), grafo.
2. Correctitud: errores tragados, promesas sin await, flujos multi-tabla sin transacción.
3. Seguridad: ver skill `security-audit`.
4. Integridad de datos: migraciones, `_deleted`, FKs, idempotencia, descifrado silencioso.
5. Observabilidad: ver skill `observability-audit`.
6. Rendimiento: ver skill `performance-audit` (estático; marca los hallazgos como riesgos sin medición).
7. Pruebas: ver skill `production-verification`.
8. Despliegue/config: env validado, gates de CI.
9. Verificación final: corre los gates y registra su resultado.

**Comandos permitidos.** Lectura, `graphify query/explain/path`, `yarn type-check`, `yarn lint`, `yarn test:unit`, `yarn build`, gates `yarn check:*`.
**Comandos prohibidos.** Migraciones/seeds contra DB real, `git push`, cualquier cosa contra producción.

**Evidencia requerida.** Cada hallazgo cita `archivo:línea`. Los gates ejecutados se reportan con su salida (verde/rojo). Lo no verificable se marca "no verificado".

**Entregables.** Informe en `docs/audit/` con: resumen por área (tabla), hallazgos por severidad (Crítica/Alta/Media/Baja) con evidencia+impacto+recomendación, aspectos positivos, no verificado, y top-N priorizado.

**Formato de respuesta.** Español, encabezados por área, tabla resumen al inicio.

**Checklist final.** ¿Cada hallazgo con archivo:línea? ¿Gates ejecutados y su resultado citado? ¿Severidades justificadas? ¿Limitaciones declaradas?

**Limitaciones.** Auditoría estática salvo los gates; no mide latencia real ni ejecuta contra DB.

**Trazabilidad.** `CLAUDE_ORGANIZAR_SKILLS_BACKEND.md` §11 + `docs/audit/revision-completa-backend-2026-07-21.md`.
