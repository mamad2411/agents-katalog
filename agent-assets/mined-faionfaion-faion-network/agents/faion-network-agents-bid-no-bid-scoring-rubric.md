# Bid / No-Bid Scoring Rubric

## Summary

**One-sentence:** Pre-bid 0-100 weighted rubric across 6 dimensions (fit / margin / risk / timeline / team / strategic) with go/no-go threshold and named approver.

**One-paragraph:** Pre-bid 0-100 weighted rubric across 6 dimensions (fit / margin / risk / timeline / team / strategic) with go/no-go threshold and named approver. The artefact is captured as a versioned record (JSON or Markdown) downstream agents and reviewers consume without re-deriving rationale. Mechanism: typed input → bounded transformation → contract-checked output.

**Ефективно для:**

- Pre-bid discovery for fixed-price engagement (P4).
- Pipeline triage коли inbound RFPs &gt; capacity.
- Cross-team alignment перед commitment.
- Audit trail для quarterly win/loss review.

## Applies If (ALL must hold)

- RFP / opportunity is fixed-price or substantial scope.
- Decision involves multiple stakeholders (sales / delivery / finance).
- Bid effort itself costs more than $5k.
- Win/loss can be tracked downstream.

## Skip If (ANY kills it)

- Tiny opportunity (under $5k, low bid effort).
- Existing-client expansion already committed.
- Pure-T&M staffing where rubric overhead exceeds bid effort.

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
| [[decision-analysis]] | Companion / upstream methodology |
| [[ai-acceptance-criteria-generator-reviewer]] | Sibling artefact in the same lifecycle |

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
| `templates/bid-no-bid-scoring-rubric.json` | Skeleton artefact with required fields |
| `templates/_smoke-test.json` | Minimum viable filled artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-bid-no-bid-scoring-rubric.py` | Validate artefact against output-contract | After subagent returns; pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[decision-analysis]]
- [[ai-acceptance-criteria-generator-reviewer]]
- [[ba-planning]]

## Decision tree

See `content/06-decision-tree.xml`. Routes on artefact-state signals to the active rule. Use when in doubt whether the artefact is ready for downstream consumption.
