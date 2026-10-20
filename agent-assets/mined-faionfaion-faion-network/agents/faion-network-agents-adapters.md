# Faion Platform Adapters

Faion keeps one skill and one workflow corpus, then maps platform-specific primitives through adapter files. Read exactly one adapter before applying `SKILL.md` routing rules:

| Platform | Read | Purpose |
|----------|------|---------|
| Claude Code | `claude-code.md` | Slash command invocation, `AskUserQuestion`, Claude Agent SDK retrieval, Claude session paths, Claude hooks. |
| Codex | `codex.md` | Skill auto-use, plain user questions, `spawn_agent`, Codex session assumptions, direct repository reads. |

Core Faion docs should use neutral phrases:

- `platform user-choice primitive` for structured user questions or approval gates.
- `platform subagent-dispatch primitive` for launching child agents.
- `platform quota-state source` for quota/concurrency checks.
- `platform wakeup primitive` for scheduled resume after quota or waiting.
- `platform cross-session memory store` for long-lived session memory.
- `platform worktree isolation path` for parallel write isolation.

Do not delete Claude Code metadata from `SKILL.md`; Claude still needs it. Codex should ignore fields it does not understand and follow `codex.md`.

## Gotcha

`workflows/adapters/` is a **second, workflow-scoped** pair of `claude-code.md` / `codex.md` — shorter files covering orchestration dispatch only, not the same bytes as these. The vocabulary above is shared by both; an edit to a primitive's name has to land in all four adapter files.
