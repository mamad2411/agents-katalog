---
name: cosmosmith-project-rules
description: Generate or update project instruction files for Cosmosmith-governed projects. Use when the user wants AGENTS.md, CLAUDE.md, Cursor rules, Copilot instructions, OpenCode, Trae, or other editor/agent rules created from Cosmosmith conventions, or when they ask how agents should load and follow project rules.
---

# Cosmosmith Project Rules

## Purpose

Install Cosmosmith project rules into the user's repository without forcing every editor to use the same file.

## Workflow

1. Ask which rule surfaces the user wants only if it is not clear. Default to `AGENTS.md` only.
2. If `AGENTS.md` is requested, create or update it from the Cosmosmith generated-project template.
3. If `CLAUDE.md` is requested, create a small adapter that points to `AGENTS.md` as canonical.
4. If Cursor is requested, create `.cursor/rules/cosmosmith.mdc` as an adapter to `AGENTS.md`.
5. If GitHub Copilot is requested, create `.github/copilot-instructions.md` as an adapter to `AGENTS.md`.
6. If OpenCode is requested, create `.opencode/AGENTS.md` as an adapter to `AGENTS.md`.
7. If Trae is requested, create `.trae/rules/cosmosmith.md` as an adapter to `AGENTS.md`.
8. Keep adapters short and do not duplicate the whole constitution unless the tool requires it.
9. Update `task.md` with any follow-up tasks.

## Rules

- `AGENTS.md` is canonical for cross-agent project behavior.
- Tool-specific files are adapters.
- Supported adapters include `CLAUDE.md`, `.cursor/rules/cosmosmith.mdc`, `.github/copilot-instructions.md`, `.opencode/AGENTS.md`, and `.trae/rules/cosmosmith.md`.
- If an adapter conflicts with `AGENTS.md`, follow `AGENTS.md` and update the adapter.
- Do not overwrite substantial existing project rules without preserving user-specific guidance.

## Completion

Stop when requested rule files exist, identify their canonical source, and record any follow-up tasks.
