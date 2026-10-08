---
name: fable-sonnet
description: >
  Run fable-mode execution discipline on Claude Sonnet. Routes the task to the
  @fable-worker-sonnet agent, whose definition carries the staged loop with
  step-3 verification enforced hardest (Sonnet's known gap), optionally followed
  by a cold @fable-verifier pass. Trigger when the user explicitly asks for
  thorough/systematic/"deep work" handling on Sonnet ("fable on sonnet", "stage
  this on sonnet", "deep work mode, sonnet"). The balanced default between Haiku
  (cheap/fast) and Opus/Fable (peak reasoning). Do NOT use for ordinary single-pass
  tasks.
---

# Fable Mode — Sonnet (v3, agent-routed)

v3 change: the worker is a real agent definition (`agents/fable-worker-sonnet.md`)
invoked by name, not a prose briefing the model can soft-ignore. Its system
prompt carries the loop and the operational rules; this skill only routes.

If a task has one obvious correct approach and fits in a single pass, skip this
loop and do it directly.

## How to run it

1. Confirm `fable-worker-sonnet` appears in the available agent types. If not,
   fall back to inline: spawn a general-purpose Sonnet agent and pass it the
   rules verbatim from `agents/fable-worker-sonnet.md`.
2. Spawn **@fable-worker-sonnet** via the Task tool (`subagent_type:
   "fable-worker-sonnet"`). Brief it with: the task, the exact output path(s),
   relevant context, and the pass condition its deliverable must satisfy —
   name the check, don't leave it to taste.
3. For independent sub-parts, spawn multiple workers concurrently and merge.
   Cap concurrency at a handful. Workers do not spawn workers.
4. For high-stakes deliverables, follow with **@fable-verifier**, briefed with
   only the spec and the artifact path — not the worker's report.
5. Relay results and anything marked unverified.
6. **Mandatory delivery gate:** before presenting the result to the user, invoke
   the **double-check** skill on the finished deliverable. If step 4's verifier
   already cold-checked the *final* document, double-check runs only the seam
   check — its own rules handle that. Do not skip the gate.
