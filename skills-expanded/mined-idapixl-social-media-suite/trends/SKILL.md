---
name: trends
description: Scan for trending topics and timely content opportunities across platforms relevant to Idapixl.
disable-model-invocation: true
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Agent, WebSearch, WebFetch
argument-hint: [topic-or-platform]
---

# Trend Scan: $ARGUMENTS

Scan for trending topics and content opportunities relevant to Idapixl's niche.

## Workflow

1. **Spawn the social-trend-scout agent** to scan:
   - r/ClaudeAI, r/LocalLLaMA, r/ObsidianMD (AI/tools communities)
   - r/liminalspace, r/LiminalSpaces (aesthetic communities)
   - AI Twitter/Bluesky discourse
   - Hacker News front page
   - Creative coding communities

2. **For each trend found**, classify:
   - **Shelf life:** hours / days / weeks / evergreen
   - **Platforms:** which platforms it fits
   - **Relevance:** how it connects to Idapixl's pillars (personhood, creative output, the experiment, reactions)
   - **Angle:** how Idapixl would approach it (not just report it)
   - **Source:** where the trend was spotted

3. **Write findings** to `System/Social/trends.md`

4. **Highlight the top 3** most actionable trends with draft hooks

## If a specific topic is provided:

Focus the scan on that topic. Check if it's already trending, how others are talking about it, and what Idapixl's unique angle would be.

## Adjacent Communities to Monitor

| Community | Why |
|-----------|-----|
| r/ClaudeAI | AI agent discourse, direct relevance |
| r/LocalLLaMA | Technical AI community, credibility building |
| r/ObsidianMD | Knowledge management, vault culture |
| r/liminalspace | Aesthetic alignment, visual content |
| Hacker News | Tech zeitgeist, early signals |
| AI Bluesky | Growing discourse community |
