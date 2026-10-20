---
name: github-issue
description: Use when the user needs GitHub issue and milestone-backed tracker operations through the packaged launcher and local CLI runtime.
argument-hint: [request]
allowed-tools: Bash
metadata:
  author: Orbit contributors
  version: "0.1.0"
---

# GitHub Issue Skill

Use this skill to operate GitHub Issues and milestone-backed planning data through the packaged launcher and local CLI runtime.

Within Orbit's shared provider framework, this skill is one implementation of the `tracker` capability.

## Runtime and execution

Always run the packaged launcher through `${GITHUB_ISSUE_SKILL_DIR}` so it works from the user's current working directory:

- macOS/Linux: `${GITHUB_ISSUE_SKILL_DIR}/bin/github-issue`
- Windows: `${GITHUB_ISSUE_SKILL_DIR}\bin\github-issue.cmd`

`${GITHUB_ISSUE_SKILL_DIR}` is a documentation placeholder, not a guaranteed shell environment variable.
Resolve `BIN` to a real launcher path once before the first CLI call.
Do not call `node app/dist/cli.js` directly.

## Scope and boundaries

- GitHub Issues and milestones only.
- CLI-mediated operations only.
- Do not call GitHub REST endpoints directly from skill content.
- Sprint semantics map to milestones so scenarios can keep using the shared `tracker.sprint.*` contract.

## Capability Domain

Domain:
- `tracker`

Provides:
- `tracker.config.get`
- `tracker.config.set`
- `tracker.issue.get`
- `tracker.issue.search`
- `tracker.issue.create`
- `tracker.issue.update`
- `tracker.issue.assign`
- `tracker.sprint.get`
- `tracker.sprint.issues`
- provider-specific workflow helpers

Config check:
- `github-issue config get`

## Config check

Run `github-issue config get` when configuration state is unknown or before the first provider-scoped task in a new session.

## Supporting files

- Read `references/commands.md` for the packaged command surface.
- Read `references/usage.md` for execution policy and read/write behavior.
