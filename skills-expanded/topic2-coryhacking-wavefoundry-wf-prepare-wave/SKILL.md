---
name: wf-prepare-wave
description: Confirm a wave's readiness before implementation (docs validation, gardening, lint, and the prepare-phase council gate). The Prepare wave / Ready wave workflow.
---

# Prepare a wave (Wavefoundry skill)

This skill is a thin pointer: the workflow lives in `docs/prompts/prepare-wave.prompt.md`. Read that document and follow it; do not improvise the steps from this summary.

- Prefer the `wf_prepare_wave` MCP tool: `dry_run` to validate, `ready` to record readiness without opening, `create` to prepare and open.
- The prepare-phase council review runs as the last prepare step; `wave-council-readiness` must be recorded before the wave readies.
- Gate reminder: only one wave may be OPEN at a time; readiness alone never takes that slot.
