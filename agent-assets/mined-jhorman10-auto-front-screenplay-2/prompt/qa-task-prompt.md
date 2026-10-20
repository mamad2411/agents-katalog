---
description: 'Ejecuta el QA Agent con los 8 skills secuenciales para generar el plan de calidad completo basado en la spec aprobada.'
agent: QA Agent
---

Ejecuta el QA Agent completo con los 8 skills en secuencia.

**Feature**: ${input:featureName:nombre del feature en kebab-case}

**Instrucciones para @QA Agent:**

1. Lee `.github/docs/lineamientos/qa-guidelines.md` como primer paso
2. Lee la spec en `.github/specs/${input:featureName}.spec.md`
3. Ejecuta los 8 skills en orden estricto:
   - SKILL 1: `/test-strategy-planner`    → `docs/output/qa/test-strategy.md`
   - SKILL 2: `/gherkin-case-generator`   → `docs/output/qa/features/`
   - SKILL 3: `/risk-identifier`          → `docs/output/qa/risk-matrix.md`
   - SKILL 4: `/test-data-specifier`      → `docs/output/qa/data/test-data-catalog.md`
   - SKILL 5: `/critical-flow-mapper`     → `docs/output/qa/critical-flows.md`
   - SKILL 6: `/regression-strategy`     → `docs/output/qa/regression-plan.md`
   - SKILL 7: `/automation-flow-proposer` → `docs/output/qa/automation-roadmap.md`
   - SKILL 8: `/performance-analyzer`    → `docs/output/qa/performance-plan.md`
4. Genera reporte consolidado al finalizar

**Prerequisito:** Debe existir `.github/specs/${input:featureName}.spec.md` con estado APPROVED. Si no, ejecutar `/generate-spec` primero.
