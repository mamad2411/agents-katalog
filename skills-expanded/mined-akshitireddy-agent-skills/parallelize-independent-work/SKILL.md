---
name: parallelize-independent-work
description: Delegate independently verifiable work when subagents can improve completion time or review quality.
---

# Delegate independent outcomes

When a task contains concrete outcomes that can progress independently, use
subagents if available and authorized and the expected benefit exceeds the
coordination cost. Useful lanes include a bounded investigation, an isolated
implementation, or review of a stable artifact. Keep simple or tightly coupled
work local. Reconsider the split when new independent requirements arrive.

Give each agent a clear outcome and stopping condition, exact scope, edit
ownership or a read-only boundary, and relevant verification expectations.
Delegate early when that enables useful overlap. Do not duplicate another
lane or invent work to fill slots. Model selection follows the user and host.

Assume the workspace is shared unless told otherwise. Reserve one writer per
file and one owner for exclusive resources such as a browser fixture, device,
or deployment. Subagents inherit the task's authorization, not additional rights.

The coordinator reviews returned findings and diffs, integrates dependent work,
and verifies the combined result after the tree is stable. Collect all active
results before completion or explicitly stop obsolete lanes. Report the
integrated outcome and evidence rather than an activity tally.
