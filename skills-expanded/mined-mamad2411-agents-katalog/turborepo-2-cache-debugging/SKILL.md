---
name: turborepo-2-cache-debugging
description: Debugs Turborepo 2 cache misses, suspicious cache hits, task hash inputs, environment variables, outputs, and remote cache behavior. Use when builds unexpectedly rerun or replay incorrect outputs.
license: MIT
compatibility: Requires Python 3 for the optional cache output audit script.
---

# Turborepo 2 Cache Debugging

Use this skill when diagnosing why Turborepo cache behavior is surprising.

## When to Use

Use this skill when the user mentions:

- Cache miss
- Cache hit
- Stale build
- Wrong output
- Remote cache
- `--dry`
- `--summarize`
- `inputs`
- `outputs`
- `env`
- `globalEnv`
- `.env`
- CI cache differences

## Workflow Reference

Use the workflow for structured investigation:

```text
workflows/turborepo-2-cache-debugging-workflow.md
```

## Resource Reference

Use the playbook:

```text
resources/turborepo-2-cache-debugging-playbook.md
```

## Example Reference

Use the report template:

```text
examples/turborepo-2-cache-miss-report-template.md
```

## Script Reference

Before using the cache output audit script:

```bash
python3 .agents/plugins/turborepo-2/skills/turborepo-2-cache-debugging/scripts/turborepo-2-cache-output-audit.py --help
```

Run from the repository root:

```bash
python3 .agents/plugins/turborepo-2/skills/turborepo-2-cache-debugging/scripts/turborepo-2-cache-output-audit.py --root .
```

## Investigation Strategy

1. Identify whether the issue is an unexpected miss or a suspicious hit.
2. Use `turbo run <task> --dry` to see the selected tasks without executing them.
3. Use summary output where appropriate to compare task hashes and inputs.
4. Check changed lockfiles, root `package.json`, `turbo.json`, package scripts, and workspace dependencies.
5. Check `inputs`, especially custom inputs without `$TURBO_DEFAULT$`.
6. Check environment variables in `env`, `globalEnv`, passthrough settings, and strict environment behavior.
7. Check whether `.env` files should be included in `inputs` for output-affecting values.
8. Check `outputs` for missing generated files or unsafe secret-containing files.
9. Check remote cache credentials and read/write permissions.
10. Avoid deleting caches until configuration has been reviewed.
