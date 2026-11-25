---
name: gbr
description: >
  Drive Grok Build CLI (grok) through Build Remote Agent from OpenClaw / Hermes / NemoClaw.
  Attach via stdio gbr-mcp. Pair the phone as a remote-control client for that grok TTY (host keyboard).
compatibility: Requires gbr-agent run on the host. Loopback. No mailbox keys in this file.
metadata:
  version: "0.6.1"
  product: "Build Remote Agent"
  website: "https://grokbuildremote.com/use-cases/claw.html"
---

# OpenClaw / claw → Grok Build CLI

One adapter. Not 50 one-off integrations. Default target is **Grok Build CLI** (`grok`).

Independent Linespotting AB. Not affiliated with OpenClaw, Hermes, NVIDIA, xAI, or SpaceX.

## Pair (remote-control client — optional, same mailbox)

1. Pin `gbr-agent` v0.6.2 — https://grokbuildremote.com/PINNED-INSTALL.md
2. PC: `gbr-agent pair` then `gbr-agent run` (keep running).
3. Phone: Build Remote Agent → scan QR.
4. OpenClaw **device-pair** (LAN/Bonjour) is a **different** protocol. Do not mix with `gbr/1`.

Unpair on the phone before a new mailbox.

## Attach (MCP client → grok)

| How | Where |
|-----|--------|
| MCP | stdio `gbr-mcp` (`node …/bin/gbr-mcp.js`) |
| Bot API | `http://127.0.0.1:8788` after `gbr-agent run` — **REST, not MCP** |

Do **not** `hermes mcp add` / OpenClaw MCP the `:8788` URL. That is JSON REST. MCP is stdio.

```bash
export GBR_BOT_REQUIRE_KEY=1
bash scripts/setup-gbr-mcp.sh
# Windows: powershell -NoProfile -File .\scripts\setup-gbr-mcp.ps1
# then:
# hermes mcp add gbr -- stdio -- node $HOME/.gbr/gbr-mcp-src/mcp/gbr-mcp/bin/gbr-mcp.js
```

Pin: `git clone --branch v0.6.2 --depth 1` if you clone by hand. Never default branch + `npm install`. Prefer `npm ci --ignore-scripts` once the tag includes `package-lock.json`.

## Loop — this is what makes grok work

1. `gbr_diagnose`
2. `gbr_open` — omit session_id; `command` defaults to **grok**; set `holder=openclaw` (or `hermes` / `nemoclaw`)
3. `gbr_inject` the coding task with `submit=true` (or `gbr_inject_and_wait`)
4. `gbr_result` `wait_ms=60000`
5. `gbr_lock` `action=release` when done

If `grok` is not on PATH, `gbr_open` opens a shell and tells you to install Grok Build.

Phone roster = that **grok TTY**, not the OpenClaw / Hermes / NemoClaw UI.

## `/rename` (own TUI line)

`/rename TITLE` must be its **own submitted TUI line** in Grok Build. Do not bury it in a paste. Alias `/title`. Inbox watcher uses two submits: (1) `/rename TITLE` (2) the job body.

## Inbox watch (no paste)

With `gbr-agent run` and `gh` on PATH, the agent polls `LinespottingOrg/grok-build-inbox` label `boss-steer`. Matching Grok Build title → inject newest comment. Spawn cwd is `~/Developer` on Mac Mini (`GBR_OPEN_CWD`), not `$HOME` or Dropbox. After the watcher is running, **do not paste**. `GBR_INBOX_WATCH=0` disables.

## NemoClaw

NemoClaw is a **sandbox, not a fourth pair**. GBR stays on the **host**. Do not copy `gbr-agent` into OpenShell. See `skills/nemoclaw/SKILL.md`.

## Hermes

See `skills/hermes/SKILL.md`. Same loop.

## ClawHub

Publish this skill with human `clawhub login` — not a GitHub PR on `openclaw/openclaw`.
