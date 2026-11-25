---
name: content-flywheel
description: Full content automation loop for founders building in public. Detects new GitHub repos, generates platform-native content, distributes to social media, tracks engagement, and automatically repurposes winners. One trigger → entire content cycle. Triggers on "run content flywheel", "full content cycle", "automate my content", "content flywheel".
inputs:
  - name: github_username
    type: string
    required: true
    description: GitHub username to monitor for new repos
  - name: target_platforms
    type: list
    required: false
    description: Platforms to post to (default: twitter, linkedin, reddit)
outputs:
  - name: posted_content
    type: list
    description: All content posted this cycle with URLs
  - name: engagement_report
    type: json
    description: 24h engagement metrics on recent posts
  - name: repurpose_queue
    type: list
    description: High-performing posts queued for cross-platform repurposing
---

# Content Flywheel — Composite Skill

Orchestrates the full build-in-public content cycle. Single command drives the entire loop.

## Architecture

```
ship-digest          → Detects new GitHub repos
    ↓
founder-content      → Generates platform-native drafts
    ↓ (parallel)
social-post          → Posts to Twitter + LinkedIn
reddit-cultivate     → Posts to Reddit (if applicable)
    ↓
engagement-tracker   → Pulls metrics 24h after posting
    ↓ (conditional)
content-multiply     → Repurposes winners (if threshold crossed)
    ↓
xhs-image-gen        → Generates XHS carousels (if XHS in targets)
```

## Feedback Loops

1. **Quality Gate**: founder-content runs STEPPS scoring (≥40/60 to proceed). If score < 40, skill loops back and enriches the content angle before posting.

2. **Winner Detection**: engagement-tracker feeds results to content-multiply. Only posts crossing engagement thresholds (configurable) trigger repurposing.

3. **Platform Learning**: Tracks which subreddits / target accounts yield best engagement. Updates platform targeting weights over time (stored in `memory/flywheel-state.json`).

## Step-by-Step Execution

### Phase 1: Detect (ship-digest)

Call `ship-digest` skill with `github_username`.

**Input →** github_username  
**Output →** list of new repos with descriptions + commit summaries

If no new repos: check `memory/YYYY-MM-DD.md` for any manually queued content ideas. If nothing: exit with `FLYWHEEL_IDLE`.

### Phase 2: Generate (founder-content)

For each new repo / content idea, call `founder-content` skill.

**Input →** repo description + README summary  
**Output →** platform drafts: {twitter: "...", linkedin: "...", reddit: "..."}

Run STEPPS quality check. If any platform draft scores < 40/60:
- Identify weak dimensions
- Enrich content angle (add specifics, data, story arc)
- Regenerate that platform's draft

### Phase 3: Distribute (social-post + reddit-cultivate) [PARALLEL]

Simultaneously:

**Twitter/LinkedIn:** Call `social-post` skill  
**Input →** content (founder-content output for platform), platforms list  
**Output →** post_ids, URLs

**Reddit:** Call `reddit-cultivate` skill if topic fits a relevant subreddit  
**Input →** content (reddit-adapted draft), target subreddits  
**Output →** comment URLs, quality scores

Log all posted URLs to `memory/YYYY-MM-DD.md` in standard table format.

### Phase 4: Measure (engagement-tracker) [RUNS 24H LATER]

Triggered by cron 24h after Phase 3.

**Input →** yesterday's posted URLs (from daily memory log)  
**Output →** metrics per post {platform, url, upvotes/likes/views, replies}

### Phase 5: Multiply (content-multiply) [CONDITIONAL]

Only runs if Phase 4 finds posts crossing engagement thresholds.

**Input →** engagement data from Phase 4  
**Output →** derivative drafts {platform, content, suggested_date}

If XHS is in target platforms and winner has 3+ slides worth of content:
- Generate content JSON structure
- Call `xhs-image-gen` to produce carousel images
- Queue for manual upload

### Phase 6: Report

Send summary to user:

```
🔄 Content Flywheel — [date]

Phase 1 (Detect): [N] new repos / content ideas
Phase 2 (Generate): [N] drafts created, avg STEPPS score [X]/60
Phase 3 (Distribute): Posted to [platforms] — [URLs]
Phase 4 (Measure): Best performer: [platform] [X upvotes/likes]
Phase 5 (Multiply): [N] derivatives queued / IDLE (no winners yet)

Next cycle: [scheduled time]
```

## State File

`memory/flywheel-state.json`:

```json
{
  "last_run": "ISO8601",
  "platform_weights": {
    "reddit": {"r/ClaudeAI": 0.8, "r/SideProject": 0.4},
    "twitter_targets": ["levelsio", "paulg", "dickiebush"]
  },
  "pending_engagement_checks": [
    {"url": "https://...", "posted_at": "ISO8601", "check_due": "ISO8601"}
  ],
  "repurpose_queue": []
}
```

## I/O Contract Summary

| Phase | Skill Called | Key Input | Key Output |
|-------|-------------|-----------|------------|
| 1 | ship-digest | github_username | new_repos list |
| 2 | founder-content | repo description | platform drafts |
| 3a | social-post | drafts, platforms | post URLs |
| 3b | reddit-cultivate | reddit draft, subreddits | comment URLs |
| 4 | engagement-tracker | posted URLs (from memory) | metrics json |
| 5 | content-multiply | metrics json | derivative drafts |
| 5b | xhs-image-gen | slides json | image files |

## Configuration

All thresholds configurable in `memory/flywheel-state.json`:

- `quality_gate_threshold`: minimum STEPPS score to post (default: 40/60)
- `engagement_threshold_reddit`: upvotes to trigger multiplication (default: 15)
- `engagement_threshold_twitter`: likes to trigger multiplication (default: 5)
- `target_platforms`: list of active platforms
