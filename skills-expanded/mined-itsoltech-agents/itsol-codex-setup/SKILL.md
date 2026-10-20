---
name: itsol-codex-setup
description: "Preview or change ITSOL Codex roles, model presets, and global or project agent limits."
---

# ITSOL Codex Setup

Configure four execution roles while keeping domain knowledge in ITSOLPowers skills. Run this only in the main agent; never delegate user or project configuration writes.

## Workflow

1. Resolve `itsol-workflow-mode` and `itsol-execution-policy`. Configuration authority does not authorize unrelated edits.
2. Choose scope:
   - `user` for `${CODEX_HOME:-~/.codex}`; default when the user does not specify.
   - `project` for `<project>/.codex`; use only when the user asks for repository-scoped roles.
3. Choose preset: `balanced` by default, or explicit `economy` / `quality`. Read [references/presets.md](references/presets.md) when explaining or changing routing.
4. Resolve this skill directory and run its `scripts/configure-codex.mjs install` command with `--dry-run` first.
5. Report scope, preset, target paths, conflicts, and model-entitlement limitation. If the user explicitly requested configuration and dry-run has no blocker, run install without another planning pause. Let platform filesystem approval apply normally.
6. For a conflicting existing limit or modified managed file, explain the exact conflict and request explicit `--force` authority. Force never overwrites an unmanaged role.
7. Run `$itsol-codex-doctor` after installation and advise a new task or application reload before relying on newly discovered roles.

Default commands:

```bash
node <this-skill-dir>/scripts/configure-codex.mjs install --scope user --preset balanced --dry-run
node <this-skill-dir>/scripts/configure-codex.mjs install --scope user --preset balanced
```

Use `--json` for machine-readable output. Use `--codex-home <path>` or `--project-root <path>` only for an explicit alternate target or isolated verification.

## Update And Uninstall

- Re-run install with the desired preset to update unchanged managed roles.
- Preview removal with `uninstall --dry-run`, then run `uninstall`.
- Modified managed role files are preserved unless force is explicit. During uninstall, a user-changed `config.toml` is always preserved even with force; force may remove managed roles/state, leaves the backup for manual recovery, and reports the remaining config as partial cleanup.
- Never introduce `maxTurns` or use a timeout as completion.

Read [references/safety.md](references/safety.md) before using force, uninstalling, or handling a partial/blocked result.

## Result Contract

Report command status, scope, preset, changed files, config backup, preserved items, doctor findings, unverified model availability, and whether a new task/reload is recommended. Do not claim effective sandbox enforcement from static configuration.
