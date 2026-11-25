---
name: backend-production
description: Coordina la implementación de features backend de producción en Atlas aplicando arquitectura por capas, validación Zod, persistencia transaccional, seguridad, pruebas, observabilidad y verificación con gates reales. Úsala para construir una feature end-to-end, no para auditar.
---

# backend-production

**Propósito.** Implementar una feature backend lista para producción respetando las reglas del proyecto.

**Cuándo usarla.** Para construir/extender un módulo o endpoint end-to-end.
**Cuándo NO.** Para auditar (usa `backend-hardening`) o arreglar un bug puntual (usa `/debug`).

**Fuentes obligatorias.** `.claude/rules/`, el módulo relacionado en `src/modules/`, el grafo graphify, `docs/audit/`, `package.json`.

**Entradas.** La feature (requisito/contrato). Si el contrato con el frontend importa, revisa `scripts/smoke/frontend-contract.smoke.ts`.

**Condiciones de parada.** Detente ante contradicción con un contrato vigente, necesidad de secretos/producción, o cambio destructivo de datos.

**Flujo por fases.**
1. Comprender: consulta el grafo (`graphify query/explain`) antes de tocar; ubica capas y límites.
2. Contrato: define DTO + schema Zod de entrada/salida.
3. Capas: `controller` (delgado, valida, delega) → `service` (lógica) → `repository` (persistencia) → `mapper` (a DTO). Nunca devolver modelos ORM.
4. Persistencia: transacción para flujos multi-tabla; idempotencia donde aplique (índice único + captura de `UniqueConstraintError`).
5. Seguridad: `@Throttle` en público, ownership/tenant guards, validación, redacción de PII persistida, cifrado de PII sensible.
6. Observabilidad: logs con contexto, métricas si es un flujo de negocio/worker.
7. Pruebas: spec unitario del service/repository + e2e si hay flujo crítico.
8. Migración si cambia el schema (up/down, expand/contract, gate de tamaño).
9. Verificación: skill `production-verification` (gates reales).
10. `graphify update .` tras modificar código.

**Comandos permitidos.** Edición, `graphify`, gates de verificación, `yarn test:*`, smokes locales.
**Comandos prohibidos.** Migraciones/seeds destructivos, `git push` sin aprobación, producción.

**Evidencia requerida.** Gates verdes (typecheck+tests+lint+build) con su salida; smoke del flujo si aplica.

**Entregables.** Código + pruebas + migración (si aplica) + reporte de verificación.

**Formato.** Resumen de cambios, decisiones, evidencia de gates.

**Checklist final.** ¿Capas respetadas? ¿DTO no expone ORM? ¿Transacción/idempotencia? ¿Seguridad y observabilidad? ¿Pruebas? ¿Gates verdes? ¿`graphify update`?

**Limitaciones.** No sustituye una auditoría de seguridad/rendimiento profunda; para eso usa las skills dedicadas.

**Trazabilidad.** `CLAUDE_ORGANIZAR_SKILLS_BACKEND.md` §11 (backend-production) + `.claude/rules/`.
