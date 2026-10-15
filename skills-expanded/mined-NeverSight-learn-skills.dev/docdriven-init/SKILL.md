---
name: docdriven-init
description: Use once in a repository to initialize Documentation Driven Development. Scans the project shape, detects stack and commands, and generates a repo-local project-docdriven skill that tells agents how to use the project-specific Docs tree.
---

# DocDriven Init

Use this skill to make a repository DocDriven-aware.

## Required Workflow

1. Inspect repository files and existing docs.
2. Run a Project Dynamics Scan.
3. Decide the docs root, defaulting to `Docs/`.
4. Generate `.agents/skills/project-docdriven/SKILL.md`.
5. Do not create the full docs tree; that belongs to `docdriven-build`.
6. Report what was detected, what is uncertain, and where the local skill was written.

## Project Dynamics Scan

Detect:

- package usage: package manager, workspaces, scripts, dependencies
- code shape: source dirs, app dirs, package dirs, tests
- runtime dynamics: config, env, CI, deployment, database or schema tools
- architecture dynamics: structural ownership, code organization, contract locations, configuration flow, dependency direction, reuse/composition rules, and durable coding patterns
- validation reality: actual test, build, lint, typecheck, and dev commands
- documentation fit: human questions, durable knowledge areas, route shards, ownership, and validation evidence the project actually needs

## Documentation Fit

The local skill should describe the project-specific docs model, not repeat a
generic tree. Decide from evidence:

- what humans need to set up, run, configure, deploy, or change the project
- which concepts need canonical knowledge docs
- which interfaces, domains, packages, or operations deserve their own routes
- which areas are absent and should not get docs yet
- which likely docs are uncertain and should be recorded as gaps
- which architecture and coding-style conventions should be followed instead of generic agent preferences
- where reusable components, helpers, hooks, adapters, and project primitives live, and when feature-local code should be promoted

Do not make the local skill encode a generic architecture. It should tell future
agents to follow this project's documented structure, executable style config,
nearby code, and route graph. If a long-term convention is not known, record the
gap.

## Generator

Prefer running `scripts/create-project-skill.mjs` instead of hand-writing the local skill.

## References

- Read `../_shared/repo-local-skill-template.md`.
- Read `../_shared/agent-operating-contract.md`.
