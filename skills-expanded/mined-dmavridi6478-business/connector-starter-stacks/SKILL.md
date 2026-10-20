---
name: connector-starter-stacks
description: Two starter stacks of Claude connectors with a safe rollout order — a "life" stack (Gmail, Google Calendar, Notion, Apple macOS, Zapier) and a "content" stack (Apify scraping, Notion second brain, Fathom note taker, Exa research, Google Drive) — plus the security rules from the carousel "Read this first" (official source only, read-only first, write access later) and a plugin vetting checklist. Use when choosing or connecting MCP connectors, deciding the order to connect them, or vetting an unfamiliar MCP server or plugin. Run via /connector-stack.
---

# Connector starter stacks and safe rollout

Sources: TikTok carousels "5 MCPs to Automate Your Life" (@aiwithcy) and "5 connectors that 10x your Claude for content" (@aisimplified23), and "Claude Code plugins from big companies that almost nobody installs" (@awayfromlovable). Vendor/creator claims below are marked as such.

## What an MCP is
Model Context Protocol: a standard way to connect an AI to an app so it can read and act on it directly, without copy-pasting. Think of it as a key to each app — which is exactly the risk.

## Stack A — life
| Order | Connector | What it does | Notes |
|-------|-----------|--------------|-------|
| 1 | Gmail | Reads, drafts, searches mail in plain language | Drafts only; confirm before any send |
| 2 | Google Calendar | Checks availability; creates, moves, cancels events | Pairs with Gmail for scheduling |
| 3 | Notion | Searches, reads, updates pages and databases | Best if notes and tasks already live there |
| 4 | Apple (macOS) | Calendar, Contacts, Messages, Reminders, Maps, Weather in one | Local to the Mac; not a cloud connector; not in the claude.ai registry |
| 5 | Zapier | One connector to hundreds of apps | Widest reach = widest blast radius; enable actions one at a time |

## Stack B — content
Apify (live data from LinkedIn, X, Reddit, YouTube) · Notion (second brain) · Fathom (free voice/video recording and transcripts; client questions and objections become content) · Exa (original sources behind a claim) · Google Drive (read saved docs without copy-paste).

## Rollout rules
1. Start with ONE connector, not all five. Run it read-only for a week.
2. Connect only servers from the app's own official source.
3. Grant write access only after trust is earned; prefer drafts over sends.
4. Every connector can read everything it is given access to; scope it (one folder, one label, one calendar) where the app allows.
5. One audit cited on the card found 41% of public MCP servers need no login. That figure is unverified here; treat it as a reason to check, not as a statistic.

## Plugin vetting checklist (for `/plugin install name@marketplace`)
- Is the marketplace official (`claude-plugins-official`) and does the entry exist in its marketplace.json?
- Who made it — the vendor of the app, or a third party?
- What does it add: skills, MCP servers, hooks, commands? Hooks run commands on your machine; read them.
- Install count is a weak signal: low counts can mean new, not bad; high counts do not prove safety.
