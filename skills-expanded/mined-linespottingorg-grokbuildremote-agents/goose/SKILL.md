---
name: goose
description: >
  Pair Build Remote Agent to Goose. If Goose runs in a TTY the phone sees that
  window; otherwise add gbr-mcp on the desktop Goose. Pin gbr-agent v0.6.2.
compatibility: Requires gbr-agent ≥ 0.6.2. Loopback only. No mailbox keys. Unaffiliated with block/goose.
metadata:
  version: "0.6.2"
  product: "Build Remote Agent"
  website: "https://grokbuildremote.com/integrations.html"
---

# Goose + Build Remote Agent

Unaffiliated. This skill lives **here**, not in `block/goose`.
Index: https://grokbuildremote.com/integrations.html

| You run | Phone sees |
|---------|------------|
| `goose` **in a terminal** | That window. Inject types into it. |
| Goose Desktop, `goose serve`, HTTP / Telegram | Nothing useful. Add **gbr-mcp** on the **desktop**. Phone still only lists TTYs. |

`goose-ios` is Goose’s own remote. Do not mix that tunnel with `gbr/1`.

## Pair (pin v0.6.2)

Checksum the installer, then the binary — [docs/PINNED-INSTALL.md](../../docs/PINNED-INSTALL.md).

```bash
gbr-agent version    # v0.6.2
gbr-agent pair
gbr-agent run        # other terminal
export GBR_BOT_REQUIRE_KEY=1
```

## Desktop MCP (when Goose is not a TTY)

```bash
git clone --branch v0.6.2 --depth 1 https://github.com/LinespottingOrg/GrokBuildRemote-Agents.git
cd GrokBuildRemote-Agents/mcp/gbr-mcp && npm ci --ignore-scripts && chmod +x bin/gbr-mcp.js
```

`goose configure` → Add Extension → Command-line Extension, or `~/.config/goose/config.yaml`:

```yaml
extensions:
  gbr:
    enabled: true
    type: stdio
    name: gbr
    cmd: node
    args: ["/ABSOLUTE/PATH/GrokBuildRemote-Agents/mcp/gbr-mcp/bin/gbr-mcp.js"]
    timeout: 300
```

Desktop Goose can call Bot API. The phone still lists **terminal windows** on this PC.

Relay pair (`POST /v1/mb/:id/pair`) is keyless and throttled. Push / poll / ack need `X-GBR-Key`. Never commit `mailbox_key`.
