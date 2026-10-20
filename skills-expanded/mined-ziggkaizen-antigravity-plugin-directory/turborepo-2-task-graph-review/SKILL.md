---
name: turborepo-2-task-graph-review
description: Reviews Turborepo 2 task graphs, caching, inputs, outputs, package configurations, root tasks, and turbo.json correctness. Use when editing or auditing turbo.json, turbo.jsonc, or package scripts run by turbo.
license: MIT
compatibility: Requires Python 3 for the optional validation script.
---

# Turborepo 2 Task Graph Review

Use this skill to design or review Turborepo 2 task configuration.

## When to Use

Use this skill when the user asks to:

- Review `turbo.json` or `turbo.jsonc`.
- Diagnose cache misses or stale outputs.
- Add, remove, or rename tasks.
- Configure `dependsOn`, `outputs`, `inputs`, `env`, `globalEnv`, or `passThroughEnv`.
- Add package-level `turbo.json`.
- Replace deprecated command patterns with task graph configuration.
- Review root tasks using `//#task`.

## Workflow Reference

Use the workflow for repeatable review:

```text
workflows/turborepo-2-task-graph-review-workflow.md
```

## Resource Reference

Use the task graph checklist:

```text
resources/turborepo-2-task-graph-review.md
```

## Script Reference

Before using the script:

```bash
python3 .agents/plugins/turborepo-2/skills/turborepo-2-task-graph-review/scripts/turborepo-2-validate-turbo-json.py --help
```

Run from the repository root:

```bash
python3 .agents/plugins/turborepo-2/skills/turborepo-2-task-graph-review/scripts/turborepo-2-validate-turbo-json.py --root .
```

## Review Method

1. Identify all root and package-level `turbo.json` files.
2. Confirm root config uses `tasks`.
3. Reject Turborepo 1 `pipeline`.
4. Confirm every task has a reason to exist.
5. Check whether each task is cacheable.
6. For cacheable tasks, verify `outputs`.
7. For non-cacheable tasks, verify `cache: false`.
8. For long-running tasks, verify `persistent: true` when appropriate.
9. Verify `dependsOn` reflects the package graph and task order.
10. Verify `inputs` do not accidentally opt out of defaults unless intentional.
11. Verify environment variables affecting outputs are represented in hashes.
12. Prefer package configurations for package-specific overrides.
13. Avoid framework-specific outputs unless the framework is actually present.

## Common Findings

### Missing `outputs`

A task like `build` without `outputs` can run but will not cache generated outputs as expected. Add outputs based on the actual build tool.

### Overbroad `globalEnv`

Use `globalEnv` only when a variable affects all tasks. Prefer task-level `env` for variables that affect only one task.

### Custom `inputs` Without Defaults

A task with `inputs` replaces default input behavior. Include `$TURBO_DEFAULT$` unless the replacement is intentional.

### Deprecated `--parallel`

Do not use `--parallel` to make tasks run together. Model the graph with `dependsOn`, `persistent`, and package configuration.

### Package-Level Override Pitfalls

Package-level arrays replace inherited arrays unless `$TURBO_EXTENDS$` is used. Be explicit when extending outputs, env, inputs, dependsOn, passThroughEnv, or with.
