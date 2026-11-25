---
name: migrate-claude
description: Inspect a Claude Code game project and plan a reversible Codex migration of guidance, skills, agents, hooks, and paths. Use when CLAUDE.md or .claude content is present; preserve the source and require digest confirmation before writing Codex files.
---

# Migrate a Claude project

1. Inspect `CLAUDE.md`, `.claude/`, existing `AGENTS.md`, `.codex/`, engine markers, and uncommitted work. Do not modify them.
2. Run the core `migrate claude --project <root> --output <plan.json>` command.
3. Review every proposed destination. Claude slash commands become namespaced `$ai-game-studio:<skill>` references; engine/project guidance becomes root or scoped `AGENTS.md`; supported agent definitions belong under `.codex/agents/`.
4. Block unsupported Claude-only model names, tool declarations, memory fields, fixed turn limits, or paths from entering runtime files. Keep the original Claude files unchanged for comparison and rollback.
5. Present exact actions, detected environment, backups, license notes, permissions, expiry, rollback operations, and digest. Wait for verbatim digest confirmation.
6. Apply through `pack apply --project <root> --plan <plan.json> --confirmed-digest <digest>`.
7. Run `validate skills`, `validate platform`, project tests, and a representative Codex task. Report the transaction ID and how to generate a rollback plan.

If destinations already contain user-authored guidance, stop at the proposal and show the overlap. Never silently merge policy text whose precedence is unclear.
