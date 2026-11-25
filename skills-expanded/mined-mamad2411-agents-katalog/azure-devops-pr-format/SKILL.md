---
name: azure-devops-pr-format
description: Apply when creating or updating a pull request via the Azure DevOps MCP. Defines the title and description format enforced by guard-pr-format.sh.
metadata:
  stack: [azure]
---

# Azure DevOps PR format

The `guard-pr-format.sh` PreToolUse hook enforces this contract on `mcp__azure-devops__repo_create_pull_request` and `mcp__azure-devops__repo_update_pull_request`. If a PR call doesn't match, the hook blocks with `exit 2` and the user sees the violation.

## Title

```
type(topic): Description
```

Rules:

- `type` — one of `feat`, `fix`, `chore`, `refactor`, `docs`, `test`.
- `topic` — kebab-case feature area, e.g. `daily-limits`, `oauth-rotation`, `chat-widget`.
- `Description` — starts with a capital letter, sentence case, no trailing period.
- Total length — at most 72 characters.

### Examples (good)

- `feat(daily-limits): Add per-user daily limit`
- `fix(session-cookie): Stop leaking cookie on signout`
- `refactor(vendor-adapters): Extract HMAC verifier`
- `docs(gate-pipeline): Clarify stack-conditional gate skipping`

### Examples (rejected)

- `Add daily limits` — missing `type(topic):` prefix.
- `feat: daily limits` — missing `(topic)`.
- `feat(DailyLimits): add daily limit` — topic must be kebab-case; description must start with a capital.
- `feat(daily-limits): add daily limit.` — trailing period not allowed.

## Description

- Use real newlines, not literal `\n` escape sequences.
- Reference work item with `Refs ADO <id>` at the bottom (matches the project convention).
- Bullet-list the changes; one-line summary at the top.
- Linked design doc paths welcome.

## When the hook fires

Only on PR create/update via the Azure DevOps MCP. Local commits, force-pushes, and other PR providers are unaffected. The `azure` stack tag means this skill loads only when `azure` is in the active manifest.
