# BA Trends Routing Index

## Summary

**One-sentence:** Read-only routing index of 2025-2026 BA trends (AI-enabled decisions, outcome-driven strategy, responsible innovation, operational resilience, digital trust, sustainability) mapped to internal methodology.

**One-paragraph:** Read-only routing index of 2025-2026 BA trends (AI-enabled decisions, outcome-driven strategy, responsible innovation, operational resilience, digital trust, sustainability) mapped to internal methodology. Captured as a versioned artefact downstream agents and reviewers consume without re-deriving rationale. Mechanism: typed input → bounded transformation → contract-checked output.

**Ефективно для:**

- Orientation для new senior BA: which trend → which methodology.
- Quarterly trend review session.
- Pre-engagement scoping — який trend dominates context.
- Sales / pre-sales positioning conversation.

## Applies If (ALL must hold)

- BA org wants alignment between external trends and internal methodology library.
- Trends inventory exists (≤8 trends for review period).
- Each trend can be mapped to internal methodology or 'no current coverage'.
- Report consumed by BA lead + sponsor.

## Skip If (ANY kills it)

- Tactical engagement with no strategic review.
- Trend list outdated by &gt;12 months — refresh first.
- Org without methodology library to route to.

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
| [[ba-strategic-partnership]] | Companion / upstream methodology |
| [[ba-planning]] | Sibling artefact in the same lifecycle |

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
| `templates/ba-trends-summary.json` | Skeleton artefact with required fields |
| `templates/_smoke-test.json` | Minimum viable filled artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ba-trends-summary.py` | Validate artefact against output-contract | After subagent returns; pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[ba-strategic-partnership]]
- [[ba-planning]]
- [[decision-analysis]]

## Decision tree

See `content/06-decision-tree.xml`. Routes on artefact-state signal to the active rule.
