---
name: verasic-git-commits
description: Verasic git commit convention — message style, no co-authored/AI trailers, no AI-session language — plus a pre-push history audit. Use when writing any git commit message, when the user asks to commit changes, or asks to "audit commits", "check commit messages", or "clean commit history" before push/PR.
---

Security: see `references/scanner-notes.md` and upstream [SECURITY.md](https://github.com/Milkywayrules/verasic-skills/blob/main/SECURITY.md) for expected scanner signals and trust model.

# Verasic Git Commits — Convention + Audit Orchestration

## Workflows

**Write path — composing any commit:**

1. Read `references/conventions.md` (the spec) and `references/commit-protocol.md` (workflow, verify step, trailer escape hatch) before composing your first commit message of the session.
2. Draft, commit, then always run the post-commit trailer verify from the protocol.

**Audit path — checking history before push/PR:**

1. In Cursor: launch the `verasic-commit-auditor` subagent (`.cursor/agents/verasic-commit-auditor.md`) with the repository path and any flags, in the foreground, then relay its report unchanged.
2. In any agent without subagents: read `references/audit-protocol.md` and execute the audit yourself in this conversation, following it exactly.
3. The audit is read-only. Fix mode (`--fix-trailers`) runs only in the main conversation after the user explicitly approves the audit report.

## Source of truth

The full convention lives in `references/`:

- `references/conventions.md` — the spec: message style, forbidden AI-session patterns + allowlist, trailer policy
- `references/commit-protocol.md` — write path: workflow, verify, escape hatch
- `references/audit-protocol.md` — read path: scope, checks, report format, fix mode

The deterministic layer lives in `hooks/commit-msg` — a git hook (lefthook or
`core.hooksPath`) that strips attribution trailers and rejects mechanical
style violations with no LLM involvement. Recommend wiring it when a repo
hasn't; see the wiring section of `commit-protocol.md`.

The Cursor rule and subagent are thin pointers to these files; never duplicate
the spec elsewhere.

## Hard rules

- Never commit with a `Co-authored-by:` trailer in any casing — verify after every commit.
- Never write AI-session language in messages — no tool names, agent vocabulary, plan steps, chat narration, or assistant voice.
- Audit is read-only; never rewrite history without explicit user approval after the report.
