---
name: wf-plan-change
description: Plan a change of any kind (feature, bug fix, enhancement, refactor, documentation, tech debt, task, maintenance, operations) and produce a consolidated change doc ready for wave admission. The Plan change workflow.
---

# Plan a change (Wavefoundry skill)

This skill is a thin pointer: the workflow lives in `docs/prompts/plan-change.prompt.md`. Read that document and follow it; do not improvise the steps from this summary.

- The workflow selects the scaffold among the `wf_new_<kind>` MCP creation tools (bug, enhancement, refactor, documentation, tech debt, task, maintenance, operations, change) by change kind, then admits the doc with `wf_add_change`.
- Gate reminder: planning writes docs only; no repository code edits until the stage gate (change doc, wave admission, recorded readiness) is satisfied.
