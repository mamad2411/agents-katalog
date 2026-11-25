---
name: diff-first-progress-projection
description: "Project marketplace installation progress by diffing declared sources before kickoff so the UI shows pending spinners without waiting on the clone."
metadata:
  author: ychampion
---

# SKILL: Diff-First Progress Projection
**Domain:** extensions-mcp  
**Trigger:** Background marketplace reconciliation needs to show progress before the clone/install work begins (before `reconcileMarketplaces`).
**Source Pattern:** Distilled from reviewed extension lifecycle and source-reconciliation patterns.

## Core Method
Run the marketplace diff (`diffMarketplaces`) before any long-running work so you can enumerate `missing` and `sourceChanged` entries. Collapse those names into `pendingNames` and immediately `setAppState` with `plugins.installationStatus.marketplaces = pendingNames.map(name => ({ name, status: 'pending' }))` before calling `reconcileMarketplaces`. That makes the UI show the right number of pending spinners even while git clones are still starting.

## Key Rules
- Compute `declared` and `materialized` marketplaces and pass them through `diffMarketplaces` once, capturing `missing` plus `sourceChanged.map(c => c.name)` for the pending set.
- Initialize `installationStatus.marketplaces` with the pending list; leave `installationStatus.plugins` empty unless a plugin-level hook has more granular progress.
- Write the pending state before `reconcileMarketplaces` so that any UI watching `plugins.installationStatus.marketplaces` can render spinners before the expensive work begins.
- Keep the `status` field locked to `'pending'` until the `onProgress` bridge reports a transition; do not assume any installs succeeded until they emit events.

## Example Application
`performBackgroundPluginInstallations` computes `pendingNames` and immediately updates AppState with a queue of `'pending'` marketplaces. Even before any git clones happen, a marketplace status line renders with a spinner, which later echos the `installing`/`installed` lifecycle when the `onProgress` bridge fires.

## Anti-Patterns (What NOT to do)
- Do not call `reconcileMarketplaces` before the diff – you lose the chance to know how many spinners the UI must draw and the install list might appear empty during the initial load.
- Do not skip seeding `installationStatus.marketplaces` in `setAppState`, or the UI will never show any pending state and users will assume nothing is happening.
- Do not mix plugin-level progress into `installationStatus.plugins` until you actually collect plugin-specific events; that list is for instrumentation that doesn't exist in this path.
