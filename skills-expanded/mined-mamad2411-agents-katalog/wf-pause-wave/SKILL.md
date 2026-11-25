---
name: wf-pause-wave
description: Park the current session's wave state in the durable handoff artifact when stopping work or handing off. The Pause wave workflow.
---

# Pause a wave (Wavefoundry skill)

This skill is a thin pointer: the workflow lives in `docs/prompts/pause-wave.prompt.md`. Read that document and follow it; do not improvise the steps from this summary.

- Prefer the `wf_pause_wave` MCP tool; it also closes any open edit gates.
- Write the durable handoff artifact; do not improvise a summary in its place.
