# Model Eval Control Bands

## Summary

**One-sentence:** Produces a versioned Model Eval Control Bands artefact — typed inputs + named owner + decisions traceable to source artefacts + last_reviewed gate.

**One-paragraph:** Eval methodologies define metrics but rarely how to set + maintain control bands so drift is detectable without false alarms. This methodology turns "Daily eval-suite run + drift triage" into a typed artefact: per-metric upper/lower bounds, an alerting policy, a named accountable owner, a rationale citing the input distributions and historical variance that justified the bounds, and a `last_reviewed` field that flags stale records on read. Every decision in the output cites the input artefact that justified it; batching multiple unrelated decisions through one pass is rejected.

**Ефективно для:** ML-engineer, що тримає daily eval-suite + drift triage і потребує зрозумілих, ревьюваних control bands замість туманних "anything off" alerts.

## Applies If (ALL must hold)

- Task is an instance of `role-ml-engineer/Daily eval-suite run + drift triage` or a near variant.
- All artefacts named in Prerequisites are available before starting.
- Output will be consumed by a downstream agent or human reviewer.
- Tier == geek.

## Skip If (ANY kills it)

- Team already maintains a working artefact for this gap — replace, do not duplicate.
- Greenfield prototype with no production users.
- Regulatory / compliance overrides in-methodology guidance.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Eval-suite metric definitions | YAML | eval repo |
| Historical metric series (≥30 days) | CSV / Parquet | observability |
| Owner registry | dir or doc | team handbook |
| Last-rotation policy | doc | governance |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `geek/ai/ml-engineer/model-evaluation` | Defines the metrics this bands. |
| `geek/ai/ml-engineer/llm-observability-stack` | Source of the historical series. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 rules: bound scope, typed input, named owner, versioned + last_reviewed, traceable decision. | ~900 |
| `content/02-output-contract.xml` | essential | Schema for the control-bands artefact. | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: invented inputs, "team" owner, post-hoc rationale, stale record, unbounded drift definition. | ~900 |
| `content/06-decision-tree.xml` | essential | Routes by input completeness + ownership presence. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `draft_inputs_summary` | haiku | Template fill on bounded inputs. |
| `synthesize_decision` | sonnet | Per-instance judgement on band placement. |
| `review_for_compliance` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|---|---|
| `templates/model-eval-control-bands.json` | JSON schema for the output contract. |
| `templates/model-eval-control-bands.md.j2` | Markdown skeleton with required fields. |
| `templates/model-eval-control-bands.md` | Markdown skeleton with required fields. Generated from `templates/model-eval-control-bands.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-model-eval-control-bands.py` | Enforce output contract: artefact_id, owner non-plural, rationale references inputs, version + last_reviewed present. | After subagent return, before consumer reads. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/ai/ml-engineer/`
- upstream playbook: `role-ml-engineer/Daily eval-suite run + drift triage`

## Decision tree

The tree at `content/06-decision-tree.xml` triages: are inputs typed + owner named + downstream consumer present? → produce control-bands record; otherwise → skip + escalate gap. Walk it before authoring so you don't ship an unowned drift policy.
