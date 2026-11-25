---
name: gbr-nemoclaw
description: >
  Drive Grok Build CLI from NemoClaw. gbr-agent and gbr-mcp stay on the HOST.
  Do not copy them into OpenShell. Not a NemoClaw Community recipe.
compatibility: Host tool. Sandbox must call host loopback / host stdio only.
metadata:
  version: "0.6.1"
  product: "Build Remote Agent"
  website: "https://grokbuildremote.com/integrations.html"
---

# NemoClaw → Grok Build CLI (host)

NemoClaw sandboxes **its** agent. Build Remote Agent is the **host** tool.
This is **not** a NemoClaw / OpenShell recipe. Do not PR it into
`examples/recipes/` until an independently verified OpenShell workflow exists.
Discoverability: https://grokbuildremote.com/integrations.html

## Host

`gbr-agent run` is long-running — split terminals. Keep both on the Mac/PC, not in the sandbox.

```bash
# terminal 1
gbr-agent pair
gbr-agent run
```

```bash
# terminal 2 — after run is up
export GBR_BOT_REQUIRE_KEY=1
bash scripts/setup-gbr-mcp.sh       # pins gbr-mcp @ v0.6.2 under ~/.gbr/gbr-mcp-src
```

Point NemoClaw at **host** stdio `node ~/.gbr/gbr-mcp-src/mcp/gbr-mcp/bin/gbr-mcp.js`
(or Bot API `http://127.0.0.1:8788` with the key). Do not install `gbr-agent` inside
OpenShell. No fourth pair protocol.

The paired app can inject into the host `grok` TTY (remote-control client, host-keyboard
authority). Device class `phone` is not an inject target. The sandbox UI is not on the roster.

## Loop

`gbr_diagnose` → `gbr_open` `command=grok` `holder=nemoclaw` → inject → `gbr_result`.

That `grok` process is a **host TTY**, not an OpenShell session. Do not claim NemoClaw E2E
without a captured OpenShell path.
