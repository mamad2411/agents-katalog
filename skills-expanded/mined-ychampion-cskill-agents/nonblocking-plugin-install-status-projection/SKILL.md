---
name: nonblocking-plugin-install-status-projection
description: "Map async marketplace reconciliation events into AppState rows so UIs show install/installing/failed badges without blocking."
metadata:
  author: ychampion
---

# SKILL: Nonblocking Plugin Install Status Projection
**Domain:** extensions-mcp  
**Trigger:** Use when marketplace reconciliation emits progress events but the main UI must remain responsive with up-to-date status rows.
**Source Pattern:** Distilled from reviewed extension lifecycle and source-reconciliation patterns.

## Core Method
Before the async reconciliation runs, seed AppState with `pending` rows for every diffed marketplace. Pass a shared updater into the reconciler’s `onProgress` hook that maps each event type (`installing`, `installed`, `failed`) to the corresponding AppState entry by marketplace name, keeping the rest of the state untouched. When an event includes an error, annotate that marketplace row so the UI can reveal diagnostics while still letting other installers continue running.

## Key Rules
- Always update AppState immutably via `setAppState(prev => ({ ...prev, plugins: { ...prev.plugins, installationStatus: { ... }}}))` to avoid clobbering unrelated UI state.
- Use a central helper like `updateMarketplaceStatus` so each event only updates the matching `marketplaces` entry (by name) and nothing else.
- Include event-specific metadata (`status`, optional `error`) in the row so the UI can show spinners, success checks, or failure hints.
- Keep this projection logic outside the main reconciling flow so the long-running `reconcileMarketplaces` call never awaits UI updates; it merely fires events.

## Example Application
If your agent tracks multiple plugin sources, apply this skill to emit nonblocking status rows for each install progress report so the user can monitor clones without stalling the command loop.

## Anti-Patterns (What NOT to do)
- Do not mutate the AppState array in place or replace `installationStatus` wholesale; that would drop other concurrent progress rows.
- Do not ignore the `error` payload on failures, or the UI will never explain why a marketplace install failed.
- Avoid waiting for the entire reconciliation to finish before updating statuses; the whole point is incremental feedback.
