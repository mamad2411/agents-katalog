---
name: are-implement
description: Execute implementation with and without ARE documentation (experimental)
disable-model-invocation: true
---

Execute the implementation phase with and without ARE documentation to measure impact.

<execution>
Run the implement command to execute code changes in both environments.

## Steps

1. **Read version**: Read `.claude/ARE-VERSION` → store as `$VERSION`. Show the user: `agents-reverse-engineer v$VERSION`

2. **Run the implement command**:
   ```bash
   npx agents-reverse-engineer@$VERSION implement --backend claude $ARGUMENTS
   ```
   Note: When `--plan-id <id>` is provided, the task description is loaded from the stored plan — no need to pass it explicitly.

3. **Wait for completion** — the command runs two sequential AI implementation sessions (without docs, then with docs) and outputs a comparison table.

4. **On completion**, summarize the comparison results:
   - Implementation metrics (files created/modified, lines added/deleted)
   - Test results (if `--run-tests` was used)
   - Build and lint results (if `--run-build` / `--run-lint` was used)
   - Cost and latency comparison
   - Quality evaluation scores (if `--eval` was used)

This re-uses branches created by `/are-plan` and executes the implementation in both worktrees:
- **With ARE docs**: Full documentation available during implementation
- **Without ARE docs**: Source code only (ARE artifacts stripped)

The comparison measures how much ARE documentation improves implementation quality.

**Options:**
- `--eval`: Run AI quality evaluator on both implementations
- `--eval-model <name>`: Model for the evaluator (default: same as --model)
- `--model <name>`: AI model to use for implementation
- `--task-slug <slug>`: Reference existing plan by slug (default: auto-generate from task)
- `--plan-id <id>`: Reference existing plan by ID (shown by `are plan` on completion)
- `--run-tests`: Execute test suite and include results in metrics
- `--run-build`: Execute build and verify success
- `--run-lint`: Run linter and include error/warning counts
- `--dry-run`: Show what would happen without executing
- `--list`: List all saved implementation comparisons
- `--show <id>`: View a previous comparison by date
- `--force`: Overwrite existing branches for the same task
- `--debug`: Show verbose AI execution details
</execution>
