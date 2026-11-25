---
name: cline
description: >
  Pair Build Remote Agent to Cline. If Cline runs in a TTY the phone sees that
  window; otherwise add gbr-mcp on the desktop Cline. Pin gbr-agent v0.6.2.
compatibility: Requires gbr-agent ≥ 0.6.2. Loopback only. No mailbox keys. Unaffiliated with cline/cline.
metadata:
  version: "0.6.2"
  product: "Build Remote Agent"
  website: "https://grokbuildremote.com/integrations.html"
---

# Cline + Build Remote Agent

Unaffiliated. This skill lives **here**, not in `cline/cline`.
Index: https://grokbuildremote.com/integrations.html

| You run | Phone sees |
|---------|------------|
| `cline` **in a terminal** | That window. Inject types into it. |
| Cline VS Code / JetBrains panel | Nothing useful. Add **gbr-mcp** on the **desktop**. Phone still only lists TTYs. |

Cline Kanban / Tailscale remote-access is not `gbr/1`.

## Pair (pin v0.6.2)

Checksum the installer, then the binary — [docs/PINNED-INSTALL.md](../../docs/PINNED-INSTALL.md).

```bash
gbr-agent version    # v0.6.2
gbr-agent pair
gbr-agent run        # other terminal
export GBR_BOT_REQUIRE_KEY=1
```

## Desktop MCP (when Cline is not a TTY)

```bash
git clone --branch v0.6.2 --depth 1 https://github.com/LinespottingOrg/GrokBuildRemote-Agents.git
cd GrokBuildRemote-Agents/mcp/gbr-mcp && npm ci --ignore-scripts && chmod +x bin/gbr-mcp.js
```

```bash
cline mcp add gbr -- node /ABSOLUTE/PATH/GrokBuildRemote-Agents/mcp/gbr-mcp/bin/gbr-mcp.js
```

IDE: Cline panel → MCP Servers:

```json
{
  "mcpServers": {
    "gbr": {
      "command": "node",
      "args": ["/ABSOLUTE/PATH/GrokBuildRemote-Agents/mcp/gbr-mcp/bin/gbr-mcp.js"],
      "disabled": false
    }
  }
}
```

Relay pair is keyless and throttled. Push / poll / ack need `X-GBR-Key`. Never commit `mailbox_key`.
