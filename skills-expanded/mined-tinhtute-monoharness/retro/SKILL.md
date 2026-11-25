---
name: retro
model: opus
description: "Session retrospective: evidence-cited, severity-ranked findings about the agent's environment, then one user-approved fix — a guard or a rerun-gated experiment, including a new skill, script or global rule once its pattern recurs across sessions (`retro codify` mines several). Invoke only from a poteto playbook step or when the user asks for it by name."
---

Lead with the top finding and its evidence.

Follow `references/retro.md` — it holds this skill's operating logic, including the digest script and the approval gate before any edit. A missing `zharness` binary is never a reason to stop.

Defer to: `work` when the fix grows into a locked initiative; `handoff` absorb when closing a plan.
