---
name: pi-subagent
description: Delegate substantial coding, refactoring, debugging, or review work to an isolated Pi agent that inherits the current Pi provider, model, and thinking level. Use when a task benefits from a separate context or independent worker.
version: 2.0.0
license: MIT
metadata:
  hermes:
    tags: [Coding-Agent, Pi, Subagent, Code-Review, Refactoring]
    related_skills: [requesting-code-review, writing-plans, test-driven-development]
---

# Pi Subagent

Delegate work to a fresh Pi process while preserving the dispatching session's exact model configuration.

## Dispatch order

1. If a `subagent` tool is available, prefer it. Use a general-purpose agent whose definition omits `model`; omission makes the Pi subagent inherit both the active model and thinking level. Never select an agent with a pinned model when inheritance is required.
2. Otherwise run the bundled Pi subprocess wrapper:

```bash
skill_dir="${PI_CODING_AGENT_DIR:-$HOME/.pi/agent}/skills/autonomous-ai-agents/pi-subagent"
task_file="$(mktemp)"
trap 'rm -f "$task_file"' EXIT
cat >"$task_file" <<'TASK'
Describe the delegated task, constraints, relevant paths, expected output, and verification command here.
TASK
"$skill_dir/scripts/run-pi-subagent.sh" --cwd "$PWD" --task-file "$task_file"
```

The wrapper uses:

- `PI_PROVIDER` and `PI_MODEL` for the exact active Pi model
- `PI_REASONING_LEVEL` for the current effective thinking level
- `--no-session` for isolated context
- `--no-skills` to prevent recursive delegation

Do not use `PI_THINKING`; `PI_REASONING_LEVEL` is Pi's documented effective value.

## Delegation rules

- Delegate a concrete, bounded task with file paths, constraints, acceptance criteria, and test commands.
- Use the caller's current working directory unless the task names another repository.
- Start one worker by default. Use parallel workers only for independent tasks and keep the count small.
- Never invoke an external coding-agent CLI; delegation must stay within Pi.
- Treat the worker's response as a handoff, not proof. Inspect changed files and rerun relevant tests in the parent session.
- Report the inherited `provider/model` and thinking level when the user asks which configuration was used.

## Common tasks

- Implement a bounded feature in an isolated context.
- Diagnose a complex failure without filling the parent context.
- Independently review a diff or pull request.
- Work on separate issues in separate worktrees.
