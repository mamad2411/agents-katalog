---
name: create-ui-experiment
description: Deprecated compatibility alias for build-ui-screens; use the primary visual UI screen builder instead
type: execution
version: v0.0
argument-hint: "[approved-ui-experiment]"
deprecated: true
replaced_by: build-ui-screens
---

# Create UI Experiment

Invoke as `$create-ui-experiment`.

This command is a deprecated compatibility alias for `$build-ui-screens`. Use `$build-ui-screens` for all new work.

## Routing

Immediately route to `$build-ui-screens` with the same arguments. Do not duplicate or reinterpret the screen-building process here. The primary skill owns:

- building the visual UI screens for one approved UI branch as an ordered element-batch loop
- the per-batch visual checkpoint and minimum-UI stop rule
- writing `ui_experiments[].build_ledger[]` entries with fake/fixture/local/in-memory data
- review evidence in `experiment_path` and `review_evidence` on `design/**/flow-tree-*.yaml`
- handoff to `$logic-wiring` to make the screens clickable and state-backed

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
