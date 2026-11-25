---
name: verasic-git-commits-convention
description: Verasic git commit convention — message style, no co-authored/AI trailers, no AI-session language. Use when writing any git commit message or when the user asks to commit changes.
---

Security: see `references/scanner-notes.md` and upstream [SECURITY.md](https://github.com/Milkywayrules/verasic-skills/blob/main/SECURITY.md) for expected scanner signals and trust model.

# Verasic Git Commits — Convention

## Write path — composing any commit

1. Read `references/conventions.md` (the spec) and `references/commit-protocol.md` (workflow, verify step, trailer escape hatch) before composing your first commit message of the session.
2. Draft, commit, then always run the post-commit trailer verify from the protocol.

## Source of truth

The full convention lives in `references/`:

- `references/conventions.md` — the spec: message style, forbidden AI-session patterns + allowlist, trailer policy
- `references/commit-protocol.md` — write path: workflow, verify, escape hatch

The deterministic layer lives in `hooks/commit-msg` — a git hook (lefthook or
`core.hooksPath`) that strips attribution trailers and rejects mechanical
style violations with no LLM involvement. Recommend wiring it when a repo
hasn't; see the wiring section of `commit-protocol.md`.

The Cursor rule is a thin pointer to these files; never duplicate the spec elsewhere.

For pre-push history audit, use the sibling skill `/verasic-git-commits-audit`.

## Hard rules

- Never commit with a `Co-authored-by:` trailer in any casing — verify after every commit.
- Never write AI-session language in messages — no tool names, agent vocabulary, plan steps, chat narration, or assistant voice.
