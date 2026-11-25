---
name: agent-kit-cost
description: Spend fewer tokens on agent work by routing each task to the cheapest model tier that can finish it, giving every agent a checkable finish line, and not spawning agents the task doesn't need. Use WHENEVER you are about to spawn a subagent, fork, parallel agents or a Workflow, choose a model for an agent, plan a multi-agent job, switch models mid-session, or the user says "cost", "cheaper agents", "token budget", "which model", "too many agents", "ลดค่า token". Ships a PreToolUse hook that nudges every Agent call that sets no model.
---

# Agent cost

Most agent spend is waste of three kinds: a frontier model doing a search, an agent with no finish
line looping, and an agent spawned for work that was five tool calls. Each rule below cuts one of them.
Prompt-cache rules (byte-stable prefixes, forks, SendMessage, TTL) live in
[`../prompt-cache/SKILL.md`](../prompt-cache/SKILL.md); follow both.

## Rules

1. **Do it inline first.** A lookup whose target you know, or a handful of tool calls, costs less in
   this session than any agent: an agent re-reads context, and its summary drops detail you then
   redo. Spawn only for independent work that can run in parallel, or a side task that would flood
   this context with file dumps.
2. **Route by tier, start cheap.** Set `model` on every Agent call:

   | Work | `model` |
   |---|---|
   | search, file inventory, reading logs, collecting facts | `haiku` |
   | a bounded code change with a test, a review of one diff | `sonnet` |
   | planning, multi-file architecture, a task a cheaper tier already failed | omit (inherit) or `opus` |

   Escalate one tier when an agent fails its finish line, not before. The orchestrator plans; workers
   on cheaper tiers execute.
3. **Every brief has a finish line.** Goal, scope (files, what not to touch), what to return, and how
   done is checked (a command and its expected output, a test name, a count). "Improve this" with no
   check is how an agent loops.
4. **Split big jobs into checkpoints.** Several small agents with testable outputs beat one long agent
   you can only judge at the end. Small jobs stay single-session: multi-agent overhead (briefs,
   handoffs, re-reading) outweighs the parallelism.
5. **Don't switch the session's model mid-task.** The prompt cache is per model; a switch makes the
   new model read the whole history at full price. Run `/compact` or start a fresh session first.
   A subagent on another tier doesn't touch the parent's cache, but starts its own prefix cold, so
   give siblings the same brief prefix.
6. **Effort is the user's knob.** Don't raise an agent's `effort` unless the user or the project's
   instructions ask. Top effort tiers buy little accuracy for many more tokens.
7. **Pre-allow what is reversible.** An agent stalled on a permission prompt burns wall-clock and
   context. Allowlist reads, tests and builds in `settings.json` (`/fewer-permission-prompts`); keep
   deletes, pushes and anything outward-facing behind a confirmation.
8. **The final report stands alone.** Written for someone who didn't watch: what changed, the proof
   (test or command output), what's left. Relay what matters; the user never sees an agent's report.

## The hook

`scripts/agent_guard.py` is a PreToolUse hook on `Agent`. When a call sets no `model` (forks
excepted: they always inherit), it adds the tier table to the context. It never blocks. Register it in
the project's or user's `settings.json`:

```json
{"hooks": {"PreToolUse": [{"matcher": "Agent", "hooks": [{"type": "command",
  "command": "uv run --script /path/to/agent-kit/cost/scripts/agent_guard.py"}]}]}}
```

`uv run --script scripts/agent_guard.py --selftest` checks it.
