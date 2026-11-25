---
name: gbr-hermes
description: >
  Drive Grok Build CLI (grok) from Hermes via gbr-mcp stdio.
  Requires gbr-agent run on the same host. Phone spectates that grok TTY after pair.
compatibility: Host loopback. Do not treat http://127.0.0.1:8788 as MCP.
metadata:
  version: "0.6.1"
  product: "Build Remote Agent"
  website: "https://grokbuildremote.com/use-cases/claw.html"
---

# Hermes → Grok Build CLI

Unaffiliated. Hermes stays Hermes. This skill attaches **Grok Build CLI** (`grok`)
through Build Remote Agent. Protocol `gbr/1`.

## Host (once)

```bash
# pin installer — https://grokbuildremote.com/PINNED-INSTALL.md
gbr-agent version          # v0.6.2
gbr-agent pair && gbr-agent run
export GBR_BOT_REQUIRE_KEY=1
bash /path/to/GrokBuildRemote-Agents/scripts/setup-gbr-mcp.sh
# prints: hermes mcp add gbr -- stdio -- node $HOME/.gbr/gbr-mcp-src/mcp/gbr-mcp/bin/gbr-mcp.js
```

Windows (same protocol, stdio not `:8788`):

```powershell
$env:GBR_BOT_REQUIRE_KEY = '1'
powershell -NoProfile -File .\scripts\setup-gbr-mcp.ps1
```

`:8788` is **Bot API REST**. Hermes MCP must be **stdio `gbr-mcp`**, not that URL.

## Loop (every task)

1. `gbr_diagnose`
2. `gbr_open` with `command=grok` (default) and `holder=hermes` — spawns `grok` in a TTY
3. `gbr_inject` / `gbr_inject_and_wait` the prompt (`submit=true`)
4. `gbr_result` wait_ms=60000
5. `gbr_lock` release when done

Phone (if paired) lists that Grok Build window. Do not expect Hermes UI on the phone.

Pin clone: `git clone --branch v0.6.2 --depth 1` — never default-branch + `npm install`. Prefer `npm ci --ignore-scripts` once the tag includes `package-lock.json`.
