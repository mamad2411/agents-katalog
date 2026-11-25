---
name: mode
description: Switch how much code the AI writes - between guided (you write all code), collab (split), and autopilot (AI writes it). Use when the user says "set mode to X", "switch to autopilot", "let me write it myself", "just build it for me", or asks what the modes are.
---

Run the workflow in [`docs/playbooks/mode.md`](../../../docs/playbooks/mode.md).

Read the current mode from `PROJECT.md`, confirm the trade-off of the target mode
in one line, update the `Mode` field and `**Current mode:**` line in `PROJECT.md`
(the single source for mode), and confirm the new rules. Full definitions:
[`docs/MODES.md`](../../../docs/MODES.md).
