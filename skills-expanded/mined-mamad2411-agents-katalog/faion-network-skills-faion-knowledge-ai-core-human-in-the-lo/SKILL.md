# Human-in-the-Loop Design

## Summary

**One-sentence:** Spec for which AI decisions go to a human reviewer, how decisions are presented, how reviewer signals feed back into the model, and where the system blocks vs. proceeds.

**One-paragraph:** Spec for which AI decisions go to a human reviewer, how decisions are presented, how reviewer signals feed back into the model, and where the system blocks vs. proceeds. This methodology codifies the rules, output contract, failure modes, and decision tree needed for a spec produced by an agent applying human-in-the-loop design. The deliverable is validated against an explicit JSON Schema and routed through a decision tree that maps observable signals to rule ids in `01-core-rules.xml`.

**Ефективно для:**

- Building a reproducible spec for human-in-the-loop design across teams.
- Reviewing AI-or-human work against an explicit contract instead of vibes.
- Wiring the output into downstream automation (CI gates, observability, post-mortems).
- Avoiding the failure modes listed in `03-failure-modes.xml`.

## Applies If (ALL must hold)

- AI system makes decisions whose cost-of-error justifies a human review step (refund, content moderation, medical triage)
- humans review at meaningful volume (not just escalations) and the review UX must be designed
- reviewer feedback can flow back into model/prompt updates or routing rules

## Skip If (ANY kills it)

- AI decisions are low-stakes and rollback-cheap (autocomplete, ranking) — HITL is overhead
- review volume is zero or near-zero (only escalations) — design the escalation path instead
- review is purely audit (no decision changed by review) — use audit logging methodology

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Decision inventory + stakes per decision | table | product |
| Reviewer pool + capacity | headcount + hours/day | operations |
| Feedback loop target (model retrain / prompt refit / rule update) | policy | ml-engineering |
| Review SLA + escalation policy | policy | operations |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[eval-driven-development-tdd-for-ai]] | Eval gate for AI outputs that bypass review |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules grounding the methodology with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the deliverable + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix triplets | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 800 |
| `content/05-examples.xml` | essential | Worked example from real engagement | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decision_inventory_map` | sonnet | Map decisions to stakes + review need. |
| `review_ui_spec` | opus | Reviewer-facing UI spec + ergonomics. |
| `feedback_loop_design` | opus | How reviewer signals retrain / refit / route. |

## Templates

| File | Purpose |
|------|---------|
| `templates/hitl-spec.md.j2` | HITL spec skeleton |
| `templates/hitl-spec.md` | HITL spec skeleton Generated from `templates/hitl-spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/review-decision.json` | Review decision JSON schema |
| `templates/_smoke-test.md.j2` | Minimum viable filled-in HITL spec |
| `templates/_smoke-test.md` | Minimum viable filled-in HITL spec Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-human-in-the-loop-design.py` | Validate the spec artefact against the 02-output-contract schema | After subagent returns, before commit/publish |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[ai-feature-progressive-rollout]]
- [[ai-feature-incident-runbook]]
- [[eval-driven-development-tdd-for-ai]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals from inputs and intermediate artefacts to a rule from `01-core-rules.xml`, telling the agent which variant of the methodology to apply or when to stop. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.
