---
name: use-luna-subagents
description: Configure, validate, repair, and use a personal gpt-5.6-luna custom Codex agent for bounded delegated or parallel work. Use when the user asks to set up a Luna worker, verify or repair a Luna subagent configuration, or delegate clear repeatable, high-volume, research, testing, review, or implementation tasks to Luna-backed subagents.
---

# Use Luna Subagents

Configure a persistent `luna_worker` custom agent, then use it selectively for bounded work while the parent agent retains orchestration and final verification.

## Reconcile the custom agent

1. Resolve this skill directory and run:

   ```bash
   python3 scripts/reconcile_luna_worker.py
   ```

2. Treat exit statuses as follows:
   - `0`: the agent is ready.
   - `2`: installation or reconciliation is required. Review the emitted unified diff.
   - `3`: configuration is blocked or invalid. Resolve the reported blocker before continuing.

3. When a change is required, request approval through the execution environment and run:

   ```bash
   python3 scripts/reconcile_luna_worker.py --apply
   ```

   Write only `~/.codex/agents/luna-worker.toml`. The script backs up a conflicting file before replacing it. Do not rewrite `~/.codex/config.toml`.

4. If the script reports `[agents].enabled = false`, show the smallest diff that changes only that value to `true`, obtain approval, preserve every other setting, and validate the TOML again.

5. Use `codex --version` as an informational compatibility check. If the wrapper is broken, use the package version reported by the script. When compatibility remains uncertain, consult the current official Codex manual or documentation rather than guessing.

6. Attempt a harmless `luna_worker` smoke task. If the current session does not expose a newly installed custom agent, tell the user to restart Codex or open a fresh thread; do not claim the agent was runtime-validated.

## Decide whether to delegate

Use Luna workers when the work is clear, bounded, and benefits from isolation or parallelism, including:

- focused codebase exploration or document processing;
- repetitive or high-volume transformations;
- independent implementation slices with exclusive file ownership;
- tests, reviews, triage, or evidence gathering.

Keep work with the parent agent when it is trivial, highly coupled, ambiguous, or primarily requires synthesis and judgment.

Use one worker by default. Use multiple workers only for genuinely independent tasks. Never assign overlapping write scopes to concurrent workers.

## Run the delegated workflow

1. State each worker's objective, boundaries, available inputs, expected output, and verification requirement.
2. Spawn the custom agent named `luna_worker`. Use an explicit Luna model override only when the active tool surface supports it; never silently substitute a different model.
3. Let the worker inspect, edit, and test within the parent task and permission boundary. The agent intentionally inherits the parent's sandbox.
4. Wait for all requested workers. Route follow-up instructions when a result is incomplete or off-scope.
5. Have the parent reconcile conflicts, inspect material changes, run proportional final verification, and deliver the consolidated result.

Do not delegate merely to demonstrate the skill. Do not represent a configured file as proof that the requested model actually ran.
