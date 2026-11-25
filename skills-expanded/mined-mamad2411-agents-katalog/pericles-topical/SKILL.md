---
name: pericles-topical-skill
version: 2026.05.0
description: >
  How to author a Topical Skill — a single-domain monitoring/knowledge capability —
  and lift the existing monitoring tools into the registry as Topical Skills. Use this
  WHENEVER you create or version a Topical Skill (weather, political risk,
  cybersecurity, maritime, etc.) or convert one of the 10 data-source monitor tools.
  Encodes what a Topical Skill is, the lift mapping (tool → topical/<domain>),
  knowledge_sources declaration, and reuse of the existing scorers.
doctrine_refs: [§1, §5; Manifest Spec; Industry Pack Spec §1, §6]
depends_on: [pericles-skill-authoring, pericles-mastra-tool, pericles-functional-agent]
last_reconciled: 2026-05-28
---

# Pericles Topical Skill (build skill)

A **Topical Skill** monitors one risk domain and returns structured candidate events
for that domain. Topical Skills are the broadest, most-reused layer — they feed
`pre_validation` Functional Skills and are bundled into Industry Packs. The 10
data-source monitor tools in `backend/src/mastra/tools/` are Topical Skills waiting to
be lifted (`pericles-skill-authoring`); the Industry Pack Spec targets **11 Topicals,
10 of which already exist**.

## When to use this skill

Creating/versioning a Topical Skill; lifting a monitor tool; adding a new risk domain.

## What a Topical Skill is (and isn't)

- It establishes domain signal: "what weather/political/cyber events are happening near
  the org's footprint." It returns schema-validated candidate events, never actions.
- It is **not** a Functional Agent — it does not orchestrate or decide the pipeline. A
  `pre_validation` Functional Skill (e.g. Monitoring) composes Topicals
  (`pericles-functional-agent`).
- It declares `knowledge_sources`, not `data_access.pattern` (that field is for
  Functional Skills).

## The lift mapping (tool → Topical Skill)

| Mastra tool file | Topical Skill ID |
|---|---|
| weather-disaster-monitor-tool.ts | topical/weather-disaster |
| political-risk-monitor-tool.ts | topical/political-risk |
| cybersecurity-monitor-tool.ts | topical/cybersecurity |
| economic-financial-monitor-tool.ts | topical/economic-financial |
| news-social-media-monitor-tool.ts | topical/news-social |
| maritime-logistics-monitor-tool.ts | topical/maritime-logistics |
| labor-social-monitor-tool.ts | topical/labor-social |
| regulatory-trade-monitor-tool.ts | topical/regulatory-trade |
| pandemic-health-monitor-tool.ts | topical/pandemic-health |
| geopolitical-conflict-monitor-tool.ts | topical/geopolitical-conflict |
| *(not yet built)* | topical/commodities — Wave 1 net-new |

The 3 infrastructure tools (`organizationLookup`, `incidentLookup`, `erpContext`) and
the SAP ERP tools (`sapGetMaterialStock`, `sapGetShippingLanes`, …) are **not** Topical
Skills — they're infrastructure / ERP access (`pericles-erp-adapter`).

## Authoring / lifting steps

1. Add `topical/<domain>@YYYY.MM.N` with `mastra_tool_ref` to the existing file — no
   code change.
2. Declare `knowledge_sources` (e.g. NOAA, NASA EONET for weather), marking the
   existing inlined integrations `grandfathered_inline`; route any **new** source via
   MCP (§5, `pericles-mcp-layer`).
3. Set `eval_criteria` to the existing scorers (`relevanceScorer`,
   `severityAccuracyScorer`, `deduplicationScorer`) with thresholds.
4. Confirm the output schema is the candidate-event shape the pipeline expects
   (`pericles-monitoring-pipeline`).
5. Set lifecycle `published` once evals pass.

## What this forbids

A Topical Skill that orchestrates the pipeline or commits actions; inlining a NEW data
source instead of using MCP; a Topical Skill that returns free-form text instead of
schema-validated candidate events; embedding a Topical fork inside an Industry Pack
(packs reference shared Topicals — Industry Pack Spec §10).

## Verification

`mastra_tool_ref` resolves; `knowledge_sources` declared; output is schema-valid
candidate events; scorers run; the registry accepts it and Industry Pack manifests can
reference it by ID (`pericles-industry-pack`).

## Existing standards (read alongside)

Industry Pack Spec §1/§6; the 10 monitor tools; `.claude/rules/03-agents.md` (risk
categories table), `04-tools.md`.

## Open questions

- The 11th Topical (`topical/commodities`) is net-new — confirm its data sources before
  authoring.
- Whether `news-social` maps to the rule's `REALTIME_MONITOR` naming — align IDs with
  `.claude/rules/03-agents.md`.

## Changelog

- 2026.05.0 — Initial draft; lift table grounded in the real tool exports and the
  Industry Pack Spec's "10 of 11 Topicals exist" note.
