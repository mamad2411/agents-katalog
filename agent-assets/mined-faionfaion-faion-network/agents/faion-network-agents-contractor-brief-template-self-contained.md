# Contractor Brief Template (Self-Contained)

## Summary

**One-sentence:** A self-contained contractor brief carrying all context, deliverable spec, AC, evidence checkpoints, and payment terms a subcontractor needs to execute without follow-up questions.

**One-paragraph:** Subcontractor briefs that link out to '6 wikis and a Notion doc' fail: the contractor doesn't have access, the doc rots, the deliverable misses scope. Self-contained briefs inline every piece of context (background, deliverable shape, AC, evidence checkpoints, rate + payment terms, escalation owner). Output: a single Markdown artefact the contractor signs off and the founder pays against.

**Ефективно для:**

- Solo-founder / micro-agency engagements with external contractors.
- Short-cycle (1–4 week) deliverables with fixed price.
- Engagements where the contractor has no access to internal systems.
- Re-engagements after a previous failed contractor cycle.

## Applies If (ALL must hold)

- the deliverable shape is well-defined enough to write AC
- named escalation owner exists (the founder or a delegate)
- rate + payment terms are agreed
- engagement length ≤ 4 weeks (longer engagements need an ongoing collaboration spec)

## Skip If (ANY kills it)

- the deliverable is exploratory / discovery — switch to a discovery sprint brief
- internal-employee work — use the standard story template
- rate or scope not yet agreed — finalise before drafting the brief

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| deliverable description | MD / ticket | founder / BA |
| AC drafted | MD | founder / BA |
| rate + payment terms | contract | founder / legal |
| named escalation owner | org chart | founder |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[definition-of-done-library]] | Source of canonical AC patterns. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: self-contained (no external links to gated docs), AC ≥3 per deliverable, evidence checkpoints, named escalation owner, rate + payment terms inline | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for contractor brief: context, deliverable, AC, evidence, terms, owner | 700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes: links to gated docs, AC missing, evidence-checkpoint missing, owner anonymous, terms ambiguous | 900 |
| `content/04-procedure.xml` | essential | 4-step procedure: assemble context → write AC → set evidence checkpoints → finalise terms | 600 |
| `content/05-examples.xml` | essential | Worked example: '2-week landing-page refresh' brief excerpt | 500 |
| `content/06-decision-tree.xml` | essential | Tree on deliverable definiteness + access + engagement length | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | Template fill. |
| `synthesize_decision` | sonnet | Per-deliverable spec authoring. |
| `review_for_compliance` | opus | High-stakes engagements with regulatory or IP risk. |

## Templates

| File | Purpose |
|------|---------|
| `templates/contractor-brief-template-self-contained.json` | JSON skeleton for the brief. |
| `templates/contractor-brief-template-self-contained.md.j2` | Markdown skeleton with required fields. |
| `templates/contractor-brief-template-self-contained.md` | Markdown skeleton with required fields. Generated from `templates/contractor-brief-template-self-contained.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Minimum viable brief. |
| `templates/_smoke-test.md` | Minimum viable brief. Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-contractor-brief-template-self-contained.py` | Validates the contractor brief against the JSON Schema. | Before brief is sent to contractor; pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[definition-of-done-library]]
- [[decision-options-memo-template]]
- [[cr-impact-memo-template]]
- [[decision-rationale-capture]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input completeness, ownership clarity, regulatory context, scope size) to a rule from `01-core-rules.xml`. Use it when in doubt about whether to run, skip, or split this methodology.
