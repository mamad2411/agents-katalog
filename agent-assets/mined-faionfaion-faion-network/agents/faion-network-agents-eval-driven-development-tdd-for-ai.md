# Eval-Driven Development: TDD for AI

## Summary

**One-sentence:** Playbook step that enforces TDD discipline for AI features — write eval before prompt change, gate CI on regression, treat eval suite as production code, drift watch with sunset criterion.

**One-paragraph:** Playbook step that enforces TDD discipline for AI features — write eval before prompt change, gate CI on regression, treat eval suite as production code, drift watch with sunset criterion. This methodology codifies the rules, output contract, failure modes, and decision tree needed for a playbook-step produced by an agent applying eval-driven development: tdd for ai. The deliverable is validated against an explicit JSON Schema and routed through a decision tree that maps observable signals to rule ids in `01-core-rules.xml`.

**Ефективно для:**

- Building a reproducible playbook-step for eval-driven development: tdd for ai across teams.
- Reviewing AI-or-human work against an explicit contract instead of vibes.
- Wiring the output into downstream automation (CI gates, observability, post-mortems).
- Avoiding the failure modes listed in `03-failure-modes.xml`.

## Applies If (ALL must hold)

- team ships AI features (prompts, agents, RAG, fine-tunes) into a product where regressions are user-visible or cost-visible
- a change to prompt / model / retrieval / tool schema happens at least monthly
- team can wire eval execution into CI and gate merges on a configurable threshold

## Skip If (ANY kills it)

- one-shot prototype with no plan to ship, no users, no rollback need
- feature is fully deterministic (rule-based, no LLM) and unit tests fully capture behaviour
- no inference-cost budget for eval runs and no cached/mock plan exists — fix the budget first

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| CI system that can run eval jobs | GitHub Actions / GitLab CI / Jenkins | platform |
| Eval harness (golden set + scoring function) | code + data | ml-engineering |
| Inference budget (or cache plan) for eval runs | monthly cost cap | finance |
| Suite ownership policy | named team / individual | engineering manager |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[ai-feature-observability-four-pillars]] | Drift detection feeds back into eval refresh |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules grounding the methodology with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the deliverable + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix triplets | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `eval_authoring` | opus | Write eval cases + rubric for new feature. |
| `regression_analysis` | sonnet | Diagnose stratum-level regressions in PR delta. |
| `drift_review` | sonnet | Monthly suite-discrimination review. |

## Templates

| File | Purpose |
|------|---------|
| `templates/eval-spec.md.j2` | Eval suite spec skeleton |
| `templates/eval-spec.md` | Eval suite spec skeleton Generated from `templates/eval-spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/eval-delta.md.j2` | PR description eval-delta template |
| `templates/eval-delta.md` | PR description eval-delta template Generated from `templates/eval-delta.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Minimum viable filled-in eval spec |
| `templates/_smoke-test.md` | Minimum viable filled-in eval spec Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-eval-driven-development-tdd-for-ai.py` | Validate the playbook-step artefact against the 02-output-contract schema | After subagent returns, before commit/publish |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[ai-feature-observability-four-pillars]]
- [[ai-call-site-inventory]]
- [[ai-post-mortem-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals from inputs and intermediate artefacts to a rule from `01-core-rules.xml`, telling the agent which variant of the methodology to apply or when to stop. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.
