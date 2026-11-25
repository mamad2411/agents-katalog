---
name: payclaw-io
description: "Badge identity + virtual Visa cards for AI agents. Declare, pay, audit — on existing Visa rails. MCP-native."
---

# kyaLabs — Badge + Spend

Agents are not bots. kyaLabs proves it — then lets them pay.

## Setup

Add to your MCP client config:

```json
{
  "mcpServers": {
    "kyalabs": {
      "command": "npx",
      "args": ["-y", "@kyalabs/mcp-server"],
      "env": {
        "KYA_API_KEY": "your_key_here",
        "KYA_API_URL": "https://www.kyalabs.io"
      }
    }
  }
}
```

Get your API key at [kyalabs.io](https://www.kyalabs.io).

## Tools

| Tool | Description |
|------|-------------|
| `kya_getAgentIdentity` | Declare identity → get verification token (Badge) |
| `kya_getCard` | Declare purchase intent → get virtual Visa (Spend) |
| `kya_reportPurchase` | Report outcome → close the audit trail |

## How It Works

**Badge:** Agent declares identity before shopping. Merchants see a verified authorized actor, not anonymous traffic.

**Spend:** Agent declares purchase intent. Human approves. Single-use virtual Visa issued. Card self-destructs after use. Your real card never enters the chat.

## Badge Only?

If you only need identity (no payment), use [payclaw-badge](https://clawhub.com/skills/payclaw-badge).

## Links

- [kyalabs.io](https://www.kyalabs.io)
- [Trust & Verification](https://www.kyalabs.io/trust)
- [npm: @kyalabs/mcp-server](https://www.npmjs.com/package/@kyalabs/mcp-server)
