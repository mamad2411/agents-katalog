# AI Acceptance Criteria Generator Reviewer

## Summary

**One-sentence:** Reviewer rubric that scores LLM-drafted acceptance criteria across happy/negative/edge/perf/a11y dimensions and gates them on evidence + frozen weights.

**One-paragraph:** Modern BAs generate acceptance criteria with an LLM; the failure mode is half-baked AC slipping into the backlog. This methodology codifies the reviewer pass: a numeric 0-100 rubric with anchored dimensions (happy path, negative cases, edge cases, performance thresholds, accessibility), evidence-per-score discipline, frozen pre-scoring weights, and a reconciliation step when scores diverge. Output is a `rubric` artefact: `dimensions[]` + `instance_scores[]` + `weighted_total`.

**Ефективно для:**

- Reviewer pass на LLM-згенерованих acceptance criteria перед merge у backlog.
- Cohort comparison кількох AC варіантів від різних агентів / промптів.
- Audit trail для регульованих доменів — кожен score з evidence_ref.
- Calibration multi-rater сесії для P4 BA команди.

## Applies If (ALL must hold)

- LLM generates AC drafts at scale (≥3 stories/sprint) and a structured reviewer pass is required.
- Each criterion has a defined 1-5 anchor; raters trained on the rubric before scoring.
- Scores will be used for a binary decision (advance to dev, reject, rework).
- ≥2 raters per instance for any AC that gates a >$10k or strategic story.

## Skip If (ANY kills it)

- n < 3 AC sets — gut feel is faster and accuracy is similar.
- Decisions are single-criterion (deadline-only) — full rubric is overhead.
- One-off prototype AC that will be rewritten next sprint anyway.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| LLM-drafted AC set | Markdown / Gherkin | upstream story generator |
| Rubric anchors file | YAML / Markdown table | BA lead |
| Evidence pointers | URLs, doc paragraphs, trace IDs | story author / prompt log |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[acceptance-criteria]] | Canonical AC format (Gherkin / G-W-T) and INVEST checks |
| [[ai-elicitation-prompt-patterns]] | The prompt patterns whose output this rubric scores |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 4 testable rules: anchored scales, evidence per score, ≥2 raters for high-stakes, frozen weights | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | 700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: missing evidence, weight reverse-engineering, halo, generic anchors, single-rater high-stakes | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure: define dimensions → freeze weights → score with evidence → reconcile → emit composite | 700 |
| `content/06-decision-tree.xml` | essential | Routing on AC stakes + rater count → which rule fires | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `per_criterion_score` | sonnet | Anchored 1-5 judgment per dimension. |
| `evidence_extraction` | haiku | Mechanical pull of quoted evidence from drafts. |
| `multi_rater_reconciliation` | opus | Resolve divergent scores with rationale. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rubric.json` | Rubric skeleton with anchors_1_3_5 + weights + dimensions |
| `templates/_smoke-test.json` | Minimum viable filled-in rubric for one AC set |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-acceptance-criteria-generator-reviewer.py` | Validate emitted rubric against output-contract schema | CI on each rubric file; pre-commit gate |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[acceptance-criteria]]
- [[ai-elicitation-prompt-patterns]]
- [[ai-assisted-requirements-elicitation]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes on observable signals (AC stakes value, rater count, evidence completeness) to one of the 4 core rules. Use it when in doubt whether a single-rater pass suffices or reconciliation is required.
