---
name: factory-droid
description: "Use this skill when delegating coding work to Factory Droid's droid CLI for code analysis, edits, specification-first implementation, worktree isolation, or multi-agent missions. Do not use it for small direct edits or when Factory Droid is unavailable."
license: MIT
compatibility: "Requires macOS or Linux, Factory Droid's droid CLI, and an authenticated Factory account or configured BYOK provider."
---

# Factory Droid

Use [Factory Droid](https://factory.ai) through the `droid` CLI to delegate coding tasks. Prefer `droid exec` for bounded, non-interactive work; use interactive `droid` only when a user needs to steer the session.

## Before You Delegate

1. Confirm the task warrants an external coding agent. For a small, well-scoped edit, work directly.
2. Work inside the target Git repository and set the command working directory explicitly.
3. Verify installation and authentication before assigning a real task:
   ```sh
   droid exec -o json --auto low "Respond with: OK"
   ```
4. Use the lowest autonomy level that completes the task. Never use `--skip-permissions-unsafe` outside a disposable sandbox.

For login and BYOK details, read [references/authentication.md](references/authentication.md).

## One-Shot Tasks

```sh
# Read-only analysis
droid exec "Map the authentication flow."

# Bounded implementation and local validation
droid exec --auto medium "Add retry logic to API calls, update focused tests, and report changed files."

# Parseable result for an orchestrator
droid exec -o json --auto low "List the public functions in src/auth.py."
```

Use a prompt file rather than shell quoting for complex instructions:

```sh
droid exec --auto medium -f .factory/task.md
```

## Autonomy and Isolation

| Level | Use for | Avoid for |
|---|---|---|
| Default | Reconnaissance, reviews, plans | Any file change |
| `--auto low` | Safe, bounded edits | Dependency installs or commits |
| `--auto medium` | Implement, test, and make local commits | Push or deployment |
| `--auto high` | Explicitly authorized push/deploy workflows | Routine development |

For the full decision matrix, read [references/autonomy-levels.md](references/autonomy-levels.md).

Use a named worktree for non-trivial tasks so changes are reviewable and isolated:

```sh
droid exec --worktree fix-auth-retry --auto medium "Fix the auth retry bug, run focused tests, and leave changes uncommitted for review."
```

## Specification-First Work

Use `--use-spec` for a change whose requirements or architecture are unclear enough that a plan reduces rework:

```sh
droid exec --use-spec --auto medium "Design and implement user profiles with avatar upload."
```

It costs more because Droid plans and implements. Do not choose it for a mechanical edit.

## Mission Mode

Use mission mode only for a clear, multi-file objective that benefits from worker and validator roles:

```sh
droid exec --mission --auto high --worktree mission-auth-refactor -f mission.md
```

Read [references/mission-mode.md](references/mission-mode.md) before writing the mission specification. For model selection and provider-specific identifiers, read [references/model-ids.md](references/model-ids.md).

## Output and Follow-Through

Request concrete outcomes: changed files, tests run and results, remaining risks, and a session ID when relevant. Inspect the working tree and run the project’s own checks before claiming completion. A Droid result is evidence, not proof.

For session continuation, reasoning effort, tool controls, explicit `--cwd`, and local session search, read [references/advanced-operations.md](references/advanced-operations.md).

## Choosing an Agent

Read [references/delegation-comparison.md](references/delegation-comparison.md) when Factory Droid is one of several viable coding agents.

## Pitfalls

- `droid exec` is non-interactive; do not allocate a TTY unless using the interactive `droid` application.
- Dirty worktrees may be preserved. Inspect the printed path before cleanup; never delete a worktree by guesswork.
- Use `-f` for prompts containing shell-sensitive text.
- Treat model IDs, provider availability, and pricing as version-sensitive. Verify them rather than presenting examples as permanent facts.
