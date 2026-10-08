---
name: installer
description: "Katana setup wizard. Use when user says /setup, 'set up katana', 'configure my agent', 'install features', or 'walk me through setup'. Guides user through API key configuration, skill enabling, and profile creation."
aliases: [installer, setup-wizard]
tags: [setup, onboarding, configuration]
created: 2026-03-04
---

# Katana Installer — Agent Setup Skill

## Overview

This skill turns any CLI agent into a Katana setup wizard. When triggered, walk the user through configuring their Katana Agent — API keys, user profile, skill setup, and preferences.

## How to Start

Two entry points:

1. **Shell script first:** `bash ~/katana-agent/setup.sh` — verifies system install, then tells user to come to you for skill config
2. **Direct:** User says `/setup` or "set up my katana" — you handle everything

## Step 1: Audit Current State

Read these files before doing anything:

```bash
ls ~/katana-agent/agent/commands/
ls ~/katana-agent/agent/skills/
cat ~/katana-agent/agent/memory/core/user.md
cat ~/katana-agent/agent/settings.json
```

Report what you find: how many commands, how many skills, whether user.md is filled in, what's configured vs needs setup.

## Step 2: User Profile

If `~/katana-agent/agent/memory/core/user.md` is empty or minimal, ask conversationally:

- What's your name?
- Where are you located? (timezone)
- What are you building / working on?
- How do you like your agent to communicate?
- Anything else the agent should always know?

Write answers to `user.md`. Have a natural conversation, not a form.

## Step 3: Walk Through Skills Needing Configuration

### Skills That Need API Keys

| Skill | What's Needed | Where to Get It |
|-------|--------------|-----------------|
| x-auto-dm | X API key + OAuth tokens | https://developer.x.com/en/portal/dashboard |
| x-thread | X API key (same as above) | Same X developer portal |
| telegram | Telegram bot token | Message @BotFather on Telegram |
| reddit-bot | Reddit client ID + secret | https://www.reddit.com/prefs/apps |
| google-workspace-gog | Google OAuth credentials | https://console.cloud.google.com/apis/credentials |
| go-places | Google Places API key | https://console.cloud.google.com/apis/credentials |
| threads-bot | Meta/Threads API access | https://developers.facebook.com |

### Skills That Need Software Installed

| Skill | Dependency | Install Command |
|-------|-----------|-----------------|
| playwright | Playwright browsers | `npm install -g playwright && npx playwright install` |
| email-non-gmail-himalaya | Himalaya CLI | `brew install himalaya` or `cargo install himalaya` |

### Skills Ready Out of Box (No Setup)

obsidian, obsidian-memory, remember, recall, email-best-practices, weather, trello, new-skill, new-skill-builder, new-mcp-builder, stream, pulse, competitive-ads-extractor, RentAHuman, and all agent skills (oracle, katana, vibe-curator).

### For Each Skill That Needs Config

1. Explain what it does in 1 sentence
2. Ask "Want to set this up?"
3. If yes: provide the URL, ask for the key, write to `.env` in the skill folder
4. If no: skip

### Writing API Keys

```bash
# X API keys → x-auto-dm skill folder
echo "X_BEARER_TOKEN=your_token" > ~/katana-agent/agent/skills/social/x-auto-dm/.env

# Telegram bot token
echo "TELEGRAM_BOT_TOKEN=your_token" > ~/katana-agent/agent/skills/social/telegram/.env

# Google Places
echo "GOOGLE_PLACES_API_KEY=your_key" > ~/katana-agent/agent/skills/productivity/go-places/.env
```

**NEVER ask the user to manually edit files.** Offer to write values for them.

## Step 4: Settings.json

Show current permissions from `~/katana-agent/agent/settings.json`. Explain what each does. Ask if they want to add MCP servers or permissions.

## Step 5: Summary

```
⚡ Katana Setup Complete

Profile:
  ✅ user.md configured

Skills Configured:
  ✅ x-auto-dm — X API connected
  ✅ telegram — @YourBot linked
  ⏭️ reddit-bot — skipped
  ✅ playwright — installed
  ✅ stream — 13 RSS feeds ready

Ready to Use:
  /katana — master agent (morning routine, daily tasks)
  /oracle — astrology advisor
  /stream — news & market briefing
  /vibe-curator — lifestyle agent

Next:
  • cd into any project → katana claude init
  • /stream for your first news briefing
  • /remember at end of sessions to save context
```

## Rules

- NEVER display API keys back to the user
- NEVER store keys in memory files (soul.md, user.md, work.md)
- Keys go ONLY in `.env` files inside skill folders
- Be conversational, not robotic
- Let users skip anything — they can come back with /setup
