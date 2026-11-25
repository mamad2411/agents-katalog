---
name: catch-me-up
description: Builds a fast, accurate mental model of an unfamiliar or recently changed codebase. Use when the user asks to get caught up, understand a new repository, comprehend architecture, trace a feature or behavior, learn local conventions, review recent commits from the last few days, prepare for a rebase, or understand code before planning, editing, reviewing, or debugging.
---

# Catch Me Up

## Operating Rule

Prioritize comprehension over edits. Do not modify files unless the user explicitly asks for implementation after the catch-up. Read the code, tests, docs, configuration, and git history needed to form a defensible mental model the user can verify and use to steer planning.

Do not read all workflow references up front. Start with the smallest workflow that answers the user:

1. Read `references/repo-comprehension.md` when the user is new to the repository or asks how the repo works broadly.
2. Read `references/task-specific-comprehension.md` when the user names a feature, bug, refactor, subsystem, PR, file, error, or behavior they need to change or review.
3. Read `references/recent-changes-catch-up.md` when the user asks what changed lately, says they came back after time away, needs to rebase, or wants to understand new code merged over the last few days.

If multiple workflows apply, read and run them in this order: Recent Changes Catch-Up, then Task-Specific Comprehension, then only the repo context needed to fill gaps.

## Quick Start

Example requests and reference choices:

- "Catch me up on this repo" -> read `references/repo-comprehension.md`.
- "I am a new contributor. Catch me up on how this repository works and clarify whether it simulates envelopes or intercepts real ones" -> read `references/repo-comprehension.md`, then `references/task-specific-comprehension.md` for the named behavior.
- "Catch me up on how login works before I change it" -> read `references/task-specific-comprehension.md`.
- "Catch me up on this PR before I review it" -> read `references/task-specific-comprehension.md`.
- "Catch me up on what changed since Friday before I rebase" -> read `references/recent-changes-catch-up.md`, then read `references/task-specific-comprehension.md` only if the user names a subsystem or task.

## Shared Exploration

Run a quick repository scan before choosing depth:

- Identify project type from package and build files such as `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Gemfile`, `pom.xml`, `Makefile`, `README`, and workspace config.
- Prefer `rg --files`, `rg`, `git log`, `git show`, `git diff`, and existing project scripts over slow or broad commands.
- Read local agent guidance such as `AGENTS.md`, `CLAUDE.md`, `.cursor/rules`, or equivalent before drawing conclusions.
- Prefer primary evidence from source files, tests, commit messages, and docs. Label guesses as guesses.
- Prefer a shallow map plus one useful deep path over a comprehensive survey with weak evidence.
- Stop scanning once the answer has enough evidence. Avoid dumping full directory trees.

## Workflow References

- `references/repo-comprehension.md`: broad orientation for a new repository.
- `references/task-specific-comprehension.md`: focused comprehension before planning, editing, debugging, or reviewing a concrete change.
- `references/recent-changes-catch-up.md`: git-history catch-up for recent merges, rebases, and stale context.

## Output Style

Be visual and compact. Prefer tables, short bullets, and Mermaid diagrams over long prose when they improve comprehension. Include file paths and symbols so the user can jump directly into the code. Separate facts from inferences. Answer the user's concrete question directly before broader context when they ask one.

End with one of these:

- "Ready to plan the change" when comprehension is sufficient for implementation.
- "Ready to review" when comprehension is sufficient for a PR review.
- "Need one clarification" when a single user decision blocks useful progress.
- "Need deeper investigation" when the codebase evidence is contradictory or incomplete.
