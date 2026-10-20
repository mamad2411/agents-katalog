# Acceptance Criteria

## Summary

**One-sentence:** Explicit, testable Given-When-Then or rule-based criteria per user story with mapping to ≥1 test case and explicit edge / negative / non-functional coverage.

**One-paragraph:** Explicit, testable Given-When-Then or rule-based criteria per user story with mapping to ≥1 test case and explicit edge / negative / non-functional coverage. Captured as a versioned artefact downstream agents and reviewers consume without re-deriving rationale. Mechanism: typed input → bounded transformation → contract-checked output.

**Ефективно для:**

- Pre-sprint AC writing для кожної user story.
- Bug fixes: expected vs actual behavior documentation.
- Technical story success measurable (latency, throughput).
- Integration з BDD tooling (Cucumber, SpecFlow).

## Applies If (ALL must hold)

- User story enters sprint without AC.
- Output is consumed by QA + dev (test design + acceptance).
- Story is appropriately sized (≤8-10 AC per story).
- Domain context is reachable for clarification.

## Skip If (ANY kills it)

- Spike / research stories — output contract is the right artifact.
- System-level NFRs (SLOs, capacity) — belong in ADR / SLA.
- Pure infra / ops tasks with no user-visible behavior.
- Story with 30+ scenarios — split first.

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
| [[ai-acceptance-criteria-generator-reviewer]] | Companion / upstream methodology |
| [[use-case-modeling]] | Sibling artefact in the same lifecycle |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema + examples | 800 |
| `content/03-failure-modes.xml` | essential | Antipatterns | 800 |
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
| `templates/acceptance-criteria.json` | Skeleton artefact with required fields |
| `templates/_smoke-test.json` | Minimum viable filled artefact |
| `templates/ac-checklist.md.j2` | Checklist-form acceptance criteria — functional, validation, error-handling, performance and security criteria for one story. |
| `templates/ac-checklist.md` | Checklist-form acceptance criteria — functional, validation, error-handling, performance and security criteria for one story. Generated from `templates/ac-checklist.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

| `templates/ac-bdd.md.j2` | Given/When/Then acceptance-criteria skeleton for one story |
| `templates/ac-bdd.md` | Given/When/Then acceptance-criteria skeleton for one story Generated from `templates/ac-bdd.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-acceptance-criteria.py` | Validate artefact against output-contract | After subagent returns; pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[ai-acceptance-criteria-generator-reviewer]]
- [[use-case-modeling]]
- [[ai-assisted-requirements-elicitation]]

## Decision tree

See `content/06-decision-tree.xml`. Routes on artefact-state signal to the active rule.
