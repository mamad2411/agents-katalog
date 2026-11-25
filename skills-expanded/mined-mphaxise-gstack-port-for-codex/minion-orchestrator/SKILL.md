---
name: minion-orchestrator
description: Coordinate Codex subagents, shell jobs, or background investigations with explicit ownership, sandbox limits, status tracking, and bounded parallelism.
---

# Minion Orchestrator

Use this skill when the user wants durable background work, multiple independent investigations, queued tasks, or explicitly requested Codex subagents.

## Workflow

1. Split work into independent jobs.
2. Decide the execution shape:
   - main-thread tool calls for short serial work
   - shell sessions for local commands with trackable output
   - Codex subagents only when the user explicitly asked for subagents or parallel agent work
   - upstream GBrain minions only when that external runtime is actually installed and in scope
3. For each job, define:
   - goal
   - inputs
   - command or agent path
   - expected artifact
   - timeout or stop condition
4. Run jobs only with available local tooling and permissions.
5. Track status and collect outputs.
6. Merge findings into one report with unresolved gaps.

## Codex Adaptation

- Prefer Codex tool calls, shell sessions, or explicit subagents available in the current session.
- Codex subagents inherit the current sandbox and approval policy; plan for approval blockers in inactive child threads.
- Use subagents mainly for independent read-heavy exploration, test triage, log analysis, or summarization.
- Treat upstream GBrain minions as an optional external runtime, not something bundled by this port.
- Use parallelism only for independent read-only work or isolated outputs.
- For mutating work, define ownership before starting the job.

## Guardrails

- Do not spawn unbounded background work.
- Do not spawn Codex subagents unless the user explicitly requested subagents or parallel agent work.
- Do not lose track of running sessions.
- Do not use parallelism when jobs mutate the same files.
- Do not claim durable worker semantics unless an actual durable worker runtime is present.
