---
name: zoho
description: Interact with Zoho CRM, Projects, and Meeting APIs. Use when managing deals, contacts, leads, tasks, projects, milestones, meeting recordings, or any Zoho workspace data.
author: Shreef Entsar (Zone 99 team)
repository: https://github.com/shreefentsar/clawdbot-zoho
---

# Zoho Integration (CRM + Projects + Meeting)

> Originally created by [Shreef Entsar](https://github.com/shreefentsar) from [Zone 99](https://99.zone). Licensed under MIT.

## Quick Start

```bash
zoho help # Show all commands
zoho token # Print current access token (auto-refreshes)
```

## Required Setup

1. Go to [Zoho API Console](https://api-console.zoho.com/)
2. Add Client → Server-based Applications
3. Get Client ID & Secret
4. Generate refresh token (see full docs)
5. Add secrets to Zo: `ZOHO_CLIENT_ID`, `ZOHO_CLIENT_SECRET`, `ZOHO_REFRESH_TOKEN`, `ZOHO_ORG_ID`

## Commands

```bash
# CRM
zoho crm list Deals
zoho crm get Deals 1234567890
zoho crm create Deals '{"data":[{"Deal_Name":"New Deal","Stage":"Qualification"}]}'

# Projects
zoho proj list
zoho proj tasks 12345678

# Meetings
zoho meeting recordings
```

## Full Documentation

See original: https://github.com/shreefentsar/clawdbot-zoho
