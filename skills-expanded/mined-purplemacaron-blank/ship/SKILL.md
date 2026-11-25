---
name: Ship
description: Prepare a change for a clean commit, PR, and release. Use when implementation is done and the user wants to ship.
---

# Ship

Shipping is a sequence of checks, not a single push.

## Before the commit

1. Run the repository's verification commands: tests, typecheck, lint, build. Find them in `package.json`, `Makefile`, CI config, or `AGENTS.md`.
2. Review the complete diff (`git status`, `git diff`). Separate intended changes from accidental ones (debug logs, lockfile churn, generated files).
3. Check for secrets, tokens, local paths, and large binaries.
4. Confirm the change is coherent: one purpose per commit.

## Commit

- Inspect recent history for message style, then write a message that explains *why*.
- Never amend or rewrite history unless asked.
- Do not commit `.env`, credentials, or unrelated work.
- Stage specific files rather than `git add -A` when the tree is dirty.

## PR

Include:

- **What** changed in 1–2 sentences.
- **Why** it is needed.
- **How it was verified** — exact test/build commands and results.
- Risks and rollback notes.
- Screenshots for UI changes when useful.

Keep the title under ~70 characters. Link the issue if one exists.

## Release

- Update the changelog and version if the project does.
- Verify the artifact builds from a clean install when possible.
- State clearly what was published. Do not claim a deploy or publish that was not performed.

## Guardrails

- Never push, publish, or deploy without explicit permission.
- Never skip hooks or signing unless the user asks.
- Report failed checks honestly; a failing test is not "probably unrelated" without evidence.
