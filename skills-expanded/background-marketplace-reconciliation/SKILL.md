---
name: background-marketplace-reconciliation
description: "Run marketplace diff and reconciliation in the background while surfacing per-source progress to the UI without blocking startup."
metadata:
  author: ychampion
---

# SKILL: Background Marketplace Reconciliation
**Domain:** tool-orchestration
**Trigger:** Use when you need to reconcile declared plugin marketplaces or source registries without blocking startup or the main command loop.
**Source Pattern:** Distilled from reviewed plugin-source reconciliation and background install lifecycle implementations.

## Core Method
Diff the declared marketplace or plugin-source configuration against the current cached state before doing any network work. Seed UI state with a `pending` entry for every source that needs installation or update, then run the actual reconciliation in the background. As progress events arrive, map them onto visible install states so the product can show spinners, success, and failure per source without freezing the main UI. When reconciliation finishes, clear stale caches and branch on the outcome so new installs, updates, and failures each trigger the right downstream behavior.

## Key Rules
- Populate visible state with `pending` rows before the async work begins so the UI can render progress immediately.
- Use progress callbacks to update each source row (`installing`, `installed`, `failed`) and attach any error text for diagnostics.
- Keep analytics/logging around the whole operation so you know how many installed/updated/failed entries returned.
- After the promise resolves, clear caches and trigger refresh or flag-for-refresh decisions rather than leaving stale extension state behind.

## Example Application
For a new agent UI that adds curated plugin sources, apply this pattern whenever sources need to be cloned or updated in the background so the UI gets per-source spinners and the rest of the agent remains responsive.

## Anti-Patterns (What NOT to do)
- Do not block the main thread until marketplace reconciliation finishes; it should happen behind the scenes with status rows.
- Do not start reconciling without seeding the UI state—users must see which marketplaces are pending.
- Avoid treating updates and fresh installs the same way; they often require different downstream actions (live refresh vs. manual refresh notification).


