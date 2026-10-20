# Benefit Sustainment Checklist

## Summary

**One-sentence:** Post-launch 90-day checklist verifying realized benefits match projected business case (metric, target, measured-value, variance, named owner).

**One-paragraph:** Post-launch 90-day checklist verifying realized benefits match projected business case (metric, target, measured-value, variance, named owner). The artefact is captured as a versioned record (JSON or Markdown) downstream agents and reviewers consume without re-deriving rationale. Mechanism: typed input → bounded transformation → contract-checked output.

**Ефективно для:**

- Post-launch 30/60/90 day benefits review.
- Process-improvement initiative ROI tracking.
- Compliance audit показуючи realized vs projected outcomes.
- Continuous-improvement loop coли наступний investment thresholded на попередньому result.

## Applies If (ALL must hold)

- Feature/process change shipped with documented business-case targets.
- Measurement infrastructure can capture the target metric.
- Named owner accountable for sustainment.
- Review cadence fits within 30/60/90 day frame.

## Skip If (ANY kills it)

- Spike / prototype with no business-case targets.
- Already-sunset initiative.
- Measurement infrastructure missing and unreachable.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Recent task context (30 days) | Markdown / tracker | BA |
| Write access to artefact store | repo / wiki | engagement manager |
| Named downstream owner | stakeholder list | BA |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[business-process-analysis]] | Companion / upstream methodology |
| [[decision-analysis]] | Sibling artefact in the same lifecycle |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 4-5 testable rules | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema + examples | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | Mechanical template fill. |
| `synthesize_decision` | sonnet | Per-instance bounded judgment. |
| `review_for_compliance` | opus | Cross-input synthesis on high-stakes outputs. |

## Templates

| File | Purpose |
|------|---------|
| `templates/benefit-sustainment-checklist.json` | Skeleton artefact with required fields |
| `templates/_smoke-test.json` | Minimum viable filled artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-benefit-sustainment-checklist.py` | Validate artefact against output-contract | After subagent returns; pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[business-process-analysis]]
- [[decision-analysis]]
- [[ba-planning]]

## Decision tree

See `content/06-decision-tree.xml`. Routes on artefact-state signals to the active rule. Use when in doubt whether the artefact is ready for downstream consumption.
