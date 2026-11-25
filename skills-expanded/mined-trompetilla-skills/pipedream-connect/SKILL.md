---
name: pipedream-connect
description: Connect 2,000+ APIs with managed OAuth via Pipedream. Includes full UI integration for Clawdbot Gateway dashboard.
metadata: {"clawdbot":{"emoji":"🔌","requires":{"bins":["mcporter"],"clawdbot":">=2026.1.0"},"category":"integrations"}}
---

# Pipedream Connect

Connect your AI agent to 2,000+ APIs with managed OAuth via Pipedream. This skill provides:

- **Full UI Dashboard** — Configure credentials, connect apps, manage tokens
- **Automatic Token Refresh** — Cron job keeps tokens fresh
- **MCP Integration** — Apps become tools your agent can use via mcporter

## Overview

Pipedream Connect handles OAuth flows for thousands of APIs, so your agent can access Gmail, Google Calendar, Slack, GitHub, and more without managing tokens manually.

## Prerequisites

1. **Pipedream Account** — Sign up at [pipedream.com](https://pipedream.com)
2. **mcporter** — MCP tool runner (`npm install -g mcporter`)
3. **Clawdbot Gateway** — v2026.1.0 or later with UI enabled

## Quick Start

### Step 1: Create Pipedream OAuth Client

1. Go to [pipedream.com/settings/api](https://pipedream.com/settings/api)
2. Click **"New OAuth Client"**
3. Copy the **Client ID** and **Client Secret**

### Step 2: Create a Pipedream Project

1. Go to [pipedream.com/projects](https://pipedream.com/projects)
2. Create a new project (e.g., "clawdbot")
3. Copy the **Project ID** (starts with `proj_`)

### Step 3: Configure in Clawdbot UI

1. Open Clawdbot Dashboard → **Tools** → **Pipedream**
2. Click **Configure** and enter:
   - Client ID
   - Client Secret
   - Project ID
   - Environment (development/production)
   - External User ID (e.g., "clawdbot")
3. Click **Save Credentials**

### Step 4: Connect Apps

1. In the Pipedream UI, click **Connect** on any app (e.g., Gmail, Google Calendar)
2. Complete the OAuth flow in the popup
3. Click **Connect** again to finalize

### Step 5: Set Up Token Refresh (Recommended)

Pipedream tokens expire after 1 hour. Set up automatic refresh:

```bash
# Copy the token refresh script
cp ~/clawd/skills/pipedream-connect/scripts/pipedream-token-refresh.py ~/clawd/scripts/

# Set up cron job (runs every 45 minutes)
(crontab -l 2>/dev/null; echo "*/45 * * * * /usr/bin/python3 $HOME/clawd/scripts/pipedream-token-refresh.py >> $HOME/clawd/logs/pipedream-cron.log 2>&1") | crontab -
```

## Usage

Once connected, your agent can use app tools via mcporter:

```bash
# Gmail
mcporter call pipedream-clawdbot-gmail.gmail-find-email \
  instruction="Find unread emails from today"

mcporter call pipedream-clawdbot-gmail.gmail-send-email \
  instruction="Send email to bob@example.com with subject 'Hello' and body 'Hi there!'"

# Google Calendar
mcporter call pipedream-clawdbot-google-calendar.google_calendar-list-events \
  instruction="Show my events for this week"

mcporter call pipedream-clawdbot-google-calendar.google_calendar-create-event \
  instruction="Create a meeting tomorrow at 2pm called 'Team Standup'"

# Slack
mcporter call pipedream-clawdbot-slack.slack-send-message \
  instruction="Send 'Hello team!' to the #general channel"
```

## Architecture

### Files Created

| Location | Purpose |
|----------|---------|
| `~/clawd/config/pipedream-credentials.json` | Encrypted credential storage |
| `~/clawd/config/mcporter.json` | MCP server configurations |
| `~/clawd/scripts/pipedream-token-refresh.py` | Token refresh script |
| `~/clawd/logs/pipedream-token-refresh.log` | Refresh logs |

### Backend Endpoints

The skill adds these gateway RPC methods:

| Method | Purpose |
|--------|---------|
| `pipedream.status` | Get connection status and configured apps |
| `pipedream.saveCredentials` | Validate and store credentials |
| `pipedream.getToken` | Get fresh access token |
| `pipedream.getConnectUrl` | Get OAuth URL for an app |
| `pipedream.connectApp` | Save app config to mcporter |
| `pipedream.disconnectApp` | Remove app from mcporter |
| `pipedream.refreshToken` | Update stored token |

### UI Components

The Pipedream page in the Clawdbot dashboard provides:

- Credential configuration form
- Connected apps list with test/disconnect buttons
- App browser with 100+ popular apps
- Manual app slug entry for any Pipedream-supported app

## App Slug Reference

Find app slugs at [mcp.pipedream.com](https://mcp.pipedream.com). Common ones:

| App | Slug |
|-----|------|
| Gmail | `gmail` |
| Google Calendar | `google-calendar` |
| Google Sheets | `google-sheets` |
| Google Drive | `google-drive` |
| Slack | `slack` |
| Discord | `discord` |
| GitHub | `github` |
| Notion | `notion` |
| Linear | `linear` |
| Airtable | `airtable` |
| OpenAI | `openai` |
| Stripe | `stripe` |

## Troubleshooting

### "No tools available"
- The OAuth flow wasn't completed. Click Connect again and complete the popup.
- Check Pipedream dashboard → Connect → Users to verify the app is linked.

### "Token expired" / 401 errors
- Run the token refresh script manually: `python3 ~/clawd/scripts/pipedream-token-refresh.py`
- Verify cron job is running: `crontab -l | grep pipedream`

### "Failed to fetch" / CORS errors
- Ensure you're running Clawdbot v2026.1.0+ with the Pipedream backend fixes
- All API calls should go through the gateway backend, not browser

### App not showing in Pipedream dashboard
- Use `google_calendar` (underscore) format for MCP calls
- UI uses `google-calendar` (hyphen), backend converts automatically

### OAuth popup blocked
- Allow popups for localhost:18789 in your browser
- Or copy the connect URL and open manually

## Multi-Agent Setup

Each agent can have their own connected accounts using different `externalUserId` values:

```
User ID: koda      → Apps connected for Koda
User ID: assistant → Apps connected for Assistant
```

Each creates separate mcporter server entries:
- `pipedream-koda-gmail`
- `pipedream-assistant-gmail`

## Development Notes

### Token Expiry

Pipedream access tokens expire after **1 hour**. The refresh script should run at least every 50 minutes.

### MCP Endpoint

All MCP calls go to `https://remote.mcp.pipedream.net` with headers:
- `Authorization: Bearer <access_token>`
- `x-pd-project-id: <project_id>`
- `x-pd-environment: development|production`
- `x-pd-external-user-id: <user_id>`
- `x-pd-app-slug: <app_slug>` (underscores, not hyphens)
- `Accept: application/json, text/event-stream`

### SSE Responses

The MCP endpoint may return Server-Sent Events format:
```
event: message
data: {"result":{"tools":[...]},"jsonrpc":"2.0","id":1}
```

Parse the `data:` line to extract JSON.

## Reference Files

This skill includes reference implementations:

- `reference/pipedream-backend.ts` — Gateway RPC handlers
- `reference/pipedream-controller.ts` — UI controller logic
- `reference/pipedream-views.ts` — UI rendering (Lit)
- `scripts/pipedream-token-refresh.py` — Token refresh script

These are for reference when building custom integrations or debugging.

## Support

- **Pipedream Docs**: [pipedream.com/docs](https://pipedream.com/docs)
- **MCP Apps**: [mcp.pipedream.com](https://mcp.pipedream.com)
- **Clawdbot Discord**: [discord.com/invite/clawd](https://discord.com/invite/clawd)
