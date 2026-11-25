---
name: gbr-password-managers
description: >
  Use 1Password CLI (op) or LastPass CLI (lpass) on a PC already paired with
  Build Remote Agent. Host-side only. Not a pair protocol. Phone never sees vault items.
compatibility: Requires gbr-agent ≥ 0.6.2 already paired. Attach stays :8788 / gbr-mcp.
metadata:
  version: "0.6.2"
  product: "Build Remote Agent"
  website: "https://grokbuildremote.com/integrations.html"
---

# 1Password / LastPass — host CLI (not a pair)

Unaffiliated. This skill lives **here**. Plan: [docs/PASSWORD-MANAGERS.md](../../docs/PASSWORD-MANAGERS.md)

| Surface | Role |
|---------|------|
| `gbr-agent pair` then `run` | The **only** pair |
| `:8788` / `gbr-mcp` | The **only** attach |
| `op` / `lpass` on this PC | Host CLI after the user is already signed in |
| Phone | TTY remote-control. Never a vault. |

```bash
gbr-agent version    # v0.6.2
gbr-agent pair
gbr-agent run
export GBR_BOT_REQUIRE_KEY=1
op account list
lpass status
```

Never: fourth pair protocol, inject vault fields, return secrets from MCP/relay, PR into 1Password/LastPass trees.
