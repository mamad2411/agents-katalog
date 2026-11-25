---
name: daily-debrief-alpha
description: Morning briefing pattern combining session rehash, tech news, and Polymarket alpha scanning
version: 1.0.0
category: productivity
license: MIT
platforms: [linux, macos]
tags: [briefing, polymarket, memory, morning-routine, alpha]
tested: schema-only
tested_note: Frontmatter and docs validated; runtime cron workflow not executed by this repo.
metadata:
  hermes:
    tags: [briefing, polymarket, memory, morning-routine, alpha]
    category: productivity
---

# Daily Debrief & Alpha — Morning Briefing Pattern

## What it is
A daily 08:30 AM cron job that delivers a high-signal, conversational briefing combining:
1. Session rehash from Holographic Memory
2. Technical news sweep
3. Polymarket "steal" identification

## Polymarket Scanning Approach
The briefing job uses the `polymarket` skill to scan for opportunities. Key search terms:
- Tech regulation, AI policy, crypto legislation
- Macroeconomic events, Fed decisions, inflation data
- Elections, geopolitical events with tech implications
- Major company earnings or product launches

## Finding "Steals"
A "steal" is a market where:
- The odds seem mispriced vs recent news/events
- High volume suggests liquidity but price hasn't adjusted yet
- There's a clear catalyst the market hasn't priced in

**Process:**
1. Search `gamma-api.polymarket.com` for relevant categories
2. Filter for markets with volume > $100K
3. Look for price anomalies (e.g., 80% No when news suggests 50/50)
4. Cross-reference with morning news to find unpriced events

## Tone Rules
- Conversational, like a sharp colleague texting you
- No headers, no bot-speak
- Bold only for specific prices/metrics
- Readable in ~30 seconds

## Cron Configuration
- Schedule: `30 8 * * *`
- Deliver: origin (back to Chief's chat)
- Enabled toolsets: web, terminal, file
- Skills: polymarket, kanban-orchestrator
- Model: qwen/qwen3.6-plus via Nous

## Reviewer's Role in Polymarket
The Reviewer profile (qwen/qwen3.6-plus) can be tasked with:
- Deeper analysis of Polymarket opportunities identified by the briefing
- Cross-referencing market odds with recent news
- Risk assessment of potential "steals"
- This is done via Kanban tasks, not automatically

## Holographic Memory Integration
The session rehash uses Holographic Memory's FTS5 + HRR algebra to:
- Find relevant work from last 24 hours
- Identify incomplete tasks or half-fixed bugs
- Provide context for today's priorities
