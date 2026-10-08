---
name: agent-session-hooks
description: Explains how startup scripts run at the start of agent sessions and inject context. Use when an agent session reports a failing hook (e.g. validate-session-branch-name.sh, validate-session-worktree-name.sh, validate-session-commit-signing.sh, validate-session-gh-authentication.sh, validate-session-skills.sh), or when adding a new startup check.
---
# Agent Session Hooks

Startup checks run at the start of every agent session and inject their failure as additional context. **Fix what they report before writing any code** — each one names the problem and the command that repairs it.

## When to Use This Skill

- When an agent session fails at startup due to a hook.
- When you need to understand how the session gets context about branches, worktrees, git signing, GitHub authentication, or missing skills.
- When you need to add a new check that should run for every agent session.

## Architecture

| Script                                  | Checks                                                                                                |
| --------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| `validate-session-branch-name.sh`       | Branch follows `<type>/<scope>-<description>`; directs the agent to the rename-branch skill           |
| `validate-session-worktree-name.sh`     | Worktree directory follows lowercase kebab-case naming and ignore conventions                         |
| `validate-session-commit-signing.sh`    | `commit.gpgsign`, `user.signingkey`, and a GPG signing smoke test                                     |
| `validate-session-gh-authentication.sh` | The active `gh` account plus Projects access                                                          |
| `validate-session-skills.sh`            | Every skill declared in `skills-lock.json` is present; directs the agent to `codebase:install-skills` |

Each script is registered twice, once per harness, and both registrations point at the same file:

| Harness        | Registration                                      |
| -------------- | ------------------------------------------------- |
| Claude Code    | `SessionStart` entries in `.claude/settings.json` |
| GitHub Copilot | `sessionStart` entries in `.github/hooks/*.json`  |

## Adding a New Check

When adding a check: put the script under `scripts/git/`, emit through `scripts/git/emit-session-hook-context.sh` so both harnesses can read it, and register it in both places.

Why the credential checks resolve the session's own token and signing configuration rather than the hook shell's, and why a hook can fail but never hang, is in [ADR 0010](../../docs/adr/0010-judge-the-credentials-a-session-really-uses.md).
