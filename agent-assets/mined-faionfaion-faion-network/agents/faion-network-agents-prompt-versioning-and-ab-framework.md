# Prompt Versioning and A/B Framework

## Summary

**One-sentence:** Version-controls prompts (semver + changelog + ownership + lockfile) and ships A/B-test rig (deterministic traffic split + per-variant metrics + power analysis + statistical significance) for safe prompt iteration.

**One-paragraph:** Version-controls prompts (semver + changelog + ownership + lockfile) and ships A/B-test rig (deterministic traffic split + per-variant metrics + power analysis + statistical significance) for safe prompt iteration. The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Prompt fleet >5 на team: без versioning silent regressions неминучі.
- A/B experiments на prompts (variant_a vs variant_b) з power-analysis перед launch.
- Per-variant cost + latency + quality metrics — порівняння на одному dashboard.
- Changelog discipline: кожна зміна prompt = entry + reviewer + rollback path.

## Applies If (ALL must hold)

- Prompt fleet size ≥5 in active production use.
- Per-user identifier exists for deterministic traffic split.
- Eval infra exists that can attach metrics to prompt versions.
- PR review process is enforced on prompt changes.

## Skip If (ANY kills it)

- Prompt fleet ≤2 — versioning overhead is not justified.
- No A/B infra and cannot be built within the migration window.
- Anonymous traffic only — no per-user identifier for deterministic split.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Prompt repo with semver branch structure | Git directory | Eng team |
| A/B infra config | YAML (LaunchDarkly / GrowthBook / internal) | Infra team |
| Eval pipeline that attaches metrics to prompt version | Python module | ML eng |
| Per-user identifier for deterministic split | string from request context | App API |

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
| `draft-prompt-versioning-and-ab-framework` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config-instance.json` | JSON instance of a filled config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-prompt-versioning-and-ab-framework.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- Parent: `pro/ai/AGENTS.md`
- [[model-upgrade-migration-playbook]]
- [[prompt-injection-test-suite]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
