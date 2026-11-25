---
name: gbr-qa
description: >
  Grok multi-agent QA loop via Build Remote Agent. Spawn grok windows, lock
  each, inject, wait idle, iterate until gbr_tasks status=done. Agent and relay
  are free. Phone app is optional remote-control client (not an inject target).
compatibility: gbr-agent ≥ 0.6.2. Loopback Bot API or stdio gbr-mcp. No mailbox keys.
metadata:
  version: "0.6.2"
  product: "Build Remote Agent"
  website: "https://grokbuildremote.com/use-cases/qa.html"
---

# Multi-agent QA

You orchestrate. `gbr-agent` is MIT. Hosted relay is free. Device class `phone` is **not** an inject target (`cannot_inject_phone`).

## Setup

```bash
gbr-agent version    # v0.6.2
gbr-agent pair       # only if a phone should watch
gbr-agent run
export GBR_BOT_REQUIRE_KEY=1
```

MCP: `git clone --branch v0.6.2 --depth 1` then `npm ci --ignore-scripts` in `mcp/gbr-mcp` (and `chmod +x bin/gbr-mcp.js` on macOS/Linux). Do not treat `:8788` as MCP.

## Loop

1. `gbr_diagnose`
2. `gbr_open` `command=grok` `holder=writer` `goal=<fix>`
3. `gbr_open` `command=grok` `holder=tester` `goal=<verify>` — **different session_id**
4. `gbr_lock` each (do not share a window)
5. Writer inject → `gbr_result`
6. Tester inject → `gbr_result`
7. `gbr_tasks` upsert `status=running|done|failed`
8. Repeat until `done`. Release locks.

Empty `session_id` attaches an existing grok window (spawn cap 3 / 10 min). Do not loop `sessions/open`.

Playbook: [docs/USE-CASE-MULTI-AGENT-QA.md](../../docs/USE-CASE-MULTI-AGENT-QA.md)
