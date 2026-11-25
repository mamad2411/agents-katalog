---
name: dev-flow-git
description: Use when dev-flow must choose or apply Git isolation, commits, PRs, patch-ready output, conflict handling, rollback, branch cleanup, or side-effect permissions.
---

# dev-flow-git

Own Git isolation, integration mode, side-effect permissions, rollback, conflict handling, and cleanup. Execution may reference Git mode but must not invent Git permissions.

## Boundary

This skill owns Git isolation mode selection, branch/worktree lifecycle, integration state transitions, rollback, and safety gate enforcement. Does NOT execute code changes — only manages Git state.

## Core Contract

- For Loop work, resolve Phase parallelism, max_parallel_phases, Phase worktrees, local branch/commit permission, Loop integration branch, final delivery, fallback, and cleanup once at the Loop Start Gate. The Phase Planning Gate only verifies the inherited policy and actual Phase scope.
- When the Loop Start Gate approves parallel Phase execution, default to one worktree per selected Phase. When it does not, use one serial Phase writer. Never create one worktree per OpenSpec task.
- Integrate accepted Phase branches into the named Loop integration branch with one integration writer, in stable Phase-ID order, before dependent phases start.
- Default to patch-ready mode when commits, pushes, PRs, merges, or destructive actions are not explicitly authorized or supported.
- Use exact canonical integration state names in persisted artifacts.
- Preserve unrelated user changes and avoid staging/committing them unless explicitly authorized.
- Classify artifacts by role, not extension: keep canonical dev-flow, Loop, OpenSpec/opsx, code, config, and test artifacts eligible for tracking; isolate transient verification output under `.dev-flow/runtime/<run-id>/` and stage only through an explicit staging allowlist.

## References

- Read `references/modes-and-states.md` before selecting isolation mode, integration mode, writer concurrency, or canonical task integration states.
- Read `references/operations-and-safety.md` before creating worktrees/branches, staging, committing, pushing, opening PRs, merging, applying shared patches, handling conflicts, rolling back, or cleaning up.

## Language Policy

All user-facing replies and all generated artifact documents (requirements, design, specs, CLI specs, test plans, delivery reports, and other persisted Markdown files) in dev-flow must be written in Chinese.

## Required Signal

Emit `git_safe` with Phase isolation mode, Phase branch/worktree, Loop integration branch/base revision when applicable, one-writer task and integration limits, final-delivery mode, allowed and forbidden effects, capability/permission result, rollback/cleanup constraints, blockers, and allowed canonical integration states.

Full YAML schema for `git_safe` is defined in `dev-flow-master/references/state-and-gates.md` § Signal Schemas. The field list here is the authoritative prose summary; the YAML block in state-and-gates.md is the authoritative machine-readable definition.
