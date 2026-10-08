# GitHub Actions — Matrix Builds

## Summary

**One-sentence:** Generates a matrix-strategy config (axes + include/exclude + fail-fast policy + per-combination artifacts + concurrency) for parallel multi-OS / multi-version testing.

**One-paragraph:** Generates a matrix-strategy config (axes + include/exclude + fail-fast policy + per-combination artifacts + concurrency) for parallel multi-OS / multi-version testing. The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Libraries що мають підтримувати кілька версій runtime (python 3.10/3.11/3.12).
- Multi-OS support (ubuntu, macos, windows) — cross-platform testing.
- Combinatorial test coverage (db × cache × language version).
- Per-combination artifacts (different binaries per OS/arch).

## Applies If (ALL must hold)

- Code must be verified on ≥2 versions/platforms.
- Tests are runnable in parallel without shared mutable state.
- Runner minutes budget allows N×M jobs per build (cost-aware).
- Per-combination outputs (binaries, reports) are useful downstream.

## Skip If (ANY kills it)

- Single platform / single language version — matrix overhead is gratuitous.
- Tests share state and cannot run concurrently — matrix flakes immediately.
- Runner budget constrained and N×M > 5× the value of the coverage.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Supported versions list | YAML (language, versions) | Eng team |
| Supported OS list | YAML | Eng team |
| Per-combo include/exclude rules | YAML | Eng team |
| Runner budget baseline | minutes per build | GitHub admin |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/infra/cicd-engineer/AGENTS.md` | Parent skill context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-gha-matrix-builds` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config-instance.json` | JSON instance of a filled config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-gha-matrix-builds.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- Parent: `pro/infra/cicd-engineer/AGENTS.md`
- [[finops-framework]]
- [[gitops-core-principles]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
