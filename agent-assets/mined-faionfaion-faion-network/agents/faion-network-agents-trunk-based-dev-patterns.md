# Trunk-Based Development Patterns

## Summary

**One-sentence:** Produces a trunk-based pattern plan using feature flags, branch by abstraction, and dark launching — with cleanup tickets, positive flag naming, < 24h branch lifetimes, and < 1% dark-launch ramp before scaling.

**One-paragraph:** Trunk-based patterns at scale: feature flags hide incomplete work; branch by abstraction enables large refactors without long-lived branches; dark launching tests new implementations against production traffic before exposure. The methodology produces a pattern plan with: branch lifetime cap < 24h, one-flag-one-task with cleanup ticket at birth, positive flag naming (<area>.<verb>_<thing>), CI < 10 min, auto-revert on red trunk, dark-launch ramp < 1% for a full diurnal cycle, and explicit cleanup-collapse step for any BbA migration.

**Ефективно для:**

- Multi-step feature shipped on trunk with flag-gated rollout.
- Large refactor staged via Branch by Abstraction.
- Dark-launching a new implementation alongside the legacy one.
- Auditing existing flag inventory for cleanup obligations.

## Applies If (ALL must hold)

- Team has a feature-flag provider (homegrown OK if reliable).
- Trunk-based gating (see trunk-based-ci-gates) is already in place.
- Project supports parallel implementations behind an interface (BbA candidate).
- Production observability exists (so dark-launch metrics can be compared).

## Skip If (ANY kills it)

- Mobile/desktop release-cut projects without flag infrastructure.
- Solo project where 'shipping a small feature on trunk' has no audience to dark-launch against.
- Codebases where the CI gate is not yet trustworthy (apply trunk-based-ci-gates first).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Feature spec | design doc + acceptance criteria | PM / lead |
| Flag-naming convention | <area>.<verb>_<thing> | team standard |
| Dark-launch observability | metric to compare new vs legacy | ops |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[trunk-based-ci-gates]] | CI + branch protection + auto-revert in place |
| [[trunk-based-branch-by-abstraction]] | BbA mechanics for staged refactors |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules with rationale + source | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 6-step procedure | 900 |
| `content/06-decision-tree.xml` | essential | Routing tree → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `design-flag-and-cleanup` | sonnet | name flag + open cleanup ticket |
| `plan-rollout-ramp` | sonnet | compose dark-launch ramp schedule |
| `track-active-flags` | haiku | register flag in .aidocs/feature-flags.md |

## Templates

| File | Purpose |
|------|---------|
| `templates/flag-naming.md.j2` | Positive flag naming reference |
| `templates/flag-naming.md` | Positive flag naming reference Generated from `templates/flag-naming.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/dark-launch-ramp.yaml` | Dark-launch ramp schedule template |
| `templates/feature-flags-inventory.md.j2` | Inventory entry template under .aidocs/feature-flags.md |
| `templates/feature-flags-inventory.md` | Inventory entry template under .aidocs/feature-flags.md Generated from `templates/feature-flags-inventory.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/artefact.json` | Sample artefact metadata for validator |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-trunk-based-dev-patterns.py` | Validate output artefact against the JSON Schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; agent self-check |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[trunk-based-ci-gates]]
- [[trunk-based-branch-by-abstraction]]
- [[trunk-based-challenges]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, environment context, risk level) to a concrete conclusion, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which rule applies to the current context.
