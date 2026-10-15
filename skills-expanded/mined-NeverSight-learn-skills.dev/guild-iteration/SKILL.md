---
name: guild-iteration
description: Create, list, update, and delete Guild iterations (sprints) via the guild CLI. Use when the user asks about sprints, iterations, or capacity planning in Guild.
metadata:
  requires:
    bins: ["guild"]
    cliHelp: "guild iteration --help"
---
# guild-iteration

## Overview

Manage iterations through `guild iteration` subcommands. Iteration numbers (`--no`) are project-scoped.

## When to use

- Planning sprints with title, date range, and story points.
- Assigning tickets to an iteration via `guild ticket set-iteration`.

## Prerequisites

Complete [guild-shared](../guild-shared/SKILL.md) setup.

## Commands

```bash
guild iteration list --json
guild iteration get --no <n>
guild iteration create --title "Sprint 1" --start-at 2026-01-01 --deadline 2026-01-14 --points 40
guild iteration update --no <n> [--title ...] [--points 50]
guild iteration delete --no <n>
```

## Permissions

All iteration CRUD requires `P.ticket.manage`.

## Help

```bash
guild iteration --help
guild iteration create --help
```

## Related

Assign tickets: `guild ticket set-iteration --no <ticketNo> --iteration-no <n>` (use `--iteration-no 0` or check `--help` for clearing iteration).
