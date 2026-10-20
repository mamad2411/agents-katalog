# AI Post-Mortem Template

## Summary

**One-sentence:** Post-mortem report template for incidents in AI features (hallucination, refusal, drift, eval miss) — root cause, contributing factors, action items keyed to AI-specific failure modes.

**One-paragraph:** Post-mortem report template for incidents in AI features (hallucination, refusal, drift, eval miss) — root cause, contributing factors, action items keyed to AI-specific failure modes. This methodology codifies the rules, output contract, failure modes, and decision tree needed for a report produced by an agent applying ai post-mortem template. The deliverable is validated against an explicit JSON Schema and routed through a decision tree that maps observable signals to rule ids in `01-core-rules.xml`.

**Ефективно для:**

- Building a reproducible report for ai post-mortem template across teams.
- Reviewing AI-or-human work against an explicit contract instead of vibes.
- Wiring the output into downstream automation (CI gates, observability, post-mortems).
- Avoiding the failure modes listed in `03-failure-modes.xml`.

## Applies If (ALL must hold)

- an AI feature incident has occurred (user-visible regression, hallucination cluster, drift detection, eval miss)
- the org runs blameless post-mortems and expects this incident to feed corrective actions
- the incident involves at least one LLM call in the failure path

## Skip If (ANY kills it)

- incident has no AI component (pure infra outage) — use ordinary infra post-mortem template
- incident is a single-user complaint with no signal of systemic issue — use ticket triage instead
- team does not own the affected AI feature — escalate to the owning team

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Incident timeline | tool / ticket / chat exports | incident commander |
| Affected prompt + model version | git SHA + model ID | ml-engineering |
| Eval suite history | scores + changes around incident date | ml-engineering |
| User-impact data | sessions affected + severity | product analytics |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[eval-driven-development-tdd-for-ai]] | Eval-suite discipline context |

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
| `timeline_assembly` | sonnet | Stitch tool / ticket / chat exports into single timeline. |
| `root_cause_analysis` | opus | AI-aware five-whys with hallucination / drift / refusal branches. |
| `action_item_drafting` | sonnet | Concrete, owner-assigned action items with due dates. |

## Templates

| File | Purpose |
|------|---------|
| `templates/post-mortem.md.j2` | Post-mortem report skeleton with AI-specific sections |
| `templates/post-mortem.md` | Post-mortem report skeleton with AI-specific sections Generated from `templates/post-mortem.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/action-items.json` | Action items JSON schema |
| `templates/_smoke-test.md.j2` | Minimum viable filled-in post-mortem |
| `templates/_smoke-test.md` | Minimum viable filled-in post-mortem Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-post-mortem-template.py` | Validate the report artefact against the 02-output-contract schema | After subagent returns, before commit/publish |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[eval-driven-development-tdd-for-ai]]
- [[ai-feature-incident-runbook]]
- [[ai-feature-observability-four-pillars]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals from inputs and intermediate artefacts to a rule from `01-core-rules.xml`, telling the agent which variant of the methodology to apply or when to stop. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.
