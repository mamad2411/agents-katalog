---
name: dead-path-update-skipping
description: "Skip update actions that point at missing local paths when a valid materialized entry already exists, preserving the working state instead of converting drift into a noisy failure."
metadata:
  author: ychampion
---

# SKILL: Dead Path Update Skipping
**Domain:** extensions-mcp  
**Trigger:** Use when update candidates come from local paths that may disappear across checkouts, but existing materialized state should remain usable until a valid replacement exists.
**Source Pattern:** Distilled from reviewed extension lifecycle and source-reconciliation patterns.

## Core Method
Before running an update from a local path, verify that the declared path still exists. If the action is an update and the current materialized entry is still valid, skip the update rather than turning a transient path mismatch into a failed reinstall. This preserves the working materialized state in multi-checkout or ephemeral-path scenarios while still surfacing missing paths for truly absent entries.

## Key Rules
- Only apply this skip to updates where a materialized entry already exists; missing entries should still surface real errors.
- Check path existence after normalization so you validate the exact path the reconciler would use.
- Record skipped updates distinctly from failures so operators know the existing entry was intentionally preserved.
- Limit the exception to local-path sources; remote sources need normal failure handling.
- Log the reason for the skip so future debugging can tell path drift from install breakage.

## Example Application
If a developer switches away from a temporary worktree that contained a local marketplace path, keep the previously materialized marketplace entry instead of failing an update against the now-missing worktree path. The next valid local path or explicit reinstall can replace it later.

## Anti-Patterns (What NOT to do)
- Do not attempt updates from dead local paths just to fail loudly; you destroy signal-to-noise while preserving nothing.
- Do not apply this rule to brand-new missing entries; if nothing working exists yet, the user needs the error.
