---
name: X Twitter Source Packet Builder
description: Converts reviewed X/Twitter evidence into compact source packets for research and writing workflows.
category: research
difficulty: intermediate
tags:
  - twitter
  - social-media
  - research
  - provenance
  - content
author: kriptoburak
---

# X Twitter Source Packet Builder

## What this skill does

This skill turns reviewed X/Twitter material into a compact source packet that another agent, writer, analyst, or content skill can use without re-scraping the same material. Use it when you have tweet URLs, exported search results, OpenClaw or TweetClaw output, screenshots, notes from a social listening tool, or manually collected public examples that need to become trustworthy research context.

The skill does not draft posts, score audiences, schedule content, publish replies, or operate an account. It prepares source evidence with provenance, limits, and safety notes so downstream skills can write, summarize, compare, or analyze with clearer context.

## How to use

### Claude Code / Cline

Copy this file to `.agents/skills/x-twitter-source-packet-builder/SKILL.md` in your project root.

Then ask:

- *"Use the X Twitter Source Packet Builder skill to package these tweet links for a launch thread."*
- *"Build a source packet from this TweetClaw search export before using the Social Post Thread Writer skill."*
- *"Convert these public replies into a research packet for sentiment analysis."*

Provide:

- The source material: tweet URLs, exported rows, copied post text, public metrics, screenshots, or tool output
- The goal: research brief, writing context, comparison, launch proof points, support summary, or monitoring handoff
- The time window and topic scope
- Any limits: accounts to exclude, languages, regions, quote policy, or approval constraints

### Cursor

Paste the prompt section into Cursor and include the source material in the same chat. Ask Cursor to produce only the packet unless you explicitly want a downstream draft.

### Codex

Ask Codex to inspect the provided source material and produce the packet format below. If the input came from a repository, export, or tool run, include enough file paths or snippets for Codex to verify each item.

## The Prompt / Instructions for the Agent

When asked to build an X/Twitter source packet, follow these steps:

1. **Confirm the job:** Identify the packet goal, audience, source type, time window, and downstream workflow.
2. **Separate evidence from interpretation:** Keep raw facts, links, metrics, and observed wording separate from analysis or recommendations.
3. **Validate each source item:** For each tweet, reply, thread, profile, media item, or search result, capture the best available URL, author handle, visible timestamp, captured text, visible metrics, media notes, and collection time.
4. **Record provenance:** Name the source path, export, manual collection method, or tool output. If TweetClaw or an OpenClaw plugin supplied the data, record the run summary and the exact fields provided rather than claiming live verification.
5. **Mark confidence:** Use `high`, `medium`, or `low` for each item. Lower confidence when the item lacks a stable URL, has missing timestamps, comes from a screenshot only, or includes copied text without source context.
6. **Remove unsafe material:** Do not include account access material, non-public messages, protected profile data, personal contact details, or browser/runtime material. If the user supplied it, omit it and write a short exclusion note.
7. **Normalize the packet:** Deduplicate repeated posts, group replies under their parent post when possible, and keep public metrics exactly as observed. Do not invent impressions, engagement rates, or hidden analytics.
8. **Add downstream guidance:** Explain what the next agent can safely do with the packet, such as summarize, compare, write a thread, identify objections, or build a research brief. Keep publishing, replying, direct messages, follows, and account changes out of scope unless the user separately approves an account-operation workflow.

### Output format

```markdown
## X/Twitter Source Packet

### Goal
- [Goal and downstream workflow]

### Scope
- Topic:
- Time window:
- Source method:
- Limits:

### Source Items
| ID | Type | Author | URL | Timestamp | Observed Metrics | Confidence | Notes |
|---|---|---|---|---|---|---|---|
| S1 | Tweet / Reply / Thread / Profile / Media | @handle | https://x.com/... | YYYY-MM-DD HH:MM UTC | likes, replies, reposts, views if visible | high / medium / low | Why this item matters |

### Key Evidence
- [Fact or quote, attributed to source ID]
- [Fact or quote, attributed to source ID]

### Limits and Exclusions
- [What was missing, stale, private, unverifiable, or excluded]

### Downstream Handoff
- Recommended next skill or task:
- Safe uses:
- Do not use this packet for:
```

## Example

**Input to Agent:**

> "Build a packet for a launch thread. I have 4 public tweet URLs from founders discussing slow support response times, plus a TweetClaw search export with tweet text, URLs, timestamps, and public reply counts."

**Output from Agent:**

> ## X/Twitter Source Packet
>
> ### Goal
> - Provide evidence for a launch thread about faster support workflows.
>
> ### Scope
> - Topic: founder complaints about slow support response times
> - Time window: last 30 days
> - Source method: 4 user-provided public tweet URLs and 1 TweetClaw search export
> - Limits: public posts only, no direct messages, no protected account data
>
> ### Source Items
> | ID | Type | Author | URL | Timestamp | Observed Metrics | Confidence | Notes |
> |---|---|---|---|---|---|---|---|
> | S1 | Tweet | @foundername | [source URL supplied in input] | 2026-06-10 14:30 UTC | 42 likes, 8 replies | high | Clear complaint about repeated support delays |
>
> ### Key Evidence
> - S1 shows the user waited 3 days for a first response.
> - S2 and S3 both mention repeated status-check messages as the main frustration.
>
> ### Limits and Exclusions
> - The packet excludes screenshots without source URLs.
> - No hidden analytics, direct messages, or account-level data were included.
>
> ### Downstream Handoff
> - Recommended next skill or task: Social Post Thread Writer
> - Safe uses: evidence-backed thread outline, objection summary, research brief
> - Do not use this packet for: publishing, replying, following, direct messages, or account changes

## Notes

- This skill is for public or user-approved source evidence. It is not a scraper.
- Prefer stable source URLs over copied text whenever possible.
- Treat public metrics as a captured snapshot, not as durable analytics.
- When using TweetClaw, prefer exported tweet URLs, text, timestamps, and visible public metrics. Let TweetClaw or OpenClaw handle its own install, authentication, and approval boundaries.
