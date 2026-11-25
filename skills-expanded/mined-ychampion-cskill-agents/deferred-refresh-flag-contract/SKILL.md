---
name: deferred-refresh-flag-contract
description: "Decide when to auto-refresh plugins after marketplaces change and when to defer to a manual `/reload-plugins` via the `needsRefresh` flag."
metadata:
  author: ychampion
---

# SKILL: Deferred Refresh Flag Contract
**Domain:** extensions-mcp  
**Trigger:** `performBackgroundPluginInstallations` completes `reconcileMarketplaces` and must decide whether to auto-refresh plugins or set `plugins.needsRefresh` via AppState.
**Source Pattern:** Distilled from reviewed extension lifecycle and source-reconciliation patterns.

## Core Method
When new marketplaces are installed (`result.installed.length > 0`), treat the change as urgent: clear both marketplace and plugin caches, then call `refreshActivePlugins(setAppState)` so MCP connections re-establish with the freshly cloned sources. If that auto-refresh fails, log the error, clear the plugin cache with a reason string, and set `plugins.needsRefresh = true` so the UI prompts `/reload-plugins`. When only updates are available (`result.updated.length > 0`), do not auto-refresh; instead clear caches and set `needsRefresh` so the user opts into the reload. `needsRefresh` updates must be idempotent: the setter checks `prev.plugins.needsRefresh` and returns early if already true.

## Key Rules
- Always run `clearMarketplacesCache()` before refreshing or flagging; it ensures the cached metadata is rebuilt before the next plugin load.
- For installs, wrap `refreshActivePlugins(setAppState)` in a try/catch. On failure, call `clearPluginCache('performBackgroundPluginInstallations: auto-refresh failed')` and fall back to the `needsRefresh` guard that sets the flag to true only once.
- For updates-only, clear the plugin cache with `clearPluginCache('performBackgroundPluginInstallations: marketplaces reconciled')` so stale plugin bundles are not re-used, but leave control in the user’s hands by setting `needsRefresh` instead of forcing a reload.
- The `needsRefresh` setter uses `setAppState(prev => { if (prev.plugins.needsRefresh) return prev; return { ...prev, plugins: { ...prev.plugins, needsRefresh: true } }; })` so the UI can show a single prompt and avoid redundant re-renders.

## Example Application
After `reconcileMarketplaces` returns `result.installed = [ ... ]`, the manager clears caches and calls `refreshActivePlugins`. If the refresh completes, caches stay clear and MCP reconnects automatically. If the refresh throws, the catch logs the failure, clears the plugin cache with a descriptive reason, and the guard flips `plugins.needsRefresh` so `/reload-plugins` shows up instead. When only `result.updated` is populated, the same cache-clearing and guard runs, but without trying to refresh automatically.

## Anti-Patterns (What NOT to do)
- Do not auto-refresh when only marketplace updates exist; forcing a reload can interrupt long-running contexts when an update can safely wait for an explicit `/reload-plugins`.
- Do not leave cache-clearing out of either branch—stale marketplace metadata or plugin bundles will confuse the auto-refresh or manual reload paths.
- Do not set `needsRefresh` by overwriting the object blindly; always check the previous flag so a failed refresh path does not recreate the AppState slice on every error log.
