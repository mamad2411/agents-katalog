---
name: fable-fable
description: >
  Run fable-mode execution discipline on Claude Fable 5.1 — the top of the
  escalation ladder and the strongest staged run available. Routes the task to
  the @fable-orchestrator agent with its model overridden to Fable
  (`model: "fable"`), which stages the work, delegates artifact production to
  @fable-worker-sonnet / @fable-worker-haiku, and cold-checks deliverables with
  @fable-verifier. Trigger when the user explicitly asks for
  thorough/systematic/"deep work" handling on the strongest model ("fable on
  fable", "stage this on fable", "deep work mode, fable", "run this on 5.1"),
  or when a fable-opus run reports the task exceeds Opus's ceiling. Benchmarked
  2026-09-02: zero correctness delta on Fable 5.1 at ~1.1× tokens, ~2× wall —
  a provenance runner, not an accuracy runner. Do NOT use for ordinary
  single-pass tasks — prefer fable-opus, fable-sonnet, or fable-haiku when the
  task doesn't need peak reasoning. Fable is plan-included; bulk work still
  routes down-tier.
---

# Fable Mode — Fable 5.1 (v3, agent-routed)

Same structural delegation as fable-opus: the orchestrator is a real agent
definition (`agents/fable-orchestrator.md`) with no Write/Edit tool, so it
cannot do the work inline. The only difference from fable-opus is the model the
orchestrator runs on. Fable 5.1 is the top of the ladder (Haiku → Sonnet → Opus
→ Fable → user); gaps it cannot close go to the user.

Fable 5.1's characteristic gaps under this discipline: none measured
(benchmarked 2026-09-02, 16 paired runs, n=2 per cell: 100/100 in every cell,
both arms; skill cost ~1.1× tokens, ~2× wall). This is a provenance runner —
worklog, reproducible checks, flagged judgment calls — not an accuracy runner.
The orchestrator definition keeps the frontier-tier guards (external-artifact
verification, scope rule, replan budget) because those produce the trail.

If a task has one obvious correct approach and fits in a single pass, skip this
loop and do it directly. On a Fable-class model the stage map is ceremony for
anything short of multi-session or many-file work.

## How to run it

1. Confirm the fable agents are installed (`fable-orchestrator`,
   `fable-worker-sonnet`, `fable-worker-haiku`, `fable-verifier` appear in the
   available agent types) AND the Agent/Task tool accepts `model: "fable"`.
   - Agents missing → fall back to the inline method: spawn a general-purpose
     agent with `model: "fable"` and pass it the Core loop and operational
     rules verbatim from `agents/fable-orchestrator.md`.
   - `"fable"` not accepted as a model → say so and run fable-opus instead.
   - Per-invocation `model` override is documented for Claude Code
     (code.claude.com/docs/en/sub-agents: "the per-invocation `model`
     parameter" outranks the definition's frontmatter; `fable` is a listed
     alias) and confirmed on the Cowork Agent tool. On a runtime that lacks
     it, copy `agents/fable-orchestrator.md` to
     `agents/fable-orchestrator-fable.md`, set `name: fable-orchestrator-fable`
     and `model: fable`, and route to that instead.
2. Spawn **@fable-orchestrator** via the Task tool (`subagent_type:
   "fable-orchestrator"`, `model: "fable"`). Brief it with: the user's task,
   the output directory, relevant session context, and any user-set limits
   (warning threshold, worker cap, deadline).
3. Do not restate the Core Loop or operational rules in the briefing — the
   orchestrator's agent definition carries them. Brief the task, not the
   method.
4. When it returns, relay the result, every stage it marked unverified, and its
   recommendations (surfaced scope it did not build).
5. **Mandatory delivery gate:** before presenting the result to the user, invoke
   the **double-check** skill on the finished deliverable. If the orchestrator's
   fable-verifier already cold-checked the *final* document (not just
   intermediate outputs), double-check will detect that and run only the
   synthesis-seam check instead of a full panel — its own rules handle this. Do
   not skip the gate; the user relies on it instead of re-checking the work
   themselves.

## Known limitation

Same side door as fable-opus: the orchestrator keeps Bash for verification
commands, and Bash can technically create files. Its definition forbids that
use.
