---
name: ns-pm-delivery-schedule
description: >
  (NS) Triple productivity delivery schedule — one markdown with three PERT +
  Monte Carlo tables for productivity scenarios P100 (current h/FP), P85
  (50% faster → ×0.50), P50 (85% faster → ×0.15). Section 0 = commercial
  summary + key delivery dates. Calendar percentiles P50/P85/P95 from
  pert_montecarlo.py only. Use when human asks cronograma, prazo, when we
  deliver, P50–P85–P95 de entrega, triple schedule, P100/P85/P50 produtividade,
  FP × hours/day capacity, or delivery dates after commercial FP sizing —
  even if they say "forecast" but supply FP + productivity (not story-level
  RICE/sprint). Do NOT invent R$. Do NOT replace ns-commercial-budget.
  Do NOT use for story-only PERT without FP (that is ns-project-manager Phase 5).
license: Apache-2.0
metadata:
  author: nextstage-brasil
  version: "1.2"
depends:
  - ns-harness
  - ns-project-manager
---

# Delivery Schedule — triple productivity (P100 / P85 / P50)

Produce **one** delivery-schedule markdown for a version (or remaining slices): three productivity scenarios, each with PERT phases + Monte Carlo **calendar** percentiles.

**Not** commercial FP quoting (`ns-commercial-budget`). **Not** story-level forecast alone (`ns-project-manager` Phase 5). **Never** invent R$.

## Critical naming (never conflate)

| Label | Meaning |
|-------|---------|
| **Productivity scenario P100** | Today's real productivity (baseline) — `h_fp = produtividade_atual` |
| **Productivity scenario P85** | Goal: **50% faster** — `h_fp = produtividade_atual × 0.50` |
| **Productivity scenario P50** | Goal: **85% faster** — `h_fp = produtividade_atual × 0.15` |
| **Delivery percentiles P50 / P85 / P95** | Monte Carlo calendar outcomes **inside** each productivity scenario |

P100 = reality. P85 and P50 productivity scenarios = **acceleration goals**, not Monte Carlo percentiles.

Faster formula: `horas_novas = horas_atuais × (1 − X/100)` → 50% faster ⇒ ×0.50; 85% faster ⇒ ×0.15.

## Harness discovery

Resolve `{product_root}` via `../ns-harness/references/harness-discovery.md` + `artifact-layout.md`. No harness → repo root. Ask once for `{version_san}` if missing.

## Language

- Skill + references: English.
- Deliverable: mirror the human (pt_BR default for NextStage commercial/PM docs). English only when human writes in English or asks.

## Workflow

### 1. Intake

Read `references/intake.md`.

Ask the human **only** for missing capacity + start (`horas_por_dia`,
`dias_uteis_por_semana`, `data_inicio`) — clear numbered questions, human
language (pt_BR default). Infer ceiling, phases, and O/M/P (mark
`[ASSUMPTION]`). Do not invent productivity, FP, or capacity/start. Do **not**
use a `[FILL IN]` form. Do **not** ask for estimativa experiencial unless the
human volunteers it.

### 2. Compute

Read `references/calculations.md`.

1. Derive `h_fp` for P100 / P85 / P50.
2. Scale remaining hours from remaining FP × `h_fp` (same phase structure and O/M/P **bands** across scenarios; only hours scale).
3. Convert hours → effort days (`hours ÷ hours_per_day`).
4. For **each** scenario, write `pert-config-p100.json` / `pert-config-p85.json` / `pert-config-p50.json` and run:

```bash
python3 ../ns-project-manager/scripts/pert_montecarlo.py pert-config-pNNN.json
```

(Adjust path if skills live under `.agents/skills/` or Cursor skills dir — sibling of `ns-project-manager`.)

5. Map MC effort-day percentiles to **business-day calendar** from start date. Never invent percentiles.

### 3. Write document

Read `references/document-structure.md`. Emit the full markdown in one pass (Section 0 first).

Default official commitment = **calendar P85 of productivity scenario P100**, unless human picks another.

### 4. Persist

Default base: `{product_root}/docs/versions/{version_san}/pm/`

| File | Role |
|------|------|
| `05-cronograma-tres-cenarios.md` | Main deliverable |
| `pert-config-p100.json` | MC input P100 |
| `pert-config-p85.json` | MC input P85 |
| `pert-config-p50.json` | MC input P50 |
| `roadmap.md` | Update with the three calendar-P85 dates |

Chat-only only if human says so. Confirm path once if persistence not yet agreed.

## Sibling routing

| Signal | Skill |
|--------|--------|
| Orçamento / FP / COSMIC / R$ | `ns-commercial-budget` |
| Story RICE / sprint / single PERT forecast | `ns-project-manager` Phase 3–5 |
| FP + productivity → triple delivery schedule | **this skill** |

## Out of scope

- SDD tasks, code execution, inventing R$ or FP.
- Treating productivity P50/P85/P100 as Monte Carlo percentiles without explanation.
- Acceleration factors other than 50% / 85% faster unless human explicitly overrides.

## Acceptance checklist

- [ ] Three PERT + MC tables: productivity P100 / P85 / P50
- [ ] P100 = current; P85 = ×0.50; P50 = ×0.15; text states P85/P50 are **goals**
- [ ] Section 0 first: commercial summary + delivery-date summary table
- [ ] Final comparative table; headers name productivity vs calendar percentiles
- [ ] Delivery percentiles from `pert_montecarlo.py` only
- [ ] Human language (pt_BR default)

## File index

| File | When |
|------|------|
| `references/intake.md` | Missing inputs |
| `references/calculations.md` | Before MC / calendar math |
| `references/document-structure.md` | Before writing markdown |
| `../ns-project-manager/scripts/pert_montecarlo.py` | Every scenario MC run |
