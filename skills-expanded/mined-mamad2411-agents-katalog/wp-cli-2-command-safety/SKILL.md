---
name: wp-cli-2-command-safety
description: Plans and reviews WP-CLI 2 commands before execution. Use when an agent must identify the effective WordPress target, classify command risk, choose previews or backups, review shell composition, or decide whether a proposed WP-CLI command is safe to run.
license: MIT
compatibility: Requires WP-CLI 2.x; guidance is validated against WP-CLI 2.12.0. The optional guard requires Python 3.10 or newer.
---

# WP-CLI 2 Command Safety

Use this skill before running or recommending WP-CLI commands, especially against remote or production-like targets.

## Initial Checks

1. Run `wp --info` and `wp cli version`.
2. Resolve `--path`, `--url`, aliases, `--ssh`, `--http`, and config precedence.
3. Confirm the WordPress installation with read-only commands.
4. Inspect `wp help <command>` on the target; custom packages can change available commands.
5. Classify the action using the command risk matrix.

## Planning Pattern

Use this sequence:

1. **Inspect** current target and state.
2. **Preview** with a documented dry run or narrowed query when supported.
3. **Back up/export** before risky database or filesystem mutations.
4. **Mutate** only with approved scope and rollback.
5. **Verify** the intended state and important invariants.
6. **Record** target, command, result, and verification without secrets.

Do not append guessed flags. `wp core update`, for example, does not gain safety from an unsupported `--dry-run` flag.

## Guard Script

Read help and run its tests before enabling the hook:

```powershell
python .agents/plugins/wp-cli-2/skills/wp-cli-2-command-safety/scripts/wp-cli-command-guard.py --help
python .agents/plugins/wp-cli-2/skills/wp-cli-2-command-safety/scripts/wp-cli-command-guard.py --self-test
```

The guard is conservative and intentionally asks for custom/unclassified commands. It never replaces normal command permissions or human change control.

## Workflow

- [Safe command execution workflow](workflows/safe-command-execution-workflow.md)

## Resource

- [Command risk matrix](resources/command-risk-matrix.md)
