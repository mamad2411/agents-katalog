# Model Migration Checklist

## Summary

**One-sentence:** Produces a model-provider/generation migration checklist — typed input set, named owner, traceable decisions, version + last_reviewed for staleness.

**One-paragraph:** Migrating LLM provider or model generation rarely fails on the SDK; it fails on the prompt, the eval, and the unspoken assumptions. This methodology turns the migration into a typed artefact: input list (current model, target model, prompt set, gold eval, cost band, latency band), named owner, decisions traceable to those inputs, and a `last_reviewed` field. Output is a checklist a downstream engineer can execute or audit without re-deriving the rationale.

**Ефективно для:** ML-engineer, що мігрує OpenAI → Anthropic / Sonnet → Opus / GPT-4o → Gemini і хоче явну, ревьюваєму, ownable migration plan замість wiki-page heroics.

## Applies If (ALL must hold)

- Task is "migrate LLM provider or model generation" with production traffic at stake.
- Inputs (current model, target, prompt set, gold eval, cost/latency bands) are available.
- Downstream consumer (executor or auditor) will read the artefact.
- Tier == geek.

## Skip If (ANY kills it)

- Team already maintains a working checklist for this gap.
- Greenfield prototype with no production users.
- Regulatory / compliance overrides in-methodology guidance.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Current model + sha-pinned prompt set | doc | repo |
| Target model id | string | architecture decision |
| Gold eval (≥30 hand-labelled items) | JSONL | eval repo |
| Cost + latency band targets | YAML | finops / SLO |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `geek/ai/llm-integration/model-onboarding-checklist` | Sibling: onboarding a new model. |
| `geek/ai/ml-engineer/model-evaluation` | Defines the eval the migration must satisfy. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 rules: bound scope, typed input, named owner, versioned + last_reviewed, traceable decision. | ~900 |
| `content/02-output-contract.xml` | essential | Schema for the migration checklist. | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: invented inputs, plural owner, post-hoc rationale, stale record, missing eval baseline. | ~900 |
| `content/06-decision-tree.xml` | essential | Routes by input completeness + downstream consumer. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `draft_inputs_summary` | haiku | Template fill. |
| `synthesize_decision` | sonnet | Per-instance migration judgement. |
| `review_for_compliance` | opus | Cross-input synthesis. |

## Templates

| File | Purpose |
|---|---|
| `templates/model-migration-checklist.json` | JSON schema for the output contract. |
| `templates/model-migration-checklist.md.j2` | Markdown skeleton with required fields. |
| `templates/model-migration-checklist.md` | Markdown skeleton with required fields. Generated from `templates/model-migration-checklist.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-model-migration-checklist.py` | Enforce output contract. | After subagent return, before consumer reads. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/ai/ml-engineer/`
- upstream playbook: `role-ml-engineer/Migrate LLM provider / model generation`

## Decision tree

The tree at `content/06-decision-tree.xml` triages: typed input set + named owner + downstream consumer? → ship the checklist; otherwise → skip + escalate. Walk it before authoring so the migration plan is owned and auditable.
