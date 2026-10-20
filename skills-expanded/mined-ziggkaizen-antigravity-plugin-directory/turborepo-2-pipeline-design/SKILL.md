---
name: turborepo-2-pipeline-design
description: Designs Turborepo 2 build, test, lint, and typecheck task pipelines. Use when creating or refactoring standard quality tasks, affected checks, local quality gates, or CI-aligned task groups.
license: MIT
compatibility: Optional affected-check script requires bash, git, and a local turbo executable or package-manager script.
---

# Turborepo 2 Pipeline Design

Use this skill to design practical Turborepo 2 task pipelines for `build`, `test`, `lint`, and `typecheck`.

In this skill, “pipeline” means the developer workflow and task graph. It does not mean the deprecated Turborepo 1 `pipeline` configuration key.

## When to Use

Use this skill when the user asks to:

- Create a standard `build`, `test`, `lint`, and `typecheck` setup.
- Decide which tasks should depend on dependency-package tasks.
- Align local quality commands with CI.
- Add `--affected` checks.
- Split app, service, package, and root task responsibilities.
- Refactor over-broad or hidden task chains.

## Workflow Reference

Use the workflow when designing a task pipeline:

```text
workflows/turborepo-2-pipeline-design-workflow.md
```

## Resource Reference

Use the task matrix:

```text
resources/turborepo-2-standard-task-matrix.md
```

## Example Reference

Use this example as a starting point:

```text
examples/turborepo-2-build-test-lint-typecheck-design.md
```

## Script Reference

Before using the affected-check script:

```bash
.agents/plugins/turborepo-2/skills/turborepo-2-pipeline-design/scripts/turborepo-2-affected-check.sh --help
```

Default usage performs a dry-run affected task check:

```bash
.agents/plugins/turborepo-2/skills/turborepo-2-pipeline-design/scripts/turborepo-2-affected-check.sh .
```

## Design Principles

- Design task names as stable contracts.
- Keep tasks narrow enough to explain and broad enough to be useful.
- Prefer one local quality gate that approximates CI.
- Avoid making `build` do unrelated lint, test, deploy, or publish work.
- Avoid making package tasks reach across app/service/domain boundaries without visible dependencies.
- Use `dependsOn` instead of shelling out to other package scripts manually.
- Make affected-package checks a performance optimization, not the only correctness gate.
