# Trunk-Based CI Gates

## Summary

**One-sentence:** Produces a CI configuration enforcing trunk-based gates: pre-commit hooks under 1s, CI under 10 minutes, branch protection with full required-status list, auto-revert on red trunk, and a verifier that the required-status list stays in sync with CI job names.

**One-paragraph:** CI gates that keep trunk green: pre-commit hooks complete in <1s (lint + format + secret scan only — no pytest); CI is sub-10-minute (cache deps, parallelise tests, move slow integration suites to nightly); branch protection requires PR reviews + all CI status checks + linear history + restricts direct pushes; after any CI change, re-verify the required-status list via gh api so renamed/new jobs gate merges; auto-revert on red trunk via git revert -m 1 instead of human-managed reverts.

**Ефективно для:**

- New repo bootstrap needing the full CI gate set.
- Existing repo whose trunk breaks more than once per week (apply trunk-based-challenges first).
- Hardening branch protection after a hot-fix direct push incident.
- Aligning required-status list after adding/renaming CI jobs.

## Applies If (ALL must hold)

- Hosting on GitHub / GitLab / Bitbucket with branch protection API.
- Team has adopted trunk-based development.
- Tests can run in parallel (or be split into fast/slow tiers).
- Bot account or app available for auto-revert PRs.

## Skip If (ANY kills it)

- Solo project with no CI yet (start with a single check first).
- Mobile/desktop release-branch projects (different gating model).
- Repos without admin access to configure branch protection.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Repo URL + default branch | string | git host |
| CI provider | github-actions | gitlab-ci | circleci | team decision |
| Test suite map (fast / slow / integration tiers) | table | test plan |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[trunk-based-dev-patterns]] | patterns these gates enforce |
| [[practices-python-ecosystem]] | pre-commit hook ecosystem if Python |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 7-step procedure | 900 |
| `content/06-decision-tree.xml` | essential | Routing tree → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `emit-pre-commit` | haiku | render .pre-commit-config.yaml fast hooks |
| `emit-ci-workflow` | sonnet | ci.yml with parallel test split |
| `verify-required-status` | haiku | gh api call comparing required-status to job names |

## Templates

| File | Purpose |
|------|---------|
| `templates/pre-commit-config.yaml` | Fast pre-commit hooks (lint + format + secret-scan) |
| `templates/ci.yml` | GitHub Actions workflow with required-status jobs |
| `templates/verify-protection.sh` | Verify required-status list matches CI job names |
| `templates/artefact.json` | Sample artefact metadata for validator |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-trunk-based-ci-gates.py` | Validate output artefact against the JSON Schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; agent self-check |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[trunk-based-dev-patterns]]
- [[trunk-based-challenges]]
- [[trunk-based-branch-by-abstraction]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, environment context, risk level) to a concrete conclusion, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which rule applies to the current context.
