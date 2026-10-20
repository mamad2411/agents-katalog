---
name: project-context
description: Inspect and summarize project context before coding. Use when Codex needs to modify a repository, understand structure, follow existing conventions, locate scripts, read AGENTS.md, README, package manifests, or project documentation.
---

# Project Context

## Workflow

1. Inspect the current directory and identify the project root.
2. Read local guidance first: `AGENTS.md`, `.ai_project.md`, README, and relevant docs.
3. Inspect dependency and script files: `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `pom.xml`, `requirements.txt`, or equivalents.
4. Search existing code for nearby patterns before introducing new ones.
5. Identify test, lint, typecheck, and build commands before editing.

## Rules

- Prefer existing abstractions, naming, file layout, and test style.
- Do not block small fixes just because `.ai_project.md` is absent.
- For multi-step project work, suggest creating or updating `.ai_project.md`.
- Avoid broad repository scans after enough context is available.

## Output

Report only context that affects the current decision: stack, entry points, scripts, constraints, and notable risks.
