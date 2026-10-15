---
name: guild-ticket
description: Create, update, publish, and manage Guild tickets (IDEA, BUG, STORY, SUBTASK) via the guild CLI. Use when the user asks about tickets, bugs, stories, subtasks, or ticket workflows in Guild.
metadata:
  requires:
    bins: ["guild"]
    cliHelp: "guild ticket --help"
---

# guild-ticket

## Overview

Manage tickets through `guild ticket` subcommands. Ticket numbers (`--no`) are project-scoped.

## Hierarchy rules

| Type | Parent | Milestone |
| --- | --- | --- |
| IDEA / BUG | Must be root (no parent) | Allowed on root only |
| STORY | Parent must be IDEA | Not allowed |
| SUBTASK | Parent must be STORY or BUG | Not allowed |

## Typical workflow

1. Create BUG or IDEA at root: `guild ticket create --type BUG --title "..." --content-file ./bug.md`
2. Break down STORY: `guild ticket create --type STORY --parent-no <ideaNo> --title "..."`
3. Add SUBTASK under STORY or BUG: `guild ticket create --type SUBTASK --parent-no <storyOrBugNo> --title "..."`
4. Set level: `guild ticket set-level --no <n> --level 2`
5. Assign milestone (root only): `guild ticket set-milestone --no <n> --milestone-no 3`
6. Publish: `guild ticket publish --no <n>`
7. Move to todo lane (creates take action): `guild ticket set-stage --no <n> --stage todo`
8. Take / submit / approve: `guild ticket action --no <n> --name take|submit|approve|reject|untake`

Publish only marks the ticket as published; you must set stage to `todo` before developers can take it (same as moving a card on the kanban).

Approve/reject actions are assigned to the ticket **owner** (usually PO), not PM.

Submit accepts an optional `--pull-request-url`; the repo must be bound to the project or omit the URL.

## Commands

```bash
guild ticket list [--type IDEA|BUG|STORY|SUBTASK] [--status ...] --json
guild ticket get --no <n>
guild ticket create --type BUG --title "..." [--content-file path] [--parent-no <n>] [--milestone-no <n>]
guild ticket update --no <n> [--title ...] [--content-file path]
guild ticket delete --no <n>
guild ticket set-milestone --no <n> [--milestone-no <n>]
guild ticket set-level --no <n> --level <n>
guild ticket set-stage --no <n> --stage todo|doing|review|done
guild ticket set-stage --no <n> --clear
guild ticket set-iteration --no <n> [--iteration-no <n>]
guild ticket publish --no <n>
guild ticket unpublish --no <n>
guild ticket close --no <n>
guild ticket reopen --no <n>
guild ticket action --no <n> --name take|untake|submit|approve|reject [--pull-request-url ...]
```

## Permissions (summary)

- IDEA/BUG create: project access
- STORY/SUBTASK create: `P.ticket.manage`
- publish / unpublish: `P.ticket.publish` / `P.ticket.unpublish`
- set-stage: `P.ticket.manage`
- close / reopen: `P.ticket.close`
- actions: `P.ticket.action`

## Help

When parameters are unclear, run help first:

```bash
guild ticket --help
guild ticket create --help
guild ticket action --help
```

## Tips

- Use `--content-file` for long markdown bodies.
- Use `--json` (default) for machine-readable output.
- Do not use internal UUIDs; always use `--no`.
