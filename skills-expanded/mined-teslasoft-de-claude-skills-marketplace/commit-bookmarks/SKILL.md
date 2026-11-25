---
name: commit-bookmarks
description: |
  Sync Commit Drone changelist previews into IntelliJ IDEA .idea/bookmarks.json.
  Preserves manual bookmark groups and replaces only Drone-managed [Commit] groups.
triggers:
  - /idea commit-bookmarks
  - sync commit bookmarks
  - commit drone bookmarks
  - apply changelists to bookmarks.json
negative_triggers:
  - /idea changelist
  - /idea backup
  - /idea sync-modules
version: 1.0.0
author: Teslasoft / Claude
last_updated: 2026-05-04
---

# Skill: IDEA Commit Bookmarks

Synchronize Commit Drone changelists to IntelliJ IDEA bookmark groups.

## When to Use

- Commit Drone has a changelist preview ready for review.
- `.idea/bookmarks.json` should expose commit groups in IDEA without changing manual bookmark groups.
- `/idea commit-bookmarks` is requested for a vault or project that runs the Telemetry Drone.

## Workflow

1. Confirm the Drone is running and the commit organizer is enabled.
2. Trigger `pnpm commit:bookmarks`, which calls `POST /commits/apply-to-bookmarks`.
3. Expect a response shaped as `{ success, applied, preserved, removed, groups, message }`.
4. Reopen or refresh IDEA bookmark/changelist views if the IDE does not immediately show the updated groups.

## Merge Semantics

- Managed groups always start with `[Commit] `.
- Manual groups are any groups that do not start with `[Commit] ` and must be preserved.
- Each run removes stale managed groups and writes the current preview's managed groups.
- Empty previews remove managed groups while keeping manual groups.
- Bookmark entries use project-relative file paths from the Commit Drone preview.

## Verification

Run the focused Drone adapter tests before broader E2E coverage:

```bash
pnpm --filter telemetry-drone test
```

For branch-clone Docker validation, commit the branch first so fixture clones can resolve the ref, then run the fixture suite from the vault root.
