---
name: "rankup-work-logging"
description: "Work tracking + evidence logging for Rankup. Use when updating docs/work (CURRENT, ROADMAP, epics, log) and recording yarn validate evidence to close WPs/epics reproducibly."
owner: "rankup"
scope: "work-tracking"
---

# Rankup: Work tracking + evidence logging

## Objective

Keep `docs/work/**` reproducible:

-   WPs have clear DoR/DoD
-   Validation evidence is recorded
-   CURRENT/ROADMAP reflect reality

## Trigger / Use when

-   You finish a WP or an epic.
-   You ran `yarn validate` and need to record results.
-   You need to move CURRENT to the next unit of work.

## Minimal workflow

1. Update WP/epic status

-   Mark WP sections as Done/Blocked with a short note.
-   Update epic status if closing.

2. Record evidence in the daily log

-   Append to `docs/work/log/YYYY-MM-DD.md`:
    -   command(s) executed
    -   PASS/FAIL
    -   short note about scope

3. Update `docs/work/CURRENT.md`

-   Point to next WP/epic.
-   Keep it small and unambiguous.

## Evidence format (recommended)

```md
## YYYY-MM-DD

-   WP-XXX-YY: <short label>
    -   yarn validate: PASS
    -   notes: <1-2 lines>
```

## Done criteria

-   Work docs reflect actual repo state.
-   Evidence exists for validation gates.
