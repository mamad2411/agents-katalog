---
name: gbr-mcp
description: >
  MCP stdio server for Build Remote Agent. Pin git clone --branch v0.6.2, then
  npm ci --ignore-scripts from that tag. Loopback :8788 vs HTTPS relay. Harden
  loopback with GBR_BOT_REQUIRE_KEY=1.
compatibility: Requires Node ≥ 20 and gbr-agent ≥ 0.6.2. No mailbox keys. Do not clone the default branch.
metadata:
  version: "0.6.2"
  product: "Build Remote Agent"
  website: "https://grokbuildremote.com/integrations.html"
---

# gbr-mcp — MCP attach

Protocol `gbr/1`. Independent Linespotting AB product. Not affiliated with xAI or SpaceX.

| | |
|--|--|
| Index | https://grokbuildremote.com/integrations.html |
| Pin | [docs/PINNED-INSTALL.md](../../docs/PINNED-INSTALL.md) |
| Pair | `skills/gbr/SKILL.md` |
| Server | `mcp/gbr-mcp` (tag **v0.6.2**) |

Phone roster = **terminal windows** on the paired PC, not this MCP client. The paired app can inject into listed TTYs (remote-control client).

## Do not

```bash
git clone https://github.com/LinespottingOrg/GrokBuildRemote-Agents.git
cd GrokBuildRemote-Agents/mcp/gbr-mcp && npm ci --ignore-scripts
```

That clones **main**. It is not a trust root.

## Pin `--branch v0.6.2`

```bash
git clone --branch v0.6.2 --depth 1 https://github.com/LinespottingOrg/GrokBuildRemote-Agents.git
cd GrokBuildRemote-Agents/mcp/gbr-mcp
npm ci --ignore-scripts
chmod +x bin/gbr-mcp.js   # macOS/Linux
node bin/gbr-mcp.js --diagnose
```

```bash
gbr-agent pair
gbr-agent run
export GBR_BOT_REQUIRE_KEY=1
```

## Loopback vs relay

| Surface | Auth |
|---------|------|
| `http://127.0.0.1:8788` | Unauthenticated unless `GBR_BOT_REQUIRE_KEY=1` |
| `POST /v1/mb/:id/pair` | Keyless, throttled (issues the key) |
| Relay push / poll / ack / Bot API | `X-GBR-Key` or Bearer |

```json
{
  "mcpServers": {
    "gbr": {
      "command": "node",
      "args": ["/ABSOLUTE/PATH/GrokBuildRemote-Agents/mcp/gbr-mcp/bin/gbr-mcp.js"],
      "env": { "GBR_MCP_LOG_LEVEL": "info" }
    }
  }
}
```

Never commit `mailbox_key`.
