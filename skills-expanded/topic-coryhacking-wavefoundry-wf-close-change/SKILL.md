---
name: wf-close-change
description: Close one admitted change inside the open wave with wf_close_change, marking it complete and activating its dependents; never closes the wave (Close wave is the only wave close). The Close change workflow.
---

# Close a change (Wavefoundry skill)

This skill is a thin pointer: the workflow lives in `docs/prompts/close-change.prompt.md`. Read that document and follow it; do not improvise the steps from this summary.

- Prefer the `wf_close_change` MCP tool; run `dry_run` (the default) first, then `create` once the dry run is clean.
- Run it after Review wave has cleared the change: a completed change cannot be reopened, and the tool records no review evidence.
- Close wave (`wf-close-wave`) remains the only wave close, whatever the change count.
