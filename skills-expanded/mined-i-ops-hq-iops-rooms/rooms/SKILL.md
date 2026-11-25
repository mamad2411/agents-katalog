---
name: rooms
description: >
  Local Rooms by I-Ops live session board. Use while coding in Cursor, Claude Code,
  or Codex so teammates see work as it happens — post_note / share_diff on meaningful
  steps, not only at the end. Offline. Writes only to .room/
---

# Rooms by I-Ops

You post to a **local** room on this machine. The live board (`rooms live` → http://127.0.0.1:7840/) updates for anyone with the tab open. Nothing is uploaded to I-Ops.

## Contract (do not violate)

- Do not read or print secrets, `.env`, SSH keys, or `process.env`.
- Do not run network commands for this skill.
- Write room data only via the `iops-rooms` MCP tools or `rooms` CLI.
- Prefer short notes and diffs people can read on the board.

## Setup (once per project)

1. Prefer one-command install: `npx -y iops-rooms@0.13.3 mcp install` (or `rooms mcp install`). Merges `.cursor/mcp.json` and copies this skill to `.cursor/skills/rooms/SKILL.md`.
2. Reload MCP / restart the agent host.
3. If no `.room/` yet: `create_room` with name `Rooms` (or the feature name).
4. Tell the human to run `rooms live` and leave the tab open.
5. If the board looks empty or something feels broken: run MCP tool `doctor` (or `rooms doctor`).

This repo’s checkout already has `.cursor/mcp.json` → `src/mcp.js`. For **other projects**, `mcp install` writes:

```json
{
  "mcpServers": {
    "iops-rooms": {
      "command": "npx",
      "args": ["-y", "iops-rooms@0.13.3", "mcp"]
    }
  }
}
```

Pin a version. Never `@latest`. Or point `command`/`args` at a local checkout’s `src/mcp.js`.

## Actively show live (default while working)

Do **not** wait for the human to ask every time. On **meaningful steps**, post as you go:

1. `post_note` when you start a chunk (goal in one line).
2. `share_diff` when you change files worth reviewing (path + unified diff or excerpt — never `.env` / keys).
3. `post_note` when you finish, block, change plan, or open a PR.
4. `request_review` / `approve` write a row in the log. They notify nobody, gate nothing, and
   approving does not authorise you to do anything — use them to record what happened, never to
   clear yourself to proceed.
5. If the board is empty after init: `doctor`, then post — empty means nothing was posted yet.

Keep notes short. Branch is stamped automatically from git (or `ROOMS_BRANCH`).

Optional human setup: `rooms hooks install` posts short commit/checkout notes via local git hooks only — **not** IDE telemetry. Prefer MCP `post_note` / `share_diff` for agent work.

## Tools

| Tool | When |
|---|---|
| `create_room` / `join_room` | First touch / match code |
| `rename_room` | Display title only (code unchanged) |
| `post_note` | Progress, decisions, blockers |
| `share_diff` | File changes for the board |
| `request_review` / `approve` | Write a row in the log — records a claim, permits nothing |
| `read_transcript` / `wait_for_peer` | Catch up / wait |
| `doctor` | Empty board / MCP / identity diagnosis |

## Human companion commands

```bash
rooms live          # leave open — auto-updates on 127.0.0.1
rooms doctor        # why is the board empty?
rooms hooks install # opt-in local git auto-post (not IDE telemetry)
rooms status
rooms branches
rooms rename Rooms
```
