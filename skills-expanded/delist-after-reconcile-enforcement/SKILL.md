---
name: delist-after-reconcile-enforcement
description: "Run delist or blocklist enforcement after synchronization so removals update both metrics and downstream refresh signals."
metadata:
  author: ychampion
---

# SKILL: Delist-After-Reconcile Enforcement
**Domain:** extensions-mcp
**Trigger:** Use when an extension or plugin system must enforce removals even if the install or update pass made no additions.
**Source Pattern:** Distilled from reviewed post-sync extension policy enforcement flows.

## Core Method
Apply delist or policy enforcement after synchronization finishes so removal decisions operate on the freshest materialized state. Treat removals as first-class changes that update metrics and propagate the same downstream refresh signal used for installs. This keeps policy enforcement visible and ensures callers reload when the live set changed through removal rather than addition.

## Key Rules
- Run delist checks after synchronization, not before, so policy decisions see the latest installed state.
- Count removals explicitly and include them in change metrics.
- Let removals flip the same downstream changed flag or refresh contract used by installs and updates.

## Example Application
If a headless bootstrap finds that one installed extension was later delisted, remove it after registry sync and return a changed signal so the command surface reloads.

## Anti-Patterns (What NOT to do)
- Do not hide removals as silent cleanup.
- Do not skip delist enforcement when no new installs occurred.
- Do not keep separate refresh paths for installs and removals when both affect the live set.
