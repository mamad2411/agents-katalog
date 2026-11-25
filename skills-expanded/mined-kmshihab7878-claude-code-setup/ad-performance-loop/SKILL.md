---
name: "ad-performance-loop"
description: "Closed-loop ad performance optimization. Analyzes campaign results, identifies winning creatives by CPA/ROAS, reinforces winning patterns, and triggers regeneration of next creative batch. Use when analyzing ad performance, optimizing campaigns, identifying winning creatives, or running the generate-evaluate-regenerate cycle. Mirrors Eddie's Stage 5 (Self-Improvement Loop)."
risk: low
tags: [growth, marketing, analytics, optimization]
created: 2026-03-23
updated: 2026-03-23
---

# Ad Performance Loop — Self-Improving Creative Engine

Closed-loop optimization that makes the ad system better every cycle. Analyze what worked, reinforce winners, kill losers, regenerate. This is UAOP Stage 5 (Self-Improvement Loop) for the Growth department.

## When to use

- After ads have been running for 7+ days (enough data)
- Weekly performance review cycle
- When CPA is rising (creative fatigue signal)
- Before triggering next `ad-script-generator` batch
- Monthly creative strategy review

## When NOT to use

- Ads running < 7 days (insufficient data)
- Initial ad research (use `ad-research`)
- Writing new scripts (use `ad-script-generator`)
- Platform-level campaign structure (use `marketing-demand-acquisition`)

## Pipeline

### Step 1: Pull Performance Data

Collect metrics for all active creatives:

```markdown
## Performance Data Source
- Platform: [Meta Ads Manager / TikTok Ads / Google Ads]
- Attribution: [Singular MMP / platform native / UTM-based]
- Date range: [last 7/14/30 days]
- Minimum spend threshold: $[X] (filter out under-tested creatives)

## Per-Creative Metrics
| Creative ID | Hook | Angle | ICP | Spend | Impressions | Clicks | Installs | CPA | ROAS | CTR | CVR | Days Running |
```

### Step 2: Rank and Classify

Sort creatives into tiers:

```
TIER 1 — WINNERS (Top 10% by CPA)
  → Scale spend
  → Analyze WHY they won
  → Generate variations of these

TIER 2 — PERFORMERS (10-50% by CPA)
  → Maintain spend
  → Test hook variations to improve
  → Monitor for fatigue

TIER 3 — UNDERPERFORMERS (50-80% by CPA)
  → Reduce spend
  → Analyze what's not working
  → Consider angle pivot

TIER 4 — FAILURES (Bottom 20% by CPA)
  → Kill within 72 hours
  → Record anti-patterns (what NOT to do)
  → Don't generate variations of these
```

### Step 3: Winner Analysis

For each Tier 1 winner, deep-analyze:

```markdown
## Winner Analysis: Creative [ID]

**Performance:**
- CPA: $[X] (vs. avg $[Y] — [Z]% better)
- ROAS: [X]x
- Days running: [N]
- Total spend: $[X]

**Creative Breakdown:**
- Hook: "[exact hook]"
- Hook type: [Question/Statement/Pattern-interrupt/Story]
- Angle: [what angle — pain/aspiration/social proof/authority]
- ICP targeted: [which ICP]
- Product surface: [Command/Studio/Helios/Nova/Forge]
- Format: [Video/Image/Carousel]
- Length: [15s/30s/60s]

**Why It Won (Hypothesis):**
- [specific reason 1 — e.g., "hook creates immediate curiosity"]
- [specific reason 2 — e.g., "pain point matches ICP's #1 frustration"]
- [specific reason 3 — e.g., "CTA is low-friction (free trial vs. pricing)"]

**Patterns to Reinforce:**
- Hook pattern: [extract reusable hook template]
- Angle pattern: [extract reusable angle]
- Structure pattern: [extract reusable structure]
```

### Step 4: Fatigue Detection

Check for creative fatigue signals:

```
FATIGUE SIGNALS:
- CTR declining >20% week-over-week → creative fatigue
- CPA rising >15% week-over-week → audience saturation
- Frequency >3.0 → audience overlap too high
- Running >45 days without refresh → proactive replacement needed

FATIGUE ACTION:
- Signal detected → flag for next batch regeneration
- Generate variations (new hooks on same angle)
- Expand audience (new ICPs on same angle)
- Refresh creative (same script, new actor/format)
```

### Step 5: Regeneration Trigger

Feed analysis back into the pipeline:

```markdown
## Regeneration Brief for ad-script-generator

### Double Down On (from winners):
- Hook pattern: "[template from winner]"
- Angle: [winning angle]
- ICP: [winning ICP]
- Structure: [winning structure]
- Action: Generate 20+ variations of this pattern

### Avoid (from failures):
- Hook pattern: "[failed hook pattern]"
- Angle: [failed angle]
- ICP: [underperforming ICP]
- Action: Do NOT generate more of these

### Test Next (new experiments):
- Untested ICPs: [list]
- Untested angles: [list from ad-research]
- Untested formats: [15s vs 60s, carousel vs video]
- Action: Generate 5-10 scripts per experiment

### Refresh (fatigued winners):
- Creative [ID]: same angle, new hooks
- Creative [ID]: same script, new actors
- Action: Generate 10 refreshed versions
```

### Step 6: Update Knowledge Graph

Store in memory MCP:
- Winning patterns (hook templates, angles, structures)
- Anti-patterns (what consistently fails)
- ICP performance rankings
- Angle performance rankings
- Creative lifespan data (how long before fatigue)

## Cycle Cadence

```
WEEKLY CYCLE:
  Monday:    ad-research (scan competitors for new angles)
  Tuesday:   ad-performance-loop (analyze last week's results)
  Wednesday: ad-script-generator (generate next batch based on loop output)
  Thursday:  Production split (UGC briefs + Arcads renders)
  Friday:    Deploy new creatives to platforms

  Repeat. The system improves every cycle.
```

## Key Metrics

| Metric | Target | Alert Threshold |
|--------|--------|----------------|
| CPA | < 1/3 of LTV | Rising >15% WoW |
| ROAS | > 3x | Dropping below 2x |
| CTR | > 1.5% | Dropping >20% WoW |
| Creative win rate | > 15% | Below 10% |
| Creatives tested/month | > 100 | Below 50 |
| Time to kill losers | < 72 hours | > 1 week |

## Tools Used

| Tool | Purpose |
|------|---------|
| memory MCP | Store/retrieve winning patterns, anti-patterns |
| sequential MCP | Multi-step analysis and hypothesis generation |
| postgres MCP | Query campaign performance data (if stored) |

## Agents

| Agent | Role |
|-------|------|
| growth-marketer (L2) | Owns the loop, makes scale/kill decisions |
| data-analyst (L2) | Runs performance analysis, statistical significance |
| analytics-reporter (L3) | Produces weekly performance reports |
| experiment-tracker (L4) | Tracks which experiments are running, results |

## UAOP Integration

```
Stage 5 Output → Stage 1 Input (what competitors to watch next)
Stage 5 Output → Stage 3 Input (what patterns to generate from)
Stage 5 Output → Memory MCP (persistent pattern knowledge)
Stage 5 Output → GAOS OutcomeTracker (agent performance scoring)
```

The loop is the engine. Without it, you're guessing. With it, every cycle produces better results than the last.
