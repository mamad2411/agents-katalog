---
name: prototype
description: Deprecated compatibility alias for logic-wiring; use the primary clickable/state-backed wiring skill instead
type: execution
version: v0.0
argument-hint: "[optional: topic, --variant N]"
deprecated: true
replaced_by: logic-wiring
---

# Prototype

Invoke as `$prototype`.

This command is a deprecated compatibility alias for `$logic-wiring`. Use `$logic-wiring` for all new work.

## Routing

Immediately route to `$logic-wiring` with the same arguments. Do not duplicate or reinterpret the build process here. The primary skill owns:

- consuming the visual screens produced by `$build-ui-screens`
- making each variation's flow clickable and state-backed (plus runnable CLI/API/infra logic)
- flow-reachability acceptance with one binding alignment gate per variation
- advancing `ui_experiments[].build_ledger[]` entries from `minimum-ui-reached` to `wired`
- prototype build state in `design/prototype-build-plan-*.md` and `design/**/flow-tree-*.yaml`
- handoff to `$uat --variant-evaluation`, then `$consolidate-prototypes`

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
