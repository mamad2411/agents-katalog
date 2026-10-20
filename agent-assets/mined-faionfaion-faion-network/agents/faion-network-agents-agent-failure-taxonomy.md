# Agent Failure Taxonomy

## Summary

**One-sentence:** Produces a shared agent-failure taxonomy: one primary label per incident from a closed vocabulary (hallucination / reasoning-shortfall / tool-misuse / context-overflow / injection / drift), each la...

**One-paragraph:** Without a shared vocabulary (hallucination vs reasoning-shortfall vs tool-misuse vs context-overflow vs injection vs drift) postmortems are ad-hoc and regression evals are not reusable across teams. P7's strategic-AI-narrative requires faion to own this taxonomy before competitors do. Output: labelled list, per-label remediation lane, append-only re-classification policy.

**Ефективно для:** incident triage, dashboard aggregation, regression-eval reusability across teams, executive reporting on agent quality.

## Applies If (ALL must hold)

- You triage incidents, issues, or failures and need a shared label set
- Labels feed dashboards or postmortems — consistent classification matters more than perfect labels
- Mis-classification cost (wrong remediation path) is bounded — labels are not safety-critical
- Taxonomy is versioned; new categories require explicit approval, not ad-hoc creation

## Skip If (ANY kills it)

- Failure modes still being discovered — premature labels lock in wrong categories
- Pre-incident exercises with no real data yet
- Single-incident retros where one-off detail matters more than aggregation

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| ≥10 incident records OR trace samples | Markdown or JSONL | observability + postmortems |
| Owner / approver for taxonomy | person | engineering lead |
| Remediation-lane catalogue | list | team |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[agent-postmortem-template]]` | Postmortem records consumed taxonomy labels |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale and source | ~550 |
| `content/02-output-contract.xml` | essential | JSON-schema output shape + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | medium | 5-step procedure with input/action/output per step | ~900 |
| `content/06-decision-tree.xml` | essential | decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Label single incident | sonnet | Pattern match. |
| Propose new label | opus | Cross-incident reasoning. |
| Map label → lane | opus | Process-design judgement. |

## Templates

| File | Purpose |
|------|---------|
| `templates/_smoke-test.md.j2` | Filled example with 6 default labels. |
| `templates/_smoke-test.md` | Filled example with 6 default labels. Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agent-failure-taxonomy.py` | Validates an output document against the 02-output-contract schema. | Pre-commit and CI before merge. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/ai/ai-agents/`
- `[[agent-postmortem-template]]`
- `[[agent-drift-detection-statistical]]`
- `[[agent-eval-test-set-curation]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether agent-failure-taxonomy applies: root question — "Are you triaging an agent incident or building label aggregation?". Branches lead to a specific core rule (e.g., `rule:r1`) when the methodology fits, or to a `skip:` conclusion when it does not.
