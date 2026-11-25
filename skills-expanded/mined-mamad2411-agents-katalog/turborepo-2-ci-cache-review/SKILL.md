---
name: turborepo-2-ci-cache-review
description: Reviews Turborepo 2 CI commands, remote cache readiness, environment variables, secret handling, and command safety. Use when editing CI task commands or configuring Turborepo remote cache.
license: MIT
compatibility: Optional command guard script requires Python 3.
---

# Turborepo 2 CI and Cache Review

Use this skill for CI command review, remote cache setup, and safe handling of Turborepo cache credentials.

## When to Use

Use this skill when the user asks to:

- Review CI commands that run `turbo`.
- Configure remote caching.
- Add `TURBO_TOKEN` or `TURBO_TEAM` to CI.
- Diagnose remote cache misses in CI.
- Replace unsafe or deprecated Turborepo command flags.
- Review command safety before running installs, codemods, or migrations.

## Workflow Reference

Use this workflow for repeatable CI/cache review:

```text
workflows/turborepo-2-ci-cache-review-workflow.md
```

## Resource Reference

Use this checklist:

```text
resources/turborepo-2-ci-cache-checklist.md
```

## Example Reference

Use this example for command patterns:

```text
examples/turborepo-2-ci-command-patterns.md
```

## Script Reference

Before using the command guard script:

```bash
python3 .agents/plugins/turborepo-2/skills/turborepo-2-ci-cache-review/scripts/turborepo-2-guard-command.py --help
```

The script is also used by `hooks.json` as a `PreToolUse` command guard.

## Review Method

1. Confirm the repository package manager.
2. Confirm CI uses the same package manager and lockfile.
3. Confirm `turbo` is available through the pinned repository dependency.
4. Prefer `turbo run` in CI for clarity.
5. Ensure all CI tasks are registered in `turbo.json`.
6. Confirm remote cache variables are configured as CI secrets, not inline commands.
7. Use cache controls intentionally:
   - local and remote read/write for normal CI.
   - read-only remote cache for untrusted branches when appropriate.
8. Avoid deprecated `--parallel`.
9. Avoid deleting caches as a first debugging step.
10. Separate Turborepo command review from CI-provider YAML syntax unless a CI plugin is active.

## Secret Safety

Never write these values into repository files or command strings:

- `TURBO_TOKEN`
- `TURBO_TEAM` when it is considered sensitive by the organization
- `TURBO_REMOTE_CACHE_SIGNATURE_KEY`
- Provider tokens used to fetch Turborepo credentials

Use placeholders in examples and secret storage in real CI systems.
