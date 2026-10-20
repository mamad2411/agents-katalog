---
name: plan-code-change
description: Plan a code change without editing files. Use for feature work, bug fixes, refactors, chores, cleanup, dependency/config updates, or implementation scoping before code changes.
---

# Plan Code Change

## Purpose

Create a source-grounded implementation plan without editing files.

## Supported Change Modes

### Feature
Use when adding new behavior.
Must identify:
- product intent
- affected user flow
- data/API/UI impact
- acceptance criteria
- tests
- docs

### Bugfix
Use when correcting broken behavior.
Must identify:
- expected behavior
- actual behavior
- suspected cause
- minimal fix area
- regression tests

### Refactor
Use when changing structure without intended behavior change.
Must identify:
- current pain
- behavior preservation rules
- safe refactor boundaries
- verification needed

### Chore
Use for cleanup, config, dependency, formatting, naming, maintenance, or non-behavioral work.
Must identify:
- why the chore matters
- files affected
- risk level
- verification needed

## Workflow

1. Read `AGENTS.md`.
2. Use `.ai/context-routing.md` if present.
3. Use the smallest relevant maps/indexes only for discovery.
4. Use `rg`, file search, Graphify, Aider repo maps, Understand Anything, or Repomix only as navigation aids.
5. Read exact source files, nearby tests, contracts, and docs before proposing implementation details.
6. Identify the change mode: feature, bugfix, refactor, or chore.
7. Identify affected roles: frontend, backend, database, DevOps, security, SQA, docs, architect, or planning.
8. Identify constraints: product, API, database, security, documentation, verification, migration, compatibility, or deployment.
9. Produce a focused implementation plan.

## Boundaries

- Do not edit files.
- Do not stage, commit, push, deploy, or run migrations.
- Do not treat generated maps, graphs, summaries, or indexes as implementation truth.
- Do not invent missing requirements.
- Escalate to the appropriate role when ownership is outside the current role.

## Required Output

- Change mode.
- Relevant files/docs inspected.
- Current behavior or current structure.
- Proposed target behavior or target structure.
- Step-by-step implementation plan.
- Tests/verification to run.
- Docs to update or reason docs are not needed.
- Risks, assumptions, and handoffs.
