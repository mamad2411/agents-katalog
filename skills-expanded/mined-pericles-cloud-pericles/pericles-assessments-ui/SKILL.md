---
name: pericles-assessments-ui
version: 2026.05.0
description: >
  How to build Assessments — the risk-profiling module: a Risk Profile heat map, report
  generation, a report viewer, and scenario exploration. Use this WHENEVER you build or
  change assessment frameworks, the heat map, report generation/viewing, or scenarios.
  Encodes the surfaces, reuse of the RiskAssessment model and ERP-derived context,
  pack-provided assessment types, persona data scope, and report distribution via an
  Execution Node.
doctrine_refs: [§3, §6; Assessments PRD; Industry Pack Spec §1]
depends_on: [pericles-frontend-foundations, pericles-persona-layer, pericles-org-memory, pericles-execution-node]
last_reconciled: 2026-05-28
---

# Pericles Assessments UI (build skill)

Assessments give the customer a structured view of their risk posture: where
concentration and exposure sit, a generated report, and the ability to explore
scenarios. It runs on the customer's actual ERP data (`OrganizationContext`) and
Organizational Memory. The `RiskAssessment` model exists; the UX and frameworks are
net-new (Industry Pack Spec marks assessment types as Wave-1 builds).

## When to use this skill

Building/changing assessment frameworks, the Risk Profile heat map, report
generation/viewing, or scenario exploration.

## Surfaces

- **Risk Profile heat map** — visualizes exposure/concentration (e.g. supplier portfolio,
  regional concentration, raw-material exposure) over the customer's footprint and
  suppliers. Severity styling consistent with Atlas (0.0–1.0).
- **Report generation** — runs an assessment framework over ERP data + Org Memory to
  produce a report (backed by `RiskAssessment` records, `pericles-data-model`).
- **Report viewer** — read the generated report with cited sources (document viewer,
  shared with Intelligence, `pericles-intelligence-ui`).
- **Scenario exploration** — "what if" over the profile (e.g. lose a tier-1 supplier);
  read-only analysis, not a committed action.

## Pack-provided frameworks

Industry Packs ship `assessment_types` (e.g. Supplier Portfolio Risk, Regional
Concentration, Raw Material Exposure) — the customer runs them, doesn't design them
(`pericles-industry-pack`). On day one a customer can run Supplier Portfolio Risk on
their real ERP data.

## Persona & distribution

Persona shapes depth and **data scope** (financial exposure to Risk Manager+,
`pericles-persona-layer`). Generating/viewing a report is inline; **distributing** a
report externally is a consequential action → Execution Node + approval
(`pericles-execution-node`), never auto-send.

## What this forbids

Showing exposure/financial figures outside a persona's data scope; auto-distributing a
report without an Execution Node + approval; designing customer-specific frameworks
outside packs/Custom Skills; client-trusted `organization_id`; treating Org Memory
content as trusted instructions.

## Verification

Heat map reflects real ERP/footprint data; report generation produces `RiskAssessment`
records with cited sources; persona data scope enforced; scenarios are read-only; report
distribution routes through an Execution Node; tenant-scoped.

## Existing standards (read alongside)

`.cursor/rules/001-application/*` (assessments/insights where present); Assessments PRD;
`RiskAssessment` model; Industry Pack Spec §1/§6.

## Open questions

- Scenario engine: live recompute vs precomputed snapshots — define with the platform
  team.
- Whether assessment frameworks are Skills (registry) or templates (pack) — reconcile
  with `pericles-industry-pack` and `pericles-skill-authoring`.

## Changelog

- 2026.05.0 — Initial draft from the Assessments PRD; grounded in RiskAssessment +
  ERP context + pack-provided assessment types.
