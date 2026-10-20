# BA to QA Handoff Template

## Summary

**One-sentence:** Sprint-end BA → QA handoff packet (story, AC count, fixture refs, edge cases, named QA owner) replacing ad-hoc verbal/Slack handoffs.

**One-paragraph:** Sprint-end BA → QA handoff packet (story, AC count, fixture refs, edge cases, named QA owner) replacing ad-hoc verbal/Slack handoffs. The artefact is captured as a versioned record (JSON or Markdown) downstream agents and reviewers consume without re-deriving rationale. Mechanism: typed input → bounded transformation → contract-checked output.

**Ефективно для:**

- Sprint review handoff від BA до QA коли AC stable.
- Multi-BA → multi-QA scaling: типована структура.
- Audit trail для regulated domains (banking, healthcare).
- Async handoff коли BA + QA в різних timezones.

## Applies If (ALL must hold)

- Sprint has ≥1 story moving from BA-AC-ready to QA-test-design.
- QA owns test design + execution downstream.
- AC are stable (not changing mid-handoff).
- Named QA reviewer reachable for handshake.

## Skip If (ANY kills it)

- Solo dev wearing QA hat.
- Same person is BA + QA.
- Spike / prototype with no QA pass.

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
| [[acceptance-criteria]] | Companion / upstream methodology |
| [[ba-standup-script-template]] | Sibling artefact in the same lifecycle |

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
| `templates/ba-to-qa-handoff-template.json` | Skeleton artefact with required fields |
| `templates/_smoke-test.json` | Minimum viable filled artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ba-to-qa-handoff-template.py` | Validate artefact against output-contract | After subagent returns; pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[acceptance-criteria]]
- [[ba-standup-script-template]]
- [[ai-acceptance-criteria-generator-reviewer]]

## Decision tree

See `content/06-decision-tree.xml`. Routes on artefact-state signals to the active rule. Use when in doubt whether the artefact is ready for downstream consumption.
