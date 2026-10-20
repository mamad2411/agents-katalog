# Model Upgrade Checklist

## Summary

**One-sentence:** Produces a model/provider upgrade safety checklist — typed input set, named owner, traceable decisions, eval gate, rollout policy, version + last_reviewed.

**One-paragraph:** Upgrading a model in production (Sonnet 4.5 → 4.6, GPT-4o → GPT-4.1) is non-trivial: subtle quality regressions, prompt-cache cache-busting, output format drift. This methodology produces a typed checklist with the inputs that justified the upgrade (prompt set, gold eval, cost band, latency band), a named owner, an eval gate, a rollout policy with kill-switch, and a `last_reviewed` field. Output is auditable and re-runnable on the next upgrade.

**Ефективно для:** ML-engineer, що піднімає prod-модель на нову версію і потребує явного safety pass з eval gate + rollout discipline + named owner.

## Applies If (ALL must hold)

- Task is "upgrade existing prod model to new generation / version".
- Inputs (current model id, target version, prompt set, gold eval, cost/latency bands) are available.
- Downstream consumer (executor or auditor) will read the artefact.
- Tier == geek.

## Skip If (ANY kills it)

- Team already maintains a working checklist for this upgrade.
- Greenfield prototype with no production users.
- Regulatory / compliance overrides in-methodology guidance.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Current model id + sha-pinned prompt set | doc | repo |
| Target model version | string | vendor changelog |
| Gold eval (≥30 hand-labelled items) | JSONL | eval repo |
| Cost + latency band targets | YAML | finops / SLO |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `geek/ai/model-migration-checklist` | Sibling: full provider migration. |
| `geek/ai/ml-engineer/model-evaluation` | Defines the eval the upgrade must satisfy. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 rules: bound scope, typed input, named owner, versioned + last_reviewed, traceable decision. | ~900 |
| `content/02-output-contract.xml` | essential | Schema for the upgrade checklist. | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: invented inputs, plural owner, post-hoc rationale, stale record, no eval baseline. | ~900 |
| `content/06-decision-tree.xml` | essential | Routes by input completeness + downstream consumer. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `draft_inputs_summary` | haiku | Template fill. |
| `synthesize_decision` | sonnet | Per-instance upgrade judgement. |
| `review_for_compliance` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|---|---|
| `templates/model-upgrade-checklist.json` | JSON schema for the output contract. |
| `templates/model-upgrade-checklist.md.j2` | Markdown skeleton with required fields. |
| `templates/model-upgrade-checklist.md` | Markdown skeleton with required fields. Generated from `templates/model-upgrade-checklist.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-model-upgrade-checklist.py` | Enforce output contract. | After subagent return, before consumer reads. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/ai/ml-engineer/`
- upstream playbook: `role-ml-engineer/Model / provider upgrade safety pass`

## Decision tree

The tree at `content/06-decision-tree.xml` triages: typed input set + named owner + downstream consumer? → ship the checklist; otherwise → skip + escalate. Walk it before authoring so the upgrade plan has an eval gate and a named owner.
