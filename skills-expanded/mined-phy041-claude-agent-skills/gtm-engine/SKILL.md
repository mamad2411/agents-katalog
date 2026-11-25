---
name: gtm-engine
description: Full go-to-market intelligence and outreach engine for founders. Monitors competitors on Reddit, finds high-intent leads across social platforms, and prepares warm outreach sequences. Triggers on "run gtm engine", "find leads", "competitive intel", "outreach pipeline".
inputs:
  - name: product_url
    type: string
    required: true
    description: Your product's website URL for auto-profiling
  - name: competitors
    type: list
    required: false
    description: Competitor names/URLs to track (auto-detected if omitted)
outputs:
  - name: competitive_intel
    type: json
    description: Competitor mention analysis from Reddit
  - name: leads
    type: list
    description: Scored leads ready for outreach review
  - name: outreach_drafts
    type: list
    description: Personalized outreach messages awaiting approval
---

# GTM Engine — Composite Skill

Combines brand monitoring, lead generation, and outreach preparation into one automated GTM loop.

## Architecture

```
brand-monitor        → Tracks competitor mentions + buyer signals on Reddit
    ↓ (parallel)
lead-generation      → Finds high-intent buyers across Twitter/Reddit/Instagram
    ↓
[merge + deduplicate signals]
    ↓
[score all leads 1-10]
    ↓
[prepare outreach drafts for warm leads ≥6]
    ↓
[send for human approval — NEVER auto-send]
```

## Feedback Loop

**Competitor Discovery**: brand-monitor results feed back to lead-generation. If brand-monitor finds a new competitor mentioned (one not in the original config), it's automatically added to lead-generation's query set.

## Step-by-Step

### Phase 1: Competitive Intel (brand-monitor)

Call `brand-monitor` for all configured competitors.

**Input →** brand names from config  
**Output →** alerts {subreddit, post_url, sentiment, intent, urgency}

Filter for buyer signals (intent = "buyer_signal" or competitor_comparison with negative sentiment toward competitor).

### Phase 2: Lead Discovery (lead-generation) [PARALLEL with Phase 1]

Call `lead-generation` with product profile.

**Input →** product_url (auto-profile) + competitor names from config  
**Output →** raw leads list {platform, username, post_text, url, posted_at}

### Phase 3: Merge + Score

Combine Phase 1 buyer signals + Phase 2 raw leads.

Deduplicate by `{platform}:{username}:{post_id}` against `data/lead-generation/sent-leads.json`.

Score each using rubric (see lead-generation skill). Filter: only keep score ≥ 6.

### Phase 4: Prepare Outreach

For each warm lead (score 6-7) and hot lead (score 8-10), draft a personalized outreach message:

- Warm: engage with their content first (like/reply)  
- Hot: direct DM draft

**NEVER send without human approval.**

### Phase 5: Report for Approval

```
🎯 GTM Engine — [date]

Competitive Intel:
  - [N] buyer signals on Reddit
  - Top: [subreddit] "[post title]" (score X)

Leads Found:
  - 🔴 [N] Hot leads (score 8-10)
  - 🟠 [N] Warm leads (score 6-7)

Top 3 Leads:
  1. @username | [platform] | Score: [X]/10
     "[post excerpt]"
     Outreach: "[draft]"

Reply "approve [1,2,3]" to queue these for sending, or "skip" to discard.
```

## I/O Contract Summary

| Phase | Skill Called | Key Input | Key Output |
|-------|-------------|-----------|------------|
| 1 | brand-monitor | competitor names | buyer_signals list |
| 2 | lead-generation | product_url | raw_leads list |
| 3 | (internal) | merged signals | scored_leads list |
| 4 | (internal) | scored_leads | outreach_drafts |
