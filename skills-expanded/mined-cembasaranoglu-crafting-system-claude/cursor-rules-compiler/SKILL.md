---
name: cursor-rules-compiler
description: Generate or review AGENTS.md and `.cursor/rules/*.mdc` for a repository
  using source evidence, scoped rules, plan-mode guidance, and safety guardrails.
---

# Cursor Rules Compiler

Use when creating Cursor project rules, AGENTS.md, or AI-ready repository context.

Follow `prompts/161_cursor_advanced_rules_prompt.md`.

Rules:

- Inspect the repository first.
- Keep always-on rules short.
- Use globs for file-specific conventions.
- Put long context in `docs/ai/*` and reference it.
- Add secret, Git, validation, and execution guardrails.
- Avoid duplicate AGENTS.md and Cursor rule content unless deliberately needed.
