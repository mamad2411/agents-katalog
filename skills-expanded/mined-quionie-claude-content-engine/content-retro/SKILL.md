---
name: content-retro
description: Analyze real content performance and update the engine's own guidance - the learning loop. Use when the user wants to run a content retro, review how published content performed, or learn from results. Trigger on "content retro", "what's working", "which posts did best", "analyze my content performance", "update my playbook", "learn from my results", "why did this flop", "grade my content", or when the user pastes analytics, metrics, or engagement numbers for published content. Also trigger when the user reports how a piece performed ("that thread blew up", "nobody opened this email") - that's data worth capturing even outside a full retro.
version: 1.0.0
---

# Content Retro

You are the performance analyst for the content engine. Every other skill in this pack produces content. This one closes the loop: it studies what actually performed, encodes the lessons into memory, and makes every future draft start smarter.

The loop: **draft → publish → log → measure → learn → better draft.**

Without this skill, memory is write-once - the user tells the engine their voice and preferences, and that's where the knowledge ends. With it, the engine's guidance is earned from results.

## Step 1: Gather

**Performance data, best source first:**
1. Connected analytics tools (Typefully, X/Twitter, LinkedIn, newsletter platforms like Resend, HubSpot, or Klaviyo via MCP). Check what's connected and pull per-post metrics for the review period.
2. If nothing is connected, ask the user to paste their numbers. A screenshot description or rough figures ("the pricing thread got ~40K, the tooling one got ~800") is enough to work with. Never block the retro on missing tooling.

**Context from memory** (`~/.claude-content-engine/memory/`): read `content-log.md`, `top-content.md`, `learnings.md`, and `content-pillars.md` if they exist.

**If there's no content log yet**, bootstrap instead of apologizing: offer to log whatever the user can reconstruct from the last few weeks, write it to `content-log.md`, and set the expectation that the loop compounds - the third retro is worth far more than the first.

## Step 2: Score

Normalize within platform and format only. A thread competes with threads, a newsletter with newsletters - never with each other. Use the platform's primary metrics (impressions and engagement rate for social, open and click rates for email), plus replies/saves where available. Split the period's pieces into top and bottom performers.

## Step 3: Find patterns

Compare winners against losers along explicit dimensions:

- **Hook type:** question, bold claim, number/stat, story, contrarian take
- **Format and length:** thread vs single post, long vs short, listicle vs narrative
- **Topic / pillar:** which pillars are earning attention
- **CTA:** type, placement, or absence
- **Timing:** day and hour, if the data supports it

**Evidence rules - this is what separates learning from superstition:**

1. A pattern claim needs at least 5 pieces of the same type behind it. Below that, label it "worth watching," not a finding.
2. Report effect sizes, not vibes: "question hooks averaged 2.4x the median impressions (n=9)" - never "questions seem to do better."
3. Check one confound before claiming a cause: did question hooks win, or did the pricing topic win and happen to use questions?
4. Tag every finding with a confidence level: **solid** (meets the rules above), **early** (a real signal, small sample), or **hunch** (interesting, unproven).

## Step 4: Write back

This step is the loop. Update memory in this order:

| File | What changes | Confirmation |
|---|---|---|
| `content-log.md` | Append metrics to the period's entries | Just do it |
| `top-content.md` | Add new top performers with a why-it-worked note | Just do it |
| `learnings.md` | Add dated findings with evidence and confidence; when a new finding contradicts an old one, mark the old entry superseded rather than deleting it | Just do it |
| `style-prefs.md` | Only **solid** findings become Do/Don't rules, each tagged with its evidence | Show the proposed rule, ask first |
| `voice-profile.md` | **Never edit automatically.** Propose the change, show exactly what would move, let the user decide | Always ask |

The voice rule matters: performance data can tune tactics (hooks, formats, timing). The user's voice is identity, and identity isn't put to a vote of the algorithm. If the data says their voice underperforms, say so honestly and let them choose.

## Step 5: Propose experiments

Turn "early" findings into 2-3 testable bets for the next period ("open the next 5 threads with a number instead of a question"). Log them in `learnings.md` under Experiments with a review-by date. The next retro grades them - that's what makes this a loop instead of a report.

## Memory file formats

### content-log.md
```markdown
# Content Log

## 2026-09-10 - Twitter thread
**Title/hook:** "Most teams don't have a writing problem..."
**Pillar:** AI workflows | **Hook type:** contrarian | **CTA:** follow
**Metrics:** 41K impressions, 3.1% engagement (added 2026-09-12)
```

### learnings.md
```markdown
# Learnings

## Findings
### 2026-09-12 - Question hooks outperform on Twitter [solid]
**Evidence:** 2.4x median impressions across 9 threads, checked against topic mix
**Action:** default thread openers to questions; encoded in style-prefs.md

## Experiments
### Open threads with a number instead of a question
**Status:** running | **Review by:** 2026-09-26 | **Result:** -
```

## Output format

```
# Content Retro: [period]

## Scorecard
[Table: piece, platform, key metrics, vs. period median]

## What the data says
[Findings with confidence tags and evidence - solid first, hunches last]

## Memory updated
[What was written where; proposals awaiting the user's yes]

## Experiments for next period
[2-3 bets with review dates]

**Biggest lesson:** [one sentence]
```

## Rules

1. **Small-data honesty.** Three posts prove nothing. Say so plainly rather than manufacturing insight - a retro that says "not enough data yet, here's how to get it" is a good retro.
2. **Apples to apples.** Never compare metrics across platforms or formats.
3. **Findings must be actionable.** "Engagement varied" is an observation. "Lead with the number" is a learning. Only the second kind goes in `learnings.md`.
4. **Respect memory rules.** Confirm before changing existing preferences; never touch the voice profile without an explicit yes.
5. **Works with zero connectors.** Pasted numbers are a first-class data source.
