---
name: webhook_manager
description: Manage Trello API webhooks across all boards from the ZINN Internal master card. Track webhook purpose, URLs, projects, and platforms. Use when Rob asks about webhooks, wants to register/list/delete webhooks, or audit old automation rules.
---

# Webhook Manager

Central registry for all Trello API webhooks. The source of truth is a master card on ZINN Internal > tech/production.

## Master Card

**Board:** ZINN Internal
**List:** tech/production
**Card:** [ZINN Webhooks](https://trello.com/c/w225DDuN/9673-zinn-webhooks)

Each webhook gets one section in the card description following ZINN_TRELLO_CARD_DATA_SCHEMA.md format:

```
##<webhook_name>

What its for: brief description of what the webhook communicates and why

url: the webhook callback URL

project: name of the skills, systems, or routines related to the webhook

Apps and Platforms: bulleted list of software/apps the webhook communicates between
```

## Current API Webhooks

| Count | Service | Boards | Callback URL |
|---|---|---|---|
| 4 | label-manager | Projects, ZPT2, Leads, Keynotes | `https://zinn-labels-production.up.railway.app/trello-webhook` |
| 5 | board-visualizer | ZINN projects, Chelsey's Wedding, temp, ORGANIZAÇÃO MARKETING MAX, Welxy commissions | `https://boardvisualizersyncserver-production.up.railway.app/trello-webhook` |

## Active Railway Services

| Service | URL | Purpose | Status |
|---|---|---|---|
| label-manager | `zinn-labels-production.up.railway.app` | Label sync + conflict enforcement | Active |
| board-visualizer-sync | `boardvisualizersyncserver-production.up.railway.app` | Board Visualizer checkitem sync | Active |
| project-setup | `project-setup-production.up.railway.app` | Phase transition / project setup | Active |
| zinn-proposals | `zinn-proposals-production.up.railway.app` | Proposal generation | 404 (needs review) |

## Management Scripts

### List all webhooks
```bash
python3 ~/.openclaw/skills/webhook_manager/scripts/list-webhooks.py
```

### Register a new webhook
```bash
python3 ~/.openclaw/skills/webhook_manager/scripts/register-webhook.py <boardId> <callbackURL> <description>
```

### Delete a webhook
```bash
python3 ~/.openclaw/skills/webhook_manager/scripts/delete-webhook.py <webhookId>
```

### Check webhook health
```bash
python3 ~/.openclaw/skills/webhook_manager/scripts/check-webhooks.py
```

## Old Butler Rules

See `old_trello_butler_rules.md` for inventory of Trello Automation rules that predate the API webhook system. These are visible only in the Trello UI under Automation > Rules per board.

## Credentials

- Trello API Key: `4a2c915a7c7943bee91cd872c9b1df0f`
- Trello Token: `~/.openclaw/credentials/trello-token.txt`
