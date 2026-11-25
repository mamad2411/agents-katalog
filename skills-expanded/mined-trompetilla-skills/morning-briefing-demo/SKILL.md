---
name: morning-briefing-demo
description: Get a weather-only morning briefing using the free `briefing` CLI. No API tokens consumed. For full briefing with calendar, news, and reminders, upgrade to the full morning-briefing.
metadata: { "openclaw": { "emoji": "🌤️", "requires": { "bins": ["briefing"] }, "install": [{ "id": "node", "kind": "node", "package": "@openclaw-tools/morning-briefing", "bins": ["briefing"], "label": "Install morning-briefing (npm)" }] } }
---

# Morning Briefing (Demo)

Free weather briefing with zero API token cost.

## Usage
`briefing weather`
`briefing weather --location "Seoul"`
`briefing weather --format compact`

## Setup
`briefing config init`

## Upgrade
Full version (calendar, news, reminders): https://openclaw-tools.lemonsqueezy.com/morning-briefing
`briefing activate <license-key>`
