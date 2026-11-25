---
name: materialization-aware-refresh-escalation
description: "React to marketplace materialization diffs by refreshing plugins when new installs land and escalating to needsRefresh when updates or refresh failures occur."
metadata:
  author: ychampion
---

# SKILL: Materialization-Aware Refresh Escalation
**Domain:** extensions-mcp  
**Trigger:** When background plugin installation reconcilers detect that declared marketplaces differ from what is materialized, use the diff to decide whether to auto-refresh plugins or escalate to a manual refresh prompt.
**Source Pattern:** Distilled from reviewed extension lifecycle and source-reconciliation patterns.

## Core Method
1. Before reconciling, read the declared marketplaces (`getDeclaredMarketplaces()`), the previously materialized config (`loadKnownMarketplacesConfig()`), and compute `diffMarketplaces()` so you know which names are missing or changed.
2. Build `pendingNames` from `diff.missing` plus `diff.sourceChanged` so the UI reports exactly which marketplaces are still being processed; return early when that array is empty so no work runs unless there is material change.
3. Call `reconcileMarketplaces({ onProgress })`, map the `installing`/`installed`/`failed` events to AppState, track metrics for installed/updated/failed/up-to-date counts, and log them via `logEvent` and diagnostics helpers.
4. After reconciliation, inspect the result:
   - When `result.installed.length > 0`, clear the marketplace cache, log the auto-refresh path, and await `refreshActivePlugins(setAppState)` inside a try/catch so MCP caches are rebuilt. On refresh failure, log the error, clear the plugin cache, and set `plugins.needsRefresh` via AppState only if it was previously false.
   - When there are no fresh installs but `result.updated.length > 0`, clear both marketplace and plugin caches and set the `needsRefresh` flag so the UI invites `/reload-plugins` while avoiding an automatic refresh.
   - When there are neither installs nor updates, skip cache invalidation and refresh so the reconciliation stays lightweight.

## Key Rules
- Only auto-refresh when brand-new marketplaces were installed; updates-only reconciliations should not trigger the refresh path.
- Clear both marketplace and plugin caches before touching `refreshActivePlugins` or setting `needsRefresh` so stale artifacts cannot leak into the new plugin state.
- Always wrap `refreshActivePlugins` in a try/catch, log failures (`logError`, `logForDebugging`), and fall back to `needsRefresh` rather than silently suppressing the error.
- Guard the `needsRefresh` setter so it only flips once per failure path and never reassigns while the flag is already true.

## Example Application
Installing a curated marketplace during background startup on a fresh homespace uses this path so the new tools become available without forcing the user to manually run `/reload-plugins`.

## Anti-Patterns (What NOT to do)
- Do not refresh plugin state when `result.installed.length === 0`; the caches were already populated and redundant refreshes slow startup.
- Do not swallow refresh failures; the fallback `needsRefresh` flag exists so the UI can surface `/reload-plugins` once the auto-path fails.
- Do not clear caches only after calling `refreshActivePlugins`; stale cache entries must be removed before the refresh attempt or the refresh may still resolve to old code.
