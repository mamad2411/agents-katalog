---
name: qrveloz
display_name: QrVerloz — Dynamic QR Codes
description: Create, retarget, and inspect dynamic QR codes from any AI assistant. No account required to start.
version: 1.0.0
author: Neoshrek
homepage: https://qrverloz.com
mcp_server: https://qrverloz.com/api/mcp
tags: [qr-codes, marketing, redirects, analytics, productivity]
---

# QrVerloz Skill

This skill connects to the QrVerloz MCP server, enabling you to create and manage dynamic QR codes without leaving your AI assistant.

## Setup

### 1. Add the MCP server

Add the following to your MCP client configuration:

**HTTP clients (Cursor, Claude Code, Continue):**
```json
{
  "mcpServers": {
    "qrveloz": {
      "type": "http",
      "url": "https://qrverloz.com/api/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

**VS Code with GitHub Copilot** — save as `.vscode/mcp.json` in your workspace:
```json
{
  "servers": {
    "qrveloz": {
      "type": "http",
      "url": "https://qrverloz.com/api/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

**Claude Desktop (via mcp-remote):**
```json
{
  "mcpServers": {
    "qrveloz": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://qrverloz.com/api/mcp",
               "--header", "Authorization: Bearer YOUR_API_KEY"]
    }
  }
}
```

### 2. Get a free API token

No email required. In your AI assistant:

```
Use the QrVerloz MCP tool to request an API key
```

Replace `YOUR_API_KEY` in your config with the returned token.

---

## What You Can Do

### Create a QR code
```
Use the QrVerloz MCP tool to create a QR code titled "Product launch" pointing to https://example.com/launch
```

### Change where it points — no reprinting
```
Use the QrVerloz MCP tool to update QR code abc123 to point to https://example.com/new-page
```

### Check scan analytics
```
Use the QrVerloz MCP tool to get the scan count for QR code clxxx...
```

### List all your codes
```
Use the QrVerloz MCP tool to list all my QR codes
```

### Check your plan and remaining capacity
```
Use the QrVerloz MCP tool to show my account info
```

---

## Available Tools

| Tool | Auth Required | Purpose |
|------|---------------|---------|
| `request_api_key` | No | Get a free token — no signup |
| `create_qr_code` | Optional | Create a dynamic QR code |
| `get_qr_code` | Yes | Look up a code by ID or short code |
| `list_qr_codes` | Yes | List all codes |
| `get_qr_scans` | Yes | Get scan count |
| `update_qr_target` | Yes | Retarget without reprinting |
| `delete_qr_code` | Yes | Delete a code permanently |
| `get_account_info` | Yes | Plan and usage info |

---

## Pricing

See [qrverloz.com/#pricing](https://qrverloz.com/#pricing) for current plan details.

## Claim Your Account

Free tokens expire after 90 days but your QR codes don't have to. Visit [qrverloz.com/claim](https://qrverloz.com/claim) to link an email and make your account permanent.
