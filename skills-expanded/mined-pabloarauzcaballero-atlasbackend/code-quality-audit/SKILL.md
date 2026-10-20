---
name: code-quality-audit
description: Auditoría periódica de calidad de un módulo o repo — qué medir (complejidad, duplicación, cobertura, muerto, deps, seguridad), cómo encontrar hotspots por churn × complejidad, cómo priorizar hallazgos por impacto y cómo entregar un reporte con acciones concretas y dueños en vez de una lista de quejas. Usar al evaluar la salud de un repo heredado, antes de decidir refactorizar vs reescribir, al hacer due diligence técnica, o en una revisión de calidad trimestral.
allowed-tools: Read Grep Glob Bash
effort: high
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Auditoría de calidad — diagnóstico con acciones, no una lista de quejas

Una auditoría útil termina en un plan priorizado con dueños, no en un PDF que nadie
abre. Es solo lectura: observás y reportás, no arreglás (eso es otro trabajo, guiado por
`refactoring-safely` y `technical-debt-management`). Toda afirmación va con evidencia
medida — un número o un archivo:línea — nunca una impresión (`evidence-and-verification`).

## 1. Qué medir (y con qué skill hermana)

| Dimensión | Herramienta | Skill |
|---|---|---|
| Complejidad / hotspots | eslint complexity, Sonar, git churn | `code-complexity-metrics` |
| Duplicación / muerto / ciclos | jscpd, knip, madge | `dead-code-duplication` |
| Cobertura y calidad de tests | reporter del runner, mutation | `unit-testing`, `qa-strategy` |
| Dependencias y vulnerabilidades | `yarn npm audit`, Dependabot | `dependency-management`, `github-security-features` |
| Lint / tipos | ESLint, `tsc` | `static-analysis-linting`, `typescript-standards` |
| Arquitectura | ciclos, imports entre capas, tamaño de módulos | `solid-principles`, `backend-development` |
| Seguridad | revisión con lente de seguridad | `security-guardrails` |

## 2. Empezá por los hotspots, no por la A a la Z

Auditar todo por igual desperdicia el tiempo. Localizá dónde se concentra el riesgo:

```bash
# ✅ archivos más modificados en 6 meses = donde el equipo gasta y se equivoca más
git log --since="6 months ago" --name-only --pretty=format: \
  | grep '\.ts$' | sort | uniq -c | sort -rn | head -25
```

Cruzá churn con complejidad: la intersección (cambia seguido **y** es complejo) es donde
la auditoría rinde. Un módulo horrible pero congelado va al fondo de la lista.

## 3. Priorizar hallazgos: impacto, no gusto

Cada hallazgo se clasifica por **impacto × esfuerzo**:

- **Crítico** (arreglar ya): riesgo de seguridad, pérdida de datos, bug latente en flujo
  clínico/financiero, ausencia total de tests en un módulo central.
- **Alto** (planificar): hotspot complejo sin tests, duplicación de regla de negocio,
  deuda con interés alto.
- **Medio / bajo**: estilo, nombres, deuda de bajo interés → boy scout, no proyecto.

No mezcles "esto me gustaría distinto" con "esto es un riesgo": la credibilidad del
reporte depende de esa separación.

## 4. El reporte: accionable o inútil

Cada hallazgo lleva: **qué** (con archivo:línea o métrica), **por qué importa** (impacto
concreto, no "es feo"), **acción** propuesta, **esfuerzo** estimado y **dueño** sugerido.
Los hallazgos accionables se convierten en ítems (`technical-debt-management`,
`github-issues-projects`), no quedan en prosa.

```md
### [ALTO] `billing/invoice.service.ts` — regla de impuestos duplicada en 3 lugares
Evidencia: jscpd marca 47 líneas clonadas con quote.service.ts:88 y credit.service.ts:120.
Impacto: un cambio de tasa exige tocar 3 archivos; ya divergieron (bug #198).
Acción: extraer `TaxCalculator` con tests. Esfuerzo: ~1 día. Dueño: equipo Contabilidad.
```

## 5. Refactorizar vs reescribir

La pregunta que a veces motiva la auditoría. Guía: reescribir es casi siempre la opción
equivocada (perdés el conocimiento incrustado en el código viejo y los bugs ya resueltos).
Recomendá reescritura solo con datos duros: no compila el stack, sin tests posibles,
dependencias muertas sin upgrade. Por defecto: estrangulamiento incremental
(`refactoring-safely`).

## Anti-patrones
- Reporte de 200 hallazgos sin prioridad → parálisis.
- Mezclar preferencias estéticas con riesgos reales.
- Métricas sin acción ni dueño.
- Auditar el repo entero uniforme en vez de ir a los hotspots.
- Recomendar "reescribir todo" sin evidencia dura.

## Checklist
- [ ] Cubriste las dimensiones de §1 con herramienta y salida real, no impresiones.
- [ ] Priorizaste por hotspots (churn × complejidad), no alfabéticamente.
- [ ] Cada hallazgo tiene severidad por impacto × esfuerzo.
- [ ] El reporte separa riesgos de preferencias.
- [ ] Cada hallazgo accionable salió como ítem con dueño.

## Evidencia / DoD
Pegá la **salida literal** de las herramientas corridas (knip, jscpd, madge, audit,
cobertura, el `git log` de churn) y, para cada hallazgo, la referencia archivo:línea o la
métrica que lo respalda. Una auditoría sin salidas pegadas es una opinión, no un
diagnóstico. Declará qué NO auditaste (módulos fuera de alcance, dimensiones sin medir).
