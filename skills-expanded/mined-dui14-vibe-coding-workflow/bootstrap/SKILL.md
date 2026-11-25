---
name: bootstrap
description: Initialize or redesign the project's AI context, architecture rules, and development structure.
---

# Bootstrap

Use this skill only when initializing a new project or redesigning its AI development context.

## Goal

Create a minimal, consistent project context that allows coding agents to work without loading unnecessary information.

## Mode

Choose **lite** or **full** from `idea.md` and repo size.

| Mode | When | Write |
|---|---|---|
| Lite | Small project: landing page, script, tool; no DB/auth; few screens | Exactly three files: `ai-context/01-product.md`, `ai-context/02-tech-stack.md`, `ai-context/06-coding-standards.md`. Fold role, one-page architecture, and UI tokens into those files. |
| Full | Multi-layer app | `ai-context/00-role.md` through `ai-context/08-mcp-tools.md` |

Do not write the other `ai-context/` numbers in lite mode.

## Procedure

1. Inspect the repository structure.
2. Inspect package manifests, lockfiles, build configuration, and existing documentation.
3. Identify the actual runtime, frameworks, databases, external services, and development tools. For Case 1 (empty repo), use `idea.md` only and state assumptions.
4. Identify architectural layers and their boundaries.
5. Create or update `ai-context/` using the chosen mode.
6. Create or update the root `AGENTS.md`. Preserve the model assignment and tooling-by-role sections.
7. Add local `AGENTS.md` files only where a directory has distinct rules or boundaries.
8. Keep project skills under `.agents/skills/<name>/`. Only create a skill folder this workflow already ships or the user asked to add. Do not invent extra skill names.
9. Write `spec/features/` with **runnable** acceptance criteria (commands). Write `spec/progress.md` with status `todo` and the acceptance command on each row. Write `spec/ui/` only in full mode when UI exists.
10. Remove duplicated, obsolete, or overly detailed rules from `AGENTS.md`.
11. Verify that documented architecture matches the actual codebase when code exists.
12. **Stop.** List files, flag assumptions, and wait for the user to accept the spec. Do not create `src/` or implement features in the same turn.

## Spec rules

- Each acceptance criterion is a shell or test command, not a sentence.
- `spec/progress.md` must not use status `done` at bootstrap time.
- Do not start the source tree until the user explicitly accepts the spec.

## Context

Use only the information required to define:

- Role and project purpose
- Product requirements
- Technology stack
- Architecture
- Database
- API contracts
- Coding standards
- UI system
- MCP/tools (4–5 servers; prefer CLI for tests and scanners)

## Rules

- Do not invent architecture or requirements.
- Prefer existing implementation over assumptions.
- Do not duplicate project knowledge between `AGENTS.md` and `ai-context/`.
- Keep `AGENTS.md` minimal.
- Do not modify application code unless required by the bootstrap task.
- Preserve working project behavior.
- Skills path is `.agents/skills/<name>/SKILL.md`. If a named skill is missing, give the install command instead of creating an empty folder.
