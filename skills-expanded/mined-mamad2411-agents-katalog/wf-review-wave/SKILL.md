---
name: wf-review-wave
description: Run the open wave's required review lanes and record typed review evidence ahead of closure. The Review wave workflow.
---

# Review a wave (Wavefoundry skill)

This skill is a thin pointer: the workflow lives in `docs/prompts/review-wave.prompt.md`. Read that document and follow it; do not improvise the steps from this summary.

- Start from the `wf_review_wave` MCP tool for guided actions; record evidence with `wf_review_event` (dry-run first, then create).
- Reminder: review evidence is typed and executable; approvals bind to the current receipt and lapse when the reviewed surface changes.
