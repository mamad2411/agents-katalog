---
name: docdriven
description: Use when working in a Documentation Driven Development project or when creating, changing, or maintaining docs-driven architecture, implementation, or project documentation. Enforces read-before-change, update-after-change, one canonical explanation per concept, and separate human, agent, knowledge, and tmp documentation surfaces.
---

# DocDriven

DocDriven is Documentation Driven Development for agents and humans.

## Required Workflow

1. Check whether the project has a repo-local DocDriven skill.
2. If it exists, read it before continuing.
3. Read `Docs/agent/manifest.json` when present.
4. Load only the smallest relevant route shard.
5. Read the route's `readFirst` docs.
6. Inspect the route's `codeAreas`.
7. Change code and docs together.
8. Update route shards when ownership, validation, or structure changes.
9. Record unknowns in `Docs/agent/gaps.md`.
10. Run validation from the route or `Docs/agent/validation.md`.

## Core Rules

- Code and checks prove truth.
- `Docs/knowledge/` explains current truth.
- `Docs/human/` summarizes for people.
- `Docs/agent/` routes agents.
- `Docs/tmp/` is temporary and not truth.
- The Docs structure is evidence-based, not pre-given.
- Add, omit, split, or consolidate docs when the project shape requires it.
- Do not duplicate canonical content.
- Link instead of copying.
- Follow the project's documented architecture and coding style; do not hardcode generic agent preferences.
- Prefer long-term project consistency over local convenience.
- Think before applying the scaffold: identify the project type, size, maturity,
  expected direction, and risk profile, then adapt the docs model to that
  reality.

## Dynamic Structure

The default DocDriven tree is a starting scaffold. Choose the final human docs,
knowledge docs, and route shards from repository evidence and reader needs.

- Add a human doc only when a person has a distinct task or question.
- Add a knowledge doc only when durable current truth needs a canonical home.
- Split route shards only when it reduces context load or clarifies ownership.
- Do not create docs for absent concepts just because a template names them.
- Record uncertain documentation needs in `Docs/agent/gaps.md` instead of inventing structure.
- Large projects need stronger routing, clearer ownership, narrower shards, and
  better validation evidence than small projects. Scale the documentation system
  to the project instead of treating every repository the same.

## Project Continuity

DocDriven is for long-lived projects. Agents must not introduce favorite
folders, architecture styles, config patterns, testing patterns, or coding
style preferences just because they are common elsewhere.

Use project evidence in this order:

1. executable truth such as formatter, linter, type, schema, config, and test files
2. `Docs/agent/` routes and validation protocol
3. `Docs/knowledge/architecture/` and related canonical knowledge docs
4. nearby code when docs do not yet explain the convention

If a durable convention is missing, choose the smallest locally consistent
change and record the gap. If a change creates a new convention, update the
architecture docs and routes in the same task.

Before creating new components, helpers, hooks, adapters, contracts, config
helpers, or test helpers, look for existing reusable project primitives and
documented composition patterns. Keep feature-local code local until reuse is
real. Promote reusable code only when repeated use, stable responsibility, or
project architecture justifies it.

Docs must not copy type, schema, or interface definitions from code. They should
explain where authoritative code contracts live, which module owns them, how
consumers should access them, and when changes require docs or route updates.

## Meaningful Changes

Update docs for behavior, public interface, config, environment, deployment,
dependency, package-script, schema, migration, architecture, ownership, and
validation changes.

After any large LLM task, multi-step implementation, refactor, migration, or
architectural change, update the relevant DocDriven docs before claiming the
work complete. Big changes that leave the docs stale are unfinished changes.

## Stale Or Missing Docs

- If docs contradict code, inspect code and update docs.
- If truth cannot be verified, record uncertainty in `Docs/agent/gaps.md`.
- If no route matches, update the route graph or record the gap.
- Missing documentation is part of the task.

## Completion Evidence

When finishing DocDriven work, report:

- Docs read
- Routes used
- Code changed
- Docs updated
- Validation run
- Gaps recorded

## References

- Read `../_shared/docdriven-structure.md` for the default documentation model.
- Read `../_shared/agent-operating-contract.md` for route-table requirements.
- Read `../_shared/writing-style.md` before writing or editing docs.
