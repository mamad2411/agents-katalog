---
name: openspeq-init
description: Initialize or refresh an openspeq spec workspace inside a repository using the repo-native mission/plan/record workflow.
---

# openspeq-init

Use this skill when a repository needs to adopt `openspeq` conventions or refresh an existing setup.

## Goal

Create or align a repo-local spec workspace that any coding agent can use without vendor-specific packaging.

## Inputs

- repository root
- project purpose and constraints
- preferred stack/testing/deployment defaults

## Steps

1. Read `README.md`, `docs/workflow.md`, and `templates/mission-template.md` from this `openspeq` project.
2. Inspect the target repository for existing mission/spec/ADR files before adding anything.
3. If no workspace exists, create:
   - `specs/mission.md`
   - `specs/decision-log.md`
   - `specs/_plans/`
4. Generate `specs/mission.md` from `templates/mission-template.md` and fill in:
   - project purpose
   - users and capabilities
   - stack
   - testing strategy
   - operational constraints
5. Seed `specs/decision-log.md` from `templates/decision-log-template.md` or a minimal ADR header, and tell future agents to use `/adr` for durable architecture decisions.
6. Explain to the user how future work should flow through `mission -> plan -> implement -> record`.

## Constraints

- Keep durable docs agent-agnostic.
- Prefer plain Markdown over hidden automation.
- Do not invent runtime-specific slash commands or marketplace assumptions.
- Keep files small and concrete.

## Outputs

- repo-local `specs/` workspace
- mission and decision-log starter files
- short adoption summary
