---
name: rules-infra
description: Binding personal rules for live infrastructure and the local machine — load before touching any cloud/prod/staging resource (AWS/ECS/DNS/domains/hosts), any destructive action, or Docker/Colima on this Mac.
---

# rules-infra

These rules are binding (moved verbatim from ~/.claude/CLAUDE.md). Each heading names its full-text file in `~/.claude/rulebook/`: **Read that file before acting in its area** — the one-liners are the trigger, not the whole rule.

## Live Infrastructure — `18-live-infrastructure-change-safety.md`
- PROD (your-org us-east-1) strictly READ-ONLY: no infra/env/task-def changes, no scripts; fixes go via code PR or are surfaced for humans.
- Verify live state first; task-def change = rolling restart (check health survives); avoid raw `aws ecs` CLI edits (follow operate-ecs-services-safely); one deliberate change at a time; rollback isn't guaranteed; confirm before shared-env changes, prefer reversible flips.
- **Any destructive action (any resource/tool) → revert runbook first**: capture state + restore commands, hold the cheapest undo-token until the post-test passes, snapshot before data deletion, re-test the real consumer. Urgent prod incident + safe fix → apply now.
- **Retiring a host / moving a domain → prove ZERO prod consumers in every app first**: every app × env incl. legacy V1 apps and apps pinned to an old shared-library version (read the PROD branch's pin, not rc's); grep each live prod bundle + build env for the host and read the host's access logs; an rc-only migration is not a prod migration; move every old-domain host a client calls (APIs, reports, uploads, tiles, webhooks), not just the one asked about; after the cut drive each prod client's real flow (a 307/wildcard 200 HTML is a failure).

## Local Machine — `20-local-machine-container-runtime-is-colima-not-do.md`
- Colima, not Docker Desktop (never install/suggest it). Daemon down → `colima start`. Only `~` and `/tmp/colima` are mounted. More resources → `colima stop && colima start --cpu N --memory N`.
