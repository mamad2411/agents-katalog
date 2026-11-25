---
name: scientific-runtime
description: Use when serving scientific CLI tasks through ScholarAIO, especially when the agent should prefer scholaraio toolref, handle partial coverage safely, or avoid turning user work into documentation maintenance.
---

# Scientific Runtime Protocol

This is a shared runtime skill for scientific CLI work.

It is not a tool manual.
It tells the agent how to behave when serving real users on scientific tool tasks.

Use it alongside a tool-specific scientific skill such as:

- `quantum-espresso`
- `lammps`
- `gromacs`
- `openfoam`
- `bioinformatics`

## Core Principle

ScholarAIO is for users, not for people who want to co-maintain the internal documentation layer.

So the agent should absorb complexity whenever possible.

The user should experience:

- natural language help
- reliable parameter lookup
- graceful fallback when coverage is partial

The user should not experience:

- being asked to manually patch `toolref`
- being forced to learn internal parser gaps
- being blocked because a documentation layer is imperfect

## Runtime Protocol

For any scientific CLI task:

1. Identify the scientific tool or sub-tool that matches the problem.
2. Use the tool-specific skill for workflow and scientific norms.
3. Use `toolref` first for commands, parameters, program pages, and option meanings.
4. If `toolref` is sufficient, continue normally.
5. If `toolref` is partial, fall back to official docs and continue the task.
6. Mention the coverage gap briefly only when it affects confidence or maintainability.
7. Do not turn the current user task into documentation maintenance work.

## Toolref-First Behavior

The agent should prefer:

- `scholaraio toolref show <tool> ...` for precise lookups
- `scholaraio toolref search <tool> "..."` for natural-language entry

The stable public surfaces are:

- the `scholaraio toolref ...` CLI
- the top-level `scholaraio.stores.toolref` package facade

The agent should not route users through internal implementation modules such as:

- `scholaraio.stores.toolref.fetch`
- `scholaraio.stores.toolref.manifest`
- `scholaraio.stores.toolref.storage`
- `scholaraio.stores.toolref.search`

Those internal module boundaries may change during refactors. User-facing guidance should stay anchored to the CLI and the top-level package behavior.

Before writing configuration or scripts, first resolve:

- which program or subcommand is relevant
- which parameters are high-risk
- which defaults or restrictions matter for validity

## When Toolref Is Incomplete

If `toolref` does not fully answer the question:

- continue using the official documentation source
- clearly separate "task progress" from "maintenance opportunity"
- do not ask the user to stop and repair the docs layer first
- do not expose internal refactor details unless they materially affect current behavior

Use this pattern:

- "I used `toolref` for the main entry point."
- "For this deeper detail, I fell back to the official docs because current coverage is partial."

## Escalation Rule

Escalate a gap to onboarding or maintenance only when:

- the same gap appears repeatedly
- it blocks a common task
- it affects correctness, not just convenience

If it is a one-off edge case, do not derail the user task.

## Separation Of Responsibilities

- tool-specific skill: when to use the tool, workflow, scientific norms
- `toolref`: interface and parameter reference
- scientific runtime: how to behave under uncertainty or partial coverage

When code changes are involved:

- preserve the public `scholaraio.stores.toolref` entry surface
- treat package-internal reorganizations as an implementation detail
- if a refactor changes behavior visible through CLI or top-level imports, treat that as a regression until proven otherwise

## Anti-Patterns

Do not:

- dump raw flags from memory
- tell the user to "go improve toolref first"
- confuse a successful CLI run with a valid scientific result
- replace scientific judgment with parameter lookup alone
- instruct the user to use internal module names as if they were the supported interface

## Output Style

When answering the user:

- keep maintenance details short
- foreground scientific progress and decision-making
- mention fallback only when it materially changes confidence or provenance
