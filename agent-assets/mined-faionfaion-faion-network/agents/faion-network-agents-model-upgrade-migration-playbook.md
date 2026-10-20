# Model Upgrade Migration Playbook

## Summary

**One-sentence:** Coordinates a model-family upgrade (e.g. Sonnet 4.6 → 4.7, GPT-4 → 4.5) across all prompts + tests + cost budgets + rollback, gated by golden-set delta + shadow-traffic divergence + per-prompt regression triage.

**One-paragraph:** Coordinates a model-family upgrade (e.g. Sonnet 4.6 → 4.7, GPT-4 → 4.5) across all prompts + tests + cost budgets + rollback, gated by golden-set delta + shadow-traffic divergence + per-prompt regression triage. The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Vendor announces new model — migration window 30-90 days до deprecation.
- Per-prompt regression: різні prompts реагують неоднаково на upgrade.
- Cost delta: новий model може дорожчий per-token AND економніший per-task.
- Rollback план: production-grade миграція без kill-switch — заборонена.

## Applies If (ALL must hold)

- Vendor announced model deprecation or upgrade window.
- Production AI features depend on the affected model family.
- Per-prompt eval infra exists (golden set + scoring).
- Rollback infra exists (model selector flag / version pin).

## Skip If (ANY kills it)

- Migration is config-only (region change) — no production behavior delta.
- Single-prompt isolated tool with no fleet — direct change + smoke test suffices.
- Pre-prod environment only — no rollback urgency.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Vendor announcement URL + deprecation date | URL + ISO date | Vendor docs |
| Current model id + prompt fleet inventory | YAML | Repo audit |
| Golden set per prompt | Directory of JSONL files | ml-engineering |
| Live pricing snapshot | JSON | Vendor pricing API |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/ai/AGENTS.md` | Parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-model-upgrade-migration-playbook` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/playbook-step.md.j2` | Markdown playbook skeleton — named steps with owner + input + exit criterion + output location |
| `templates/playbook-step.md` | Markdown playbook skeleton — named steps with owner + input + exit criterion + output location Generated from `templates/playbook-step.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/step-checklist.md.j2` | Per-step go/no-go checklist for operator runtime |
| `templates/step-checklist.md` | Per-step go/no-go checklist for operator runtime Generated from `templates/step-checklist.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-model-upgrade-migration-playbook.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- Parent: `pro/ai/AGENTS.md`
- [[shadow-traffic-rollout-pattern]]
- [[prompt-versioning-and-ab-framework]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
