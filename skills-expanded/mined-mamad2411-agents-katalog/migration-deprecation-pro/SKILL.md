---
name: migration-deprecation-pro
description: Plan and execute migrations, deprecations, compatibility transitions, API/schema changes, dependency upgrades, and old-code removal. Use when replacing modules, changing contracts, upgrading frameworks, deprecating features, or moving users/data safely.
---

# Migration Deprecation Pro

## Workflow

1. Identify old behavior, new behavior, consumers, data, and compatibility window.
2. Choose migration strategy: big bang, expand/contract, adapter, feature flag, dual write, backfill, or staged rollout.
3. Define rollback plan and observability.
4. Update docs, ADRs, changelog, and deprecation notes.
5. Remove old paths only after usage and compatibility are addressed.

## Required Checks

- Who consumes the old contract?
- What data must move or remain readable?
- Can old and new versions run together?
- What happens on rollback?
- What tests prove compatibility?
- What user-facing behavior changes?

## Avoid

- Deleting old paths before consumers migrate.
- Irreversible data changes without warning.
- Silent API contract changes.
- Framework upgrades mixed with unrelated feature work.

## Output

State migration strategy, phases, compatibility risk, rollback, and verification.
