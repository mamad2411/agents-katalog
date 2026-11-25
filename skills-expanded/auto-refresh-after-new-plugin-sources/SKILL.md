---
name: auto-refresh-after-new-plugin-sources
description: "Trigger a plugin refresh cycle whenever reconciliation installs new marketplaces so plugin state stays in sync."
metadata:
  author: ychampion
---

# SKILL: Auto Refresh After New Plugin Sources
**Domain:** tool-orchestration
**Trigger:** Apply when background reconciliation installs at least one new marketplace and the agent must refresh plugin cache without explicit user action.
**Source Pattern:** Distilled from reviewed post-install refresh and extension-cache invalidation implementations.

## Core Method
After reconciliation reports at least one newly installed plugin source, clear both the source cache and the active plugin cache, then trigger a refresh of the live extension registry. Treat that refresh as best-effort but important: if it succeeds, the new tools become available immediately; if it fails, log the error and raise a manual-refresh flag so the user sees that recovery is required. Do this before treating downstream extension operations as ready, otherwise the product will keep resolving against stale code.

## Key Rules
- Only trigger the refresh when new installs occurred; avoid redundant refresh cycles after mere updates.
- Clear both marketplace and plugin caches before refreshing to ensure stale data cannot leak into the newly loaded plugins.
- Catch refresh failures, log the error, and set a visible manual-refresh flag rather than silently failing.
- Keep analytics/logging tied to the install path so you know when an automatic refresh runs and whether it failed or succeeded.

## Example Application
If a new marketplace is added via a curated list, automatic refresh ensures CLI commands that rely on that marketplace can resolve tools without forcing users to manually run a separate reload step.

## Anti-Patterns (What NOT to do)
- Do not refresh plugin state when there are zero new installs; the extra cache clears slow startup without benefit.
- Do not swallow refresh errors; otherwise users never learn the auto recovery failed and manual action stays hidden.
- Do not reuse stale caches while refreshing; skip clearing caches then refresh and the agent continues pointing at old code.


