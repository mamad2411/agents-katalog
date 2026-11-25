---
name: cache-sweep-activation-fallback
description: "Sweep stale extension caches before activation, then fall back to a sticky manual-refresh flag if the live refresh fails."
metadata:
  author: ychampion
---

# SKILL: Cache Sweep Activation Fallback
**Domain:** extensions-mcp  
**Trigger:** Apply when newly materialized extension sources must be activated immediately, but the live refresh can fail and needs a recoverable fallback.
**Source Pattern:** Distilled from reviewed extension lifecycle and source-reconciliation patterns.

## Core Method
Treat installation and activation as separate phases. After a background reconcile changes what is on disk, clear the marketplace cache, attempt a full activation refresh, and degrade gracefully if that refresh throws. The fallback path should clear plugin caches again, log the failure, and set a sticky manual-refresh bit so the system admits that runtime state is stale instead of pretending activation succeeded.

## Key Rules
- Only attempt automatic activation after a materialized change that needs live components to catch up; steady-state or metadata-only work should not enter this path.
- Clear upstream caches before activation so the refresh reads fresh marketplace and plugin state rather than replaying stale memoized data.
- Wrap the activation step in a catch boundary that logs the error and preserves the newly materialized state on disk.
- If activation fails, clear the plugin cache with a specific reason string and raise an idempotent manual-refresh flag instead of retrying blindly.
- Keep the fallback sticky until a deliberate refresh consumes it; repeated failures should not thrash the state tree with duplicate writes.

## Example Application
If a background extension installer clones a new command marketplace during startup, clear the source cache, try a full runtime reload, and if the reload fails mark the UI with a single “reload extensions” prompt while preserving the newly cloned files for recovery.

## Anti-Patterns (What NOT to do)
- Do not swallow activation failures after install; users will assume the new extension is live while the runtime still points at stale caches.
- Do not skip cache clearing before the activation attempt or the refresh may rehydrate old data and fail in harder-to-debug ways.
- Do not loop automatic retries without a user-visible fallback; repeated refresh crashes should turn into a manual recovery prompt.
