---
name: itsol-repo-memory
description: "Read or maintain .itsol.md policy, project map, stable constraints, and verification."
---

# ITSOL Repo Memory

Use `itsol-workflow-mode` as the canonical contract for workflow defaults, allowed modes, restrictions, state, and precedence.

Use `.itsol.md` as repo-level operational memory for stable facts that should guide every agent working in the repository. Also use this skill when initializing `.itsol.md` for an existing repo or monorepo.

## Process

1. At the start of ITSOL work, check whether `.itsol.md` exists at the repository root.
2. If it exists, read it before choosing implementation, testing, verification, deployment, or review strategy.
3. For monorepos, use the root `Monorepo Map` and the most specific `Project: <path>` section matching the touched files.
4. If multiple projects are touched, apply each project's policy separately and state the selected policies in the plan or handoff.
5. If no matching project policy exists, inspect local configs before assuming root commands, test support, or deployment behavior.
6. Treat `.itsol.md` as stable team memory, not task scratchpad. Do not add temporary notes.
7. Propose updates when you discover stable repo-level facts, especially maintained test support, verification commands, generated-code rules, deployment constraints, legacy limits, and stable QA capability (`off`, `evidence`, `automatic`, or `strict`) including application types, runnable commands, targets, and cycle limits. Legacy TDD mode fields are capability hints, not automatic test-first requirements.
8. Resolve modes exactly through `itsol-workflow-mode`: intersect root and most-specific project `allowed_modes`, then every matching path/operation restriction. A task-level selection overrides a repo default but never an explicit restriction. Report conflicts and ask from the remaining allowed modes; never silently downgrade.

## Init Mode

Creating or improving only `.itsol.md` is a bounded repository-policy administration workflow, not feature implementation. Do not create Business/Technical Plans, initiative state, delegated code review, application QA, or a completion gate solely for repo-memory initialization. Use lightweight inspection, user confirmation, extension/YAML validation, and one focused inline self-review of the resulting policy; then report and stop. Do not route the whole working tree through implementation review, and do not include unrelated modified/untracked files.

When asked to create or initialize `.itsol.md`:

1. Inspect the repo structure and detect candidate projects/apps/packages/services.
2. Inspect only lightweight config files needed to infer stack and existing commands, such as workspace manifests, package files, solution files, project files, build configs, Docker/Nomad files, and test configs.
3. Present a candidate Monorepo Map to the user.
4. Ask the user to confirm or correct each project and its supported verification methods. Do not require a TDD mode decision or infer TDD from detected tests.
5. Ask for supported verification commands, QA profile/application types/targets, and known "do not spend time on" constraints per project. Use `qa.profile: off` for genuinely hard-to-run projects only when the user confirms the stable skip policy.
6. Write `.itsol.md` only after the user confirms the project map and policies.
7. Mark uncertain facts as `unknown`; do not invent policies from config detection alone.

## Execution Policy

After resolving `itsol-workflow-mode`, load `itsol-execution-policy` whenever resource, stop, or completion state matters; it owns the full execution state and evidence validation. Never use `maxTurns` or termination as completion; preserve `partial`, `blocked`, and `failed` outcomes.

## Focused References

- [01-usage-priority-and-updates.md](./references/01-usage-priority-and-updates.md) - Usage Priority And Updates
- [02-init-workflow.md](./references/02-init-workflow.md) - Init Workflow
- [03-file-format-monorepo-and-tdd.md](./references/03-file-format-monorepo-and-tdd.md) - File Format, Monorepo, Verification, And Legacy TDD Metadata
