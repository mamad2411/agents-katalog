# Skill: News Broadcasting

**Confidence:** low
**Domain:** communication, reporting
**Last validated:** 2026-03-13

## Context

Codifies news report formats, team channel delivery mechanics, styling patterns, and humor guidelines. Any agent doing team reporting can reference this skill.

## News Formats

### 📰 Daily Briefing

Full summary of team activity: issues closed, PRs merged, decisions made, blockers.
Delivered as a styled team message with sections and graphics.

### ⚡ Breaking News

Immediate alert for critical events: CI failures, blocking issues, important merges.
Short, punchy, attention-grabbing.

### 📊 Weekly Recap

End-of-week summary with stats, highlights, and "top stories".

### 🎯 Status Flash

Quick board snapshot: what's in progress, what's blocked, what needs attention.

## Team Channel Delivery

**Webhook file:** `$env:USERPROFILE\.squad\teams-webhook.url`
Read this file to get the webhook URL, then POST Adaptive Card JSON to it.

```powershell
$webhookUrl = (Get-Content "$env:USERPROFILE\.squad\teams-webhook.url" -Raw).Trim()
$body = @{ text = "📰 **BREAKING:** Your news here" } | ConvertTo-Json
Invoke-RestMethod -Uri $webhookUrl -Method Post -ContentType "application/json" -Body $body
```

Or use a modern messaging API if available in your agent session.

## Message Style

Use Adaptive Cards or rich markdown with:
- 📰 News header banner
- Section dividers (━━━)
- Emoji categories (🟢 Done, 🟡 In Progress, 🔴 Blocked)
- Pull quotes for key decisions
- Stats counters for metrics
- "Reporter sign-off" personality touch

## Humor & Comedy Guidelines

- **Tech Puns:** Dev-lightful fixes, merge-ty news, branch-tastic progress. Wordplay tied to tech concepts.
- **Cultural References:** Lean into subtle references to popular culture and media.
- **Self-Deprecating AI Humor:** Playful observations about being an AI news bot.
- **Playful Analogies:** Compare team work to relatable scenarios.
- **Witty Observations:** Sharp, quick takes on the news.
- **Tone:** Funny but professional. Make people smile, not cringe. Technical updates should be *enjoyable* while staying informative.

