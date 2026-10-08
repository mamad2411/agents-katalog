---
name: wf-close-wave
description: Close and archive a wave after delivery review, reconciling every AC and task checkbox. Closure is operator-owned. The Close wave workflow.
---

# Close a wave (Wavefoundry skill)

This skill is a thin pointer: the workflow lives in `docs/prompts/close-wave.prompt.md`. Read that document and follow it; do not improvise the steps from this summary.

- Prefer the `wf_close_wave` MCP tool; run `dry_run` freely to validate close readiness.
- Gate reminder: closure is operator-owned. Call `mode="create"` only when the operator explicitly instructs closure in the current request; closure is never inferred from adjacent actions such as "run the review" or "fix the tests".
- Single change: Close change (`docs/prompts/close-change.prompt.md`) marks one change `complete` inside the open wave; Close wave is still the only wave close.
