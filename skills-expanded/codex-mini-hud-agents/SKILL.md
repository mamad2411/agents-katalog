# Codex Mini HUD project guidance

## Goal

Build a fast, local-first HUD for Codex CLI that exposes useful session state
without distracting from the coding workflow.

## Product principles

- Prefer documented, native Codex capabilities over parsing internal files.
- Degrade gracefully when a capability is unavailable.
- Never delay or break a Codex session.
- Keep user data local and never collect prompt or transcript content.
- Target macOS first.
- Avoid background daemons and terminal wrappers unless clearly justified.
- Treat installation and uninstallation as safety-critical.

## Workflow

- Clearly distinguish documented APIs from heuristics or internal formats.
- Write tests for malformed, missing, duplicate, and user-modified config.
- Run `./test.sh` after relevant changes.
- Preserve unrelated user changes.
- Do not modify `~/.codex` without explicit approval.

## Delegation

Use subagents for independent read-only research, test-gap analysis, and final
review. The main agent owns architecture decisions and code edits.
