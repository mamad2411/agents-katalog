---
name: agent-contracts
description: Reference of all context slots, required vs optional declarations, and Evidence Quality standard.
triggers:
  [
    "context slot",
    "what does [agent] write",
    "context object",
    "agent outputs",
    "slot",
    "required slot",
    "optional slot",
    "evidence quality",
  ]
---

This skill documents the context slots agents read and write, the Evidence Quality standard, and the protocol for Required vs Optional slots.

Key v2.2 additions (ensure these appear in your machine-readable slot table):

- `business_model_type` (EventIQ confirms in W1 Step 1)
- `cohort_definition_method` (EventIQ — how cohorts are defined)
- `evidence_quality` (per-agent evidence rating)
- `outcome_tracking_id` (DecideWell)
- `metric_formula_map`, `okr_conflict_flags` (NorthStar)
- `network_effect_isolation_required` (HypothesisLab)

Evidence Quality Standard (copy from Playbook §4): sample size, recency, source, completeness; overall = lowest rating across criteria.

Required vs Optional protocol:

- Required: agent must block and state missing slots.
- Optional: agent proceeds but states how missing slot would improve quality.

Canonical slot table (51 slots): `schemas/context-slots.md`. Update that file when adding or renaming slots; update this skill's count to match.

v2.3 additions (6 new slots added to align schema with agent outputs):
- `regulatory_jurisdiction` — SetupGuide → DataLayer, NarrativeEngine
- `ranked_opportunity_list` — DiscoveryOS → RoadMap, NorthStar
- `research_synthesis_report` — DiscoveryOS → NarrativeEngine, OpsCommand
- `category_definition` — NarrativeEngine → LaunchPad, OpsCommand
- `audience_messaging_matrix` — NarrativeEngine → LaunchPad, OpsCommand
- `power_calculation` — HypothesisLab → DecideWell, Orchestrator
