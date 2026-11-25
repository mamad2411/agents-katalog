---
name: hermes-codex-plugin
description: Use when a task may depend on prior user preferences, project conventions, architectural rules, workflow decisions, previous Codex work, full-text memory search, durable rule saving, or skill drafting/updating through Hermes Codex Plugin, especially to reduce Codex token spend by recalling minimal relevant context.
---

# Hermes Codex Plugin

Use the bundled MCP tools to inspect and manage local memory. Treat memory as a standing source of
user preferences, project conventions, architectural rules, workflow decisions, similar solved
tasks, and existing reusable skills. Before solving a task, prefer checking whether memory or a
skill already contains the relevant rule or workflow, not only when the user explicitly says to
search memory. The main benefit is keeping Codex token usage low by retrieving only the relevant
memory needed for the current request.

## Workflow

1. Search first with `hermes_codex_search_chats` when prior context from earlier chats may matter.
2. Use `hermes_codex_search` for narrower local memory search when a project directory filter is useful.
3. Apply durable rules from memory as constraints while editing code, including style and import-placement rules.
4. Save durable facts with `hermes_codex_remember`.
5. After substantial tasks, write a concise structured task summary and save it with `hermes_codex_remember_summary`.
6. Use Codex's semantic judgment across languages to decide whether repeated workflow rules should become a skill draft; do not rely only on English keywords.
7. Use `hermes_codex_propose_skill` to draft a skill from repeated rules.
8. Only write a skill with `hermes_codex_write_skill` when the user clearly wants it.

## Rules

- Keep memories compact and actionable.
- Prefer structured summaries over raw chat transcripts for long-term task memory.
- Do not save secrets, credentials, raw logs, or huge code blocks.
- Treat skill drafts as proposals that need review before use.
- Prefer project-scoped memories for repository conventions and user-scoped memories for stable personal preferences.
