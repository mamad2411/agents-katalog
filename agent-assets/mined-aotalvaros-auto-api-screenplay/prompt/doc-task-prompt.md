---
description: 'Ejecuta el Documentation Agent para generar documentación técnica completa del feature implementado (README, API docs, ADRs, onboarding).'
agent: Documentation Agent
---

Ejecuta el Documentation Agent (MARCO DOC) para generar la documentación técnica del feature.

**Feature**: ${input:featureName:nombre del feature en kebab-case}

**Instrucciones para @Documentation Agent:**

1. Lee `.github/docs/lineamientos/dev-guidelines.md`
2. Lee la spec aprobada en `.github/specs/${input:featureName}.spec.md`
3. Revisa el código implementado en `backend/app/` y `frontend/src/`
4. Genera los siguientes entregables:
   - Actualiza `README.md` con los cambios del feature
   - Genera documentación de API: `docs/output/api/api-reference.md`
   - Registra ADRs en `docs/output/adr/architecture_decision_records.md` (si aplica)
   - Genera docs de componentes Frontend: `docs/output/frontend/components/` (si aplica)
   - Actualiza guía de onboarding: `docs/output/onboarding-guide.md` (si aplica)
5. Presenta reporte consolidado de documentación generada

**Prerequisito:** Debe existir `.github/specs/${input:featureName}.spec.md` con estado APPROVED y código implementado. Si no, ejecutar `/generate-spec` y los marcos de implementación primero.
