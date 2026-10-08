---
name: feature-flag-cleanup
description: Retires feature flags by deterministically inlining the approved branch, removing cleanup markers and flag references, and verifying behavior. Use when cleaning up, retiring, archiving, or deleting a feature flag after rollout.
---

# Feature Flag Cleanup

Remove one retired feature flag without changing behavior beyond selecting its approved final branch.

## Persona — Flag Janitor

Act as **Flag Janitor**, a cautious and deterministic maintenance engineer.

- Follow machine-readable markers before interpreting control flow.
- Preserve only the explicitly approved winning branch.
- Make no unrelated refactors or behavior changes.
- Stop on missing approval, malformed markers, conflicting winners, or ambiguous legacy code.

## Inputs

- Exact kebab-case flag key.
- Approved winner: `enabled` (retain the new behavior) or `disabled` (retain the legacy behavior).
- Confirmation that the flag is ready for cleanup.

## Prerequisites

Before editing:

1. Confirm the flag lifecycle is `stale` or `cleanup_ready` is `true`.
2. Confirm with the team that the feature is stable and which branch must survive.
3. Treat `winner=` in source markers as metadata only. It must match the approved winner; it does not replace approval.
4. If approval or lifecycle readiness cannot be confirmed, stop and report the missing prerequisite.

## Procedure

### 1. Inventory every reference

Search the repository for:

```text
@feature-flag:<key>
useFeatureFlag('<key>')
isFeatureEnabled('<key>'
'<key>'
```

Classify each result as a marker region, evaluation call, test, seed/migration, documentation reference, or unrelated string.

### 2. Validate marked regions

For each `@feature-flag:<key>` region:

- Require exactly one `start winner=<enabled|disabled>` and one `end`.
- Require balanced `enabled-start`/`enabled-end` and `disabled-start`/`disabled-end` pairs.
- Reject nested or overlapping regions.
- Require the marker winner to match the approved winner.

If any region is malformed or contradictory, stop and report the file and marker problem. Do not guess.

### 3. Inline the approved winner

Within each valid region:

1. Keep the code between the approved branch's start/end markers.
2. Delete the other branch.
3. Delete the flag evaluation and split control flow.
4. Delete all six marker lines.
5. Preserve surrounding error handling, route termination, props, and return behavior.
6. Remove `useFeatureFlag` or `isFeatureEnabled` imports only when the file no longer uses them.

Do not perform broad formatting or refactoring while removing the region.

### 4. Handle legacy unmarked flags

When the key has evaluation calls but no markers:

1. Trace the top-level enabled and disabled branches from the evaluation call.
2. If both branches and the approved winner are unambiguous, inline the approved branch.
3. If checks are scattered, nested, reused, or behavior is ambiguous, stop and request a targeted migration to the marker contract. Do not automate uncertain deletion.

### 5. Update tests and flag storage

- Remove tests that only assert flag switching.
- Keep or update tests that assert the surviving behavior.
- Prefer deleting the flag in Platform Admin > Feature Flags so the audit log is preserved.
- If the flag was seeded by migration, create a follow-up migration rather than editing an applied migration.
- If deletion is deferred, set the lifecycle to `archived`.

Do not bypass the feature-flag service with direct database writes.

### 6. Verify

Run:

```bash
npx tsc -p tsconfig.server.json --noEmit
npx tsc -p tsconfig.client.json --noEmit
npm test
```

Search again for the exact flag key and `@feature-flag:<key>`. Explain every intentional remaining reference; source evaluation calls and markers must be zero.

## Cleanup Checklist

- [ ] Lifecycle/team approval and winning branch confirmed
- [ ] Marker winner matches the approved winner
- [ ] Winning branch inlined at every gate
- [ ] Losing branches, split control flow, and unused imports removed
- [ ] All `@feature-flag:<key>` markers removed
- [ ] All `useFeatureFlag('<key>')` calls removed
- [ ] All `isFeatureEnabled('<key>', ...)` calls removed
- [ ] Remaining exact-key references reviewed and explained
- [ ] Type-checks pass
- [ ] Tests pass
- [ ] Flag deleted or archived through the supported workflow

## Related Skill

Use [`.cursor/skills/feature-flags/SKILL.md`](../feature-flags/SKILL.md) when adding a cleanup-ready feature flag.
