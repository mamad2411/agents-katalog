# BPMN via AI then Human Review

## Summary

**One-sentence:** Two-pass BPMN authoring: LLM drafts BPMN 2.0 XML from process transcript, named SME reviews + signs + commits — never AI-only commit.

**One-paragraph:** Two-pass BPMN authoring: LLM drafts BPMN 2.0 XML from process transcript, named SME reviews + signs + commits — never AI-only commit. The artefact is captured as a versioned record (JSON or Markdown) downstream agents and reviewers consume without re-deriving rationale. Mechanism: typed input → bounded transformation → contract-checked output.

**Ефективно для:**

- Regulated-domain process modelling (FinTech KYC, AML, healthcare).
- Acceleration BA process drafting з мандатним human-gate.
- Audit-grade BPMN з sign-off trail.
- Migration / replatform — bulk current-state drafting.

## Applies If (ALL must hold)

- Process modelling required in regulated context.
- SME reachable for review within 5 working days of draft.
- BPMN XML must validate against schema.
- Audit trail (sign-off + diff) is required.

## Skip If (ANY kills it)

- Greenfield product with no current process.
- Non-regulated workflow where review overhead exceeds value.
- SME unavailable / disengaged.

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
| [[interface-analysis]] | Sibling artefact in the same lifecycle |

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
| `templates/bpmn-via-ai-then-human-review.json` | Skeleton artefact with required fields |
| `templates/_smoke-test.json` | Minimum viable filled artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-bpmn-via-ai-then-human-review.py` | Validate artefact against output-contract | After subagent returns; pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[business-process-analysis]]
- [[interface-analysis]]
- [[data-analysis]]

## Decision tree

See `content/06-decision-tree.xml`. Routes on artefact-state signals to the active rule. Use when in doubt whether the artefact is ready for downstream consumption.
