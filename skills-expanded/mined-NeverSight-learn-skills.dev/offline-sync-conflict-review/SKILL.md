---
name: offline-sync-conflict-review
description: Design and audit offline sync, queued mutations, reconnect behavior, conflict resolution, local-first UX, draft persistence, tombstones, attachment sync, optimistic updates, multi-device edits, merge policies, data-loss recovery, and sync observability. Use when mobile, desktop, PWA, field, creator, or collaboration products must keep working without reliable connectivity.
---

# Offline Sync Conflict Review

Use this skill to convert a offline queues, sync state, conflict resolution, local data safety, and multi-device recovery question into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify user job, entity types, mutation types, offline duration, device count, authority model, and harm from wrong merge.
2. Read `references/offline-sync-conflict-patterns.md`.
3. Classify data as append-only, editable profile, collaborative document, financial/legal, media attachment, or system setting.
4. Define local storage, mutation log, idempotency, ordering, tombstones, merge policy, conflict UI, retry, and recovery telemetry.
5. Produce sync state machine, conflict decision table, event schema, UX copy, and QA scenario checklist.

## Guardrails

- Do not use last-write-wins for money, permissions, legal records, inventory, or destructive actions without explicit product acceptance.
- Do not silently overwrite another device or collaborator when a user decision is required.
- Do not queue unbounded offline writes without storage limits, backpressure, and failure UI.
- Do not claim “offline ready” unless cold start, logout, app reinstall, expired auth, and attachment failures are considered.

## Output format

```text
Offline context:
Entity / mutation / harm if wrong:

Sync and conflict plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Merge policy:
- <item> -> <policy, metric, edge case, support note>

Recovery and QA:
- <trigger> -> <action, communication, owner>
```
