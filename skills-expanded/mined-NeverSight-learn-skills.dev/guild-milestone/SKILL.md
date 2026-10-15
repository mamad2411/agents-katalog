---
name: guild-milestone
description: Create, list, update, close, and reopen Guild milestones via the guild CLI. Use when the user asks about milestones, releases, or roadmap planning in Guild.
metadata:
  requires:
    bins: ["guild"]
    cliHelp: "guild milestone --help"
---

# guild-milestone

## Overview

Manage project milestones through `guild milestone` subcommands. Milestone numbers (`--no`) are project-scoped sequence numbers, not internal IDs.

## When to use

- Listing or inspecting milestones.
- Creating or updating milestone title, content, or deadline.
- Closing or reopening a milestone.

## Prerequisites

Complete [guild-shared](../guild-shared/SKILL.md) setup (`auth login`, `config init`).

## Commands

```bash
guild milestone list [--status OPEN|CLOSED] --json
guild milestone get --no <n>
guild milestone create --title "M1" [--deadline 2026-12-31]
guild milestone update --no <n> [--title "..."] [--deadline ...]
guild milestone delete --no <n>
guild milestone close --no <n>
guild milestone reopen --no <n>
```

## Permissions

Milestone operations require PO-level permissions in the project:

- create → `P.milestone.create`
- update → `P.milestone.write`
- delete → `P.milestone.delete`
- close / reopen → `P.milestone.close`

## Help

If unsure about options, run:

```bash
guild milestone --help
guild milestone create --help
```

## Notes

- `deadline` must not be before today when creating or updating.
- Only root tickets (IDEA/BUG) can be assigned to a milestone via `guild ticket set-milestone`.
