---
name: list-workflows
description: List active, paused, and completed flows-lite workflow runs from the local plugin data directory.
---

# list-workflows

> Show every flows-lite workflow run on this machine, grouped by status.

## When to use

- The user asks "what workflows are running?" or "show me paused workflows".
- After a session restart when the SessionStart hook hinted at paused runs.

## Procedure

1. Call the executable:

   ```bash
   ${POLYMATH_PLUGIN_ROOT}/bin/polymath-flow list
   ```

   To filter:

   ```bash
   ${POLYMATH_PLUGIN_ROOT}/bin/polymath-flow list --status paused
   ${POLYMATH_PLUGIN_ROOT}/bin/polymath-flow list --status active
   ${POLYMATH_PLUGIN_ROOT}/bin/polymath-flow list --status completed
   ```

2. Render the table grouped by status. Active first, paused next, completed last (most recent 5 only).

## Output

```text
Active:
  - 2026-05-23T14-22-shipFeature-rate-limit-login    shipFeature

Paused:
  - 2026-05-21T09-10-shipFeature-resilient-retries   shipFeature  — mustPass: pr-draft-exists

Completed (recent):
  - 2026-05-20T11-04-shipFeature-feature-flags       shipFeature
```

## Anti-patterns to avoid

- Showing all completed runs by default — clutter.
- Inferring run state from filesystem heuristics instead of asking the executable.
