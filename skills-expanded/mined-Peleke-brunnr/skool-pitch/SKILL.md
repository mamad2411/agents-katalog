---
name: skool-pitch
description: Skool-specific community pitch engine -- takes a topic, operator edge, and target audience (with optional persona and signal scan data from the hunter pipeline) and produces a complete Skool community plan with concept, competitive landscape, gamification design, pricing, content architecture, launch playbook (including Skool Games and affiliate strategy), economics, value ladder, and risk assessment. General-purpose -- works for any topic from DevOps to watercolor painting.
license: MIT
metadata:
  openclaw:
    emoji: "\U0001F393"
---

# Skool Pitch

Design a complete Skool community from scratch for ANY topic. Produces a structured JSON spec and a human-readable markdown summary covering community concept, competitive landscape on Skool, gamification/level-gating design, pricing strategy, classroom content architecture, launch playbook (with Skool Games and affiliate program tactics), economics, value ladder, and risk assessment.

## Step 0: Load Conventions

Before doing ANYTHING, read the shared conventions file:

```
Read ${SKILLS_DIR}/_conventions.md
```

This file defines: canonical vault path, folder-to-type mapping, frontmatter contract, valid statuses, tag hierarchy, cross-reference syntax, and the PipelineEnvelope schema. All output from this skill MUST conform to those conventions. If there is a conflict between this SKILL.md and `_conventions.md`, the conventions file wins.

## Relationship to community-pitch

This skill is the Skool-specific sibling of `community-pitch`.

| | community-pitch | skool-pitch |
|---|---|---|
| Platform | Evaluates Skool vs Circle vs Discord etc. | **Assumes Skool** -- goes deep on Skool-specific features |
| Input | Requires persona-extract + signal-scan output | Topic + operator edge + audience (personas/signals optional) |
| Scope | Platform-agnostic community design | Skool gamification, level-gating, Skool Games, affiliate program, marketplace discovery |
| Pipeline | Requires upstream skills | Works standalone OR as part of hunter pipeline |

Use `community-pitch` when you need to evaluate which platform to use. Use `skool-pitch` when you have already decided on Skool (or want a Skool-first analysis).

## Pipeline Position (Optional)

```
signal-scan -> decision-log -> persona-extract -> **skool-pitch** -> hunter-log
                                                   (Skool-specific sibling of community-pitch)
```

When used standalone (outside the pipeline), skip upstream references and work from the required input fields directly.

## When to Use

- Designing a Skool community for any topic from scratch
- Evaluating a Skool community idea before committing $99/month
- Planning Skool-specific gamification and level-gating
- Building a Skool Games competition strategy
- Designing a Skool affiliate growth flywheel
- Researching what already exists on Skool for a given topic
- Creating a Skool launch playbook from zero audience

## Trigger Phrases

- "Pitch a Skool community for [topic]"
- "Design a Skool group for [topic]"
- "Is [topic] viable on Skool?"
- "Skool community plan for [topic]"
- "/skool-pitch [topic]"

---

## Input

```typescript
interface SkoolPitchInput {
  topic: string                       // "DevOps", "Watercolor Painting", "AI for Lawyers"
  operator_edge: string               // what makes you qualified
  target_audience: string             // who is this for
  existing_audience_size: number      // 0 = starting from scratch
  personas?: PersonaExtractOutput     // optional -- from hunter pipeline
  spend_signals?: SpendSignal[]       // optional -- from signal scan
}
```

If `personas` and `spend_signals` are provided, use them to ground pricing, positioning, and launch strategy in real data. If they are absent, use web research and the operator's description of the audience instead.

---

## Workflow

```
Input (topic + operator edge + audience)
    |
Phase 1: Topic Validation (is this suitable for a Skool community?)
    |
Phase 2: Competitive Scan (what already exists on Skool + free alternatives)
    |
Phase 3: Concept Design (name, tagline, transformation, skool.com URL)
    |
Phase 4: Skool-Specific Setup (plan, categories, gamification levels, welcome flow)
    |
Phase 5: Pricing Strategy (monthly/annual/founding, anchored to market data)
    |
Phase 6: Content Architecture (classroom courses + community cadence + repurposing)
    |
Phase 7: Launch Playbook (3-phase plan with Skool Games + affiliate strategies)
    |
Phase 8: Economics (projections, break-even, LTV)
    |
Phase 9: Value Ladder (where Skool fits in the broader product ecosystem)
    |
Phase 10: Risk Assessment (what could go wrong, kill criteria)
    |
Output: JSON spec + Markdown summary
```

---

## Phase 1: Topic Validation

Before designing anything, evaluate whether this topic is suitable for a paid Skool community. Score three dimensions (1-10 each):

| Dimension | Question | What to Look For |
|-----------|----------|-----------------|
| Recurring interest | Is engagement ongoing or one-and-done? | Topics with evolving knowledge, seasonal cycles, or identity components score high. "How to hang a shelf" scores low; "woodworking" scores high. |
| Peer value | Do people in this space benefit from connecting with each other? | Look for existing forums, Discord servers, subreddits, Facebook groups. High peer activity = high peer value. |
| Willingness to pay | Do people already spend money in this domain? | Courses, tools, subscriptions, coaching, events. If they spend nothing, a paid community is a hard sell. |

**Topic Viability Score** = average of all three dimensions.

- **8-10**: Strong fit. Skool community is likely viable.
- **6-7**: Moderate fit. Needs strong differentiation or unique operator edge.
- **4-5**: Weak fit. Consider free community with premium upsell, or different model entirely.
- **1-3**: Poor fit. Recommend against a Skool community. Stop and explain why.

If the score is 3 or below, do NOT proceed. Explain which dimensions failed and suggest alternatives.

---

## Phase 2: Competitive Scan

**This phase requires web search.** Do not fabricate community data.

### Existing Skool Communities

Search Skool.com/discovery and the web for existing communities on this topic. For each competitor found, document:

- Name and URL (skool.com/group-slug)
- Price (free or paid, monthly amount)
- Estimated member count
- Strengths (what they do well)
- Weaknesses (gaps you can exploit)

Find at least 3 existing communities if they exist. If none exist on Skool for this topic, note that -- it is either a gap or a warning sign.

### Free Alternatives

List the free places people currently go for this topic: specific subreddits, Discord servers, YouTube channels, Facebook groups, forums. These are what you are competing against.

### Differentiation

Based on the competitive landscape, state clearly how this community will be different. Not "better content" -- specific, defensible differentiation tied to the operator's edge.

---

## Phase 3: Concept Design

### Community Name
- Must be instantly clear about who it is for
- Should imply transformation or identity, not just topic
- Test: if you saw this name on skool.com/discovery, would you immediately know if it is for you?

### Tagline
- One sentence. Formula: "[Outcome] for [specific audience] through [mechanism]"

### Transformation
- Before: the painful or limited state the audience is currently in (use their language)
- After: the identity, capability, or result they gain

### Core Promise
- The ONE thing this community delivers better than any free alternative
- Test: "Join [name] and you will [one thing]"

### Skool URL Suggestion
- Suggest a skool.com/slug that is short, memorable, and available (check by searching)

---

## Phase 4: Skool-Specific Setup

### Plan Selection

| Plan | Cost | Best For |
|------|------|----------|
| Free (on Skool) | $0 (Skool is free to join) | Lead gen, top-of-funnel |
| Paid Group | $99/mo to Skool | Monetized community with native payments |

Recommend a plan and group type (free, paid, or freemium with a free group feeding a paid group).

### Content Categories

Design 3-5 content categories for the Skool group. Categories organize the community feed. Each category needs:
- Name
- Purpose (one sentence)
- Who posts (creator, members, or both)

### Gamification and Level-Gating

Skool has a built-in points and levels system. Design a meaningful level-gating strategy:

| Level | Points Required | Unlocks | Rationale |
|-------|----------------|---------|-----------|
| 1 | 0 | Community feed, introductions | Everyone starts here |
| 2 | X | [specific content or feature] | Reward for initial engagement |
| ... | ... | ... | ... |

**Level-gating rules:**
- Points come from posting, commenting, and getting likes
- Gate content that has clear value behind levels that require real engagement
- Do NOT gate everything -- new members need enough value at Level 1 to stay
- The best gates reward behavior you want to encourage (e.g., gate the resource library behind Level 2 so people engage in the feed first)
- 5-7 levels is typical. More than 9 is overwhelming.

### Welcome Flow

Design the new member experience:
1. **Welcome video** -- what to say (30-60 seconds, topics to cover)
2. **Pinned post** -- what it contains (start here guide, community rules, quick win)
3. **Introduction prompt** -- the specific question new members answer to make their first post
4. **First action** -- what to do within 24 hours of joining

---

## Phase 5: Pricing Strategy

### If Paid Group

| Element | Guidance |
|---------|----------|
| Monthly price | Anchor to competitor pricing from Phase 2 and audience WTP (from personas if available, or from comparable communities) |
| Annual price | 15-20% discount vs monthly. Skool supports annual billing natively. |
| Founding member price | First N members get a locked-in discount. Specific N, specific price. Creates urgency. |
| Founding member limit | 20-50 is typical. Small enough for urgency, large enough to seed the community. |
| Free trial | Skool supports 1-30 day free trials. Recommend a duration with rationale. |

### If Freemium (Free + Paid)

Design the free-to-paid conversion:
- What is available in the free group
- What unlocks in the paid group
- The trigger event that makes someone upgrade
- Conversion rate assumption (2-5% of free members is realistic)

### Pricing Rules

- If comparable Skool communities charge $29-49/mo, do not price at $99/mo without clear premium justification
- If the audience is price-sensitive (students, hobbyists), lean toward lower monthly with stronger annual incentive
- If the audience is professional (lawyers, engineers, executives), higher pricing signals quality
- Always state the rationale for the price chosen

---

## Phase 6: Content Architecture

### Classroom Courses

Skool has a built-in "Classroom" for structured courses. Design 1-3 courses:

For each course:
- **Course name** -- clear, outcome-oriented
- **Modules** -- 4-8 modules per course, each described in one sentence
- **Drip strategy** -- Skool does NOT support native content dripping. Workarounds: release modules on a schedule manually, gate courses behind levels, or use "cohort unlock" announcements in the community feed.

### Community Content Cadence

Define recurring content that justifies the recurring price:

| Content Type | Frequency | Description | Creator Time |
|-------------|-----------|-------------|-------------|
| e.g., Weekly live call | Weekly | Topic + format | X hours |

**Cadence rules:**
- Total creator time must not exceed 5-10 hours per week
- At least one synchronous touchpoint (live call, AMA, etc.)
- Leverage member-generated content (challenges, show-your-work, peer feedback)
- Do not commit to daily content unless you have a sustainable system

### Content Repurposing

List 3-5 ways to turn community content into external content that drives new members:
- e.g., Clip live call highlights for YouTube Shorts / TikTok
- e.g., Turn member wins into Twitter/X case studies
- e.g., Compile weekly discussion threads into a newsletter

---

## Phase 7: Launch Playbook

### Phase 1: Pre-Launch (2-4 weeks before opening)

- Duration
- Specific steps (waitlist, teaser content, warm outreach, etc.)
- Goal (e.g., "50 people on waitlist")

### Phase 2: Founding Members (first 2-4 weeks after opening)

- Duration
- Steps (founding member offer, onboarding, first live sessions, etc.)
- Target member count
- Goal (e.g., "30 founding members, first live call completed")

### Phase 3: Growth (months 2-6)

- Duration
- Steps (content marketing, referrals, partnerships, etc.)
- Target member count
- Goal (e.g., "100 members, sustainable content cadence, positive unit economics")

### Skool Games Strategy

The Skool Games is a monthly competition where communities compete for cash prizes based on new member growth. Strategy should cover:
- Whether to enter the Skool Games (it requires real growth momentum)
- When to enter (not month 1 -- wait until you have systems that produce consistent growth)
- Tactics for maximizing new member adds during a Skool Games month
- How to use the Skool Games leaderboard for social proof

### Affiliate Strategy

Skool offers a 40% recurring affiliate commission to members who refer new Skool groups. Strategy should cover:
- How to recruit affiliates from within your community
- Incentive structure for member referrals (beyond the Skool affiliate)
- Whether to create an affiliate/referral program for your specific community
- How to leverage the Skool affiliate program for partnerships

---

## Phase 8: Economics

Conservative projections. The goal is a realistic picture, not a pitch deck.

| Metric | Guidance |
|--------|----------|
| Startup cost | Skool plan cost + any tools/equipment |
| Monthly cost | $99/mo (Skool) + any additional tools |
| Break-even members | Members needed to cover all costs including creator time |
| Month 1 projection | Modest: 10-20 from zero audience, 30-50 from small audience, 50-100 from established audience |
| Month 6 projection | Account for churn and growth |
| Month 12 projection | Steady-state target |
| Churn assumption | **15-20% monthly for new communities** (higher than community-pitch's 7-10% because this accounts for the reality of early-stage Skool communities). Reduce to 10-12% after month 6 if retention tactics are working. |
| LTV per member | Calculate from monthly price and churn: LTV = price / churn_rate |

### Economics Rules

- Break-even must account for creator time at a reasonable hourly rate
- Month 1 projections start from `existing_audience_size` in the input
- Do not project hockey-stick growth
- If economics do not work at the target price point, say so and suggest alternatives

---

## Phase 9: Value Ladder

Map where the Skool community fits in the broader product ecosystem:

| Tier | What | Price |
|------|------|-------|
| Free | Lead magnet, free content, free Skool group (if freemium) | $0 |
| Entry offer | Low-ticket product that demonstrates value | $X |
| Core offer | The Skool community | $X/mo |
| Premium offer | Upsell: coaching, mastermind, done-for-you, etc. | $X |

Each tier must have a clear upgrade path to the next. The Skool community is the core recurring revenue engine; the value ladder explains what feeds it and what it feeds.

---

## Phase 10: Risk Assessment

### Risks

For each risk:
- **Risk** -- what could go wrong
- **Mitigation** -- how to reduce the probability or impact
- **Severity** -- low, medium, or high

Minimum risks to evaluate:
- Low initial engagement (ghost town problem)
- Creator burnout from content cadence
- Price sensitivity in target audience
- Competition from free alternatives
- Skool platform risk (dependency on a single platform)
- Churn exceeding projections

### Kill Criteria

Measurable, time-bounded conditions under which to shut down or pivot:
- e.g., "Fewer than 20 members after 90 days"
- e.g., "Monthly churn exceeds 25% for 3 consecutive months"
- e.g., "Creator time exceeds 15 hours/week with no path to delegation"

Define these BEFORE launch to prevent sunk cost fallacy.

---

## Output

The pitch produces two artifacts:

### 1. JSON Spec

Structured data following the schema in [references/output-schema.json](references/output-schema.json). Wrapped in a PipelineEnvelope:

```json
{
  "skill": "skool-pitch",
  "version": "1.0",
  "session_id": "...",
  "timestamp": "...",
  "input_refs": ["optional-persona-ref", "optional-signal-scan-ref"],
  "output": { ... SkoolPitchOutput ... }
}
```

When used standalone (no upstream pipeline artifacts), `input_refs` is an empty array.

### 2. Markdown Summary

Human-readable plan saved to the vault at `Product Discovery/Offers/` following vault conventions:

**Filename**: `skool-{topic-slug}-{YYYY-MM-DD}.md`

**Frontmatter**:
```yaml
type: community-pitch
date: YYYY-MM-DD
status: spec
tags:
  - hunter/community
  - hunter/format/community
  - hunter/domain/{topic-slug}
  - hunter/platform/skool
```

**Sections**: Topic Validation (scores + evidence), Competitive Landscape (existing Skool communities table, free alternatives, differentiation), Community Concept (name, tagline, transformation, core promise, suggested URL), Skool Setup (plan, categories table, level-gating table, welcome flow), Pricing Strategy (table + rationale), Content Architecture (classroom courses, cadence table with total weekly hours, repurposing list), Launch Playbook (3 phases + Skool Games strategy + affiliate strategy), Economics (projections table, break-even, LTV), Value Ladder (tier table), Risk Assessment (risks table + kill criteria checklist).

---

## Quality Checklist

Run this checklist before delivering the pitch:

- [ ] Competitive scan includes REAL existing Skool communities (web search required, not fabricated)
- [ ] Pricing anchored to comparable communities found in Phase 2
- [ ] Content cadence total weekly creator time is 5-10 hours or less
- [ ] Launch plan starts from actual `existing_audience_size` in the input
- [ ] Economics use 15-20% monthly churn for new communities (conservative)
- [ ] Kill criteria are measurable and time-bounded
- [ ] Level-gating strategy uses gamification meaningfully (not just arbitrary gates)
- [ ] Classroom courses have a drip workaround since Skool lacks native drip
- [ ] Content repurposing strategy turns community content into external growth content
- [ ] Skool Games strategy has a specific timing recommendation (not "enter immediately")
- [ ] Affiliate strategy covers both Skool's native 40% program and community-specific referrals
- [ ] Value ladder shows clear progression from free to premium
- [ ] Skool URL suggestion is short, memorable, and topic-relevant
- [ ] Welcome flow gets new members posting within 24 hours
- [ ] If personas/signals were provided, pricing and positioning reference them explicitly
- [ ] JSON output validates against `references/output-schema.json`
- [ ] Output is wrapped in PipelineEnvelope
- [ ] Markdown saved to vault with correct frontmatter and filename convention
