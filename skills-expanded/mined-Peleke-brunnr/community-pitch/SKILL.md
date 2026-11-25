---
name: community-pitch
description: Community pitch engine -- takes persona extraction output and signal scan data, then produces a complete paid community plan with concept, platform recommendation, membership tiers, content cadence, launch plan, economics, community structure, and bundling strategy. Use when converting validated persona insights into a recurring-revenue community business (primarily Skool, but platform-agnostic).
license: MIT
metadata:
  openclaw:
    emoji: "\U0001F3D8\uFE0F"
---

# Community Pitch

Transform persona extraction output and signal scan data into a complete paid community plan. Produces a structured JSON spec and a human-readable markdown summary with community concept, platform recommendation, membership tiers, content cadence, launch plan, economics, community structure, bundling strategy, and kill criteria -- all grounded in persona data and market signals.

## Step 0: Load Conventions

Before doing ANYTHING, read the shared conventions file:

```
Read ${SKILLS_DIR}/_conventions.md
```

This file defines: canonical vault path, folder-to-type mapping, frontmatter contract, valid statuses, tag hierarchy, cross-reference syntax, and the PipelineEnvelope schema. All output from this skill MUST conform to those conventions. If there is a conflict between this SKILL.md and `_conventions.md`, the conventions file wins.

## Pipeline Position

```
signal-scan -> decision-log -> persona-extract -> **community-pitch** -> hunter-log
                                                   (sibling of offer-scope)
```

This skill consumes the output of `persona-extract` and `signal-scan`, and feeds into `hunter-log` for execution tracking. It runs parallel to `offer-scope` -- where offer-scope produces a one-time product spec, community-pitch produces a recurring-revenue community plan.

## When to Use

- Converting validated persona insights into a paid community plan
- Evaluating whether a domain supports a recurring community model
- Designing a Skool (or comparable platform) community from scratch
- Creating a membership pricing model anchored to WTP data
- Planning a community launch from zero audience
- Building a recurring revenue complement to one-time products from offer-scope

## Trigger Phrases

- "Pitch a community for [domain]"
- "Design a paid community from this persona data"
- "Should I build a community for [domain]?"
- "Community plan for [persona]"
- "Skool community for [domain]"
- "/community-pitch [persona-extract output]"

---

## Prerequisites

Before starting, the following must be available:

1. **Persona extraction output** -- A completed persona-extract result containing: persona names, pain stories (with situation/pain/emotional state), decision triggers, willingness-to-pay data, and channel behavior
2. **Signal scan data** -- SPEND signals and COMPETITIVE signals from a completed signal-scan, plus the meta-signal
3. **Domain and opportunity** -- The specific domain and opportunity area being targeted

If any of these are missing, prompt the user to run the upstream skill first or provide the data manually.

---

## Input

The skill expects the following input structure (typically assembled from upstream skill outputs):

```typescript
interface CommunityPitchInput {
  personas: {
    persona_name: string
    pain_stories: { situation: string, pain: string, emotional_state: string }[]
    decision_triggers: { trigger: string, urgency: string }[]
    willingness_to_pay: { range: string, evidence: string }
    channels: { platform: string, behavior: string }[]
  }[]
  domain: string
  opportunity: string
  spend_signals: { signal: string, price_range: string, platform: string }[]
  competitive_signals: { signal: string, type: string, impact: string }[]
  meta_signal: string
}
```

---

## Workflow

```
Persona + Signal Scan Data (from upstream skills)
    |
Phase 1: Community-Market Fit Assessment (does this domain support a community?)
    |
Phase 2: Concept Design (name, transformation, core promise)
    |
Phase 3: Platform Selection (Skool, Circle, Discord, etc.)
    |
Phase 4: Membership & Pricing (tiers, monthly/annual, founding member pricing)
    |
Phase 5: Content Cadence Design (recurring value, minimum viable cadence)
    |
Phase 6: Launch Planning (pre-launch, founding members, first 30 days, growth)
    |
Phase 7: Economics (MRR projections, churn, break-even, time investment)
    |
Phase 8: Structure Design (channels, onboarding, engagement, retention)
    |
Phase 9: Bundling Strategy (connect to one-time products, value ladder)
    |
Output: JSON spec + Markdown summary -> hunter/docs/
```

---

## Phase 1: Community-Market Fit Assessment

Before designing anything, evaluate whether this domain actually supports a paid community. Not all domains do. A community is the wrong model for one-time problems.

Score the following five dimensions (1-10 each), with evidence from persona data:

| Dimension | Question | Where to Find Evidence |
|-----------|----------|----------------------|
| Recurring pain | Is the pain ongoing or one-time? | Persona pain stories -- look for patterns of repeated frustration, not single events |
| Peer connection desire | Do these personas want to connect with others like them? | Persona channel behavior -- are they already in communities, forums, Discords? |
| Identity component | Is there a professional or personal identity tied to this domain? | Persona names and language -- "I'm a DevOps engineer" suggests identity; "I need to fix my router" does not |
| Knowledge evolution | Does the knowledge in this domain change frequently? | Signal scan -- are there trend signals showing the landscape shifts? |
| Accountability need | Do these personas need external structure to follow through? | Pain stories -- look for "I know I should but..." or abandoned attempts |

**Community-Market Fit Score** = average of all five dimensions.

### Interpretation

- **8-10**: Strong fit. Community is likely the best monetization model.
- **6-7**: Moderate fit. Community could work but needs a strong differentiator.
- **4-5**: Weak fit. Consider community as a complement to a product, not the primary offer.
- **1-3**: Poor fit. Recommend offer-scope instead. Stop here and explain why.

If the score is 3 or below, do NOT proceed with the community pitch. Instead, recommend the user run offer-scope and explain which dimensions failed.

---

## Phase 2: Concept Design

Name the community and define its core identity. Every decision downstream flows from what you establish here.

### Community Name

- Must be instantly clear about who it is for
- Should imply transformation, not just topic
- Test: if you saw this name on a Skool discovery page, would you immediately know if it is for you?

### Tagline

- One sentence. What this community delivers.
- Formula: "[Outcome] for [specific persona] through [mechanism]"

### Transformation

- Before state: pulled directly from persona pain stories (use their language)
- After state: the identity or capability they gain
- This is the before/after that members buy into

### Core Promise

- The ONE thing this community delivers better than any free alternative
- Not five things. ONE. If you cannot pick one, the community concept is too broad.
- Test: can you complete "Join [name] and you will [one thing]"?

### Positioning Against Free Alternatives

Every domain has free communities (Reddit, Discord servers, Slack groups). Explain specifically why someone would pay when free exists. Valid reasons:

- Curated signal vs noise (free communities are full of beginners asking the same questions)
- Access to practitioner-level peers (not just anyone who joins a free server)
- Structured learning paths (not random discussion threads)
- Direct access to the creator (you cannot DM experts in a 50k-member subreddit)
- Accountability and outcomes (free communities have no skin in the game)

---

## Phase 3: Platform Selection

Evaluate platforms against persona needs. Default recommendation is Skool unless persona data strongly indicates otherwise.

### Platform Comparison

| Platform | Monthly Cost | Best For | Limitations |
|----------|-------------|----------|-------------|
| Skool | $99/mo | Course + community hybrid, gamification, simple UX | No native code sharing, limited customization |
| Circle | $49-399/mo | Branded community, rich media, course integration | More complex setup, higher cost at scale |
| Discord | Free (Nitro $10/mo) | Technical communities, real-time chat, bot integrations | Noisy, hard to monetize, no native payments |
| Mighty Networks | $39-360/mo | Course-first communities, native app, events | Smaller ecosystem, less discovery |
| Custom (forum/app) | Varies | Full control, unique features | High build cost, no built-in discovery |

### Selection Criteria

Evaluate each platform on:

1. **Member experience** -- Does the platform match how this persona already consumes content?
2. **Creator experience** -- How much ongoing maintenance does the platform require?
3. **Discovery** -- Does the platform help attract new members organically?
4. **Monetization** -- How does payment work? (Skool has native payments; Discord requires third-party tools)
5. **Domain-specific needs** -- Does the domain require code sharing, file uploads, live sessions, or other specific features?

Provide a clear recommendation with rationale, not just a comparison table.

---

## Phase 4: Membership & Pricing

Design 1-3 tiers maximum. Simplicity wins. Most Skool communities succeed with a single tier.

### Pricing Principles

- **Anchor to persona WTP data** -- The price must fall within the willingness-to-pay range from persona extraction
- **Compare to existing spend** -- What do they already pay monthly for similar value? (tools, courses, subscriptions)
- **Monthly + annual** -- Always offer both. Annual discount of 15-20% is standard.
- **Founding member price** -- First N members get a locked-in discount. This creates urgency and rewards early adopters.

### Tier Design

For each tier, define:

| Field | Description |
|-------|-------------|
| tier_name | Clear, descriptive name (not "Gold/Silver/Bronze") |
| price | Monthly price |
| annual_price | Annual price (discounted) |
| includes | Specific list of what is included |
| target_persona | Which persona this tier serves |

### Pricing Rules

- If persona WTP ceiling is $50/mo, do not price the main tier at $99/mo
- If you have only one persona, use one tier (or two at most: standard + premium with direct access)
- The lowest tier must provide enough value to retain members on its own -- do not create a hollow entry tier that forces upgrades
- Price the community based on the outcome it delivers, not the content it contains

---

## Phase 5: Content Cadence Design

Define the recurring value that justifies the recurring price. This is where most communities fail -- either the creator burns out or members do not get enough value.

### Minimum Viable Cadence

What is the LEAST you can deliver and still retain members? Start here, not with an ambitious schedule you will abandon in month 3.

### Per Content Type, Define:

| Field | Description |
|-------|-------------|
| content_type | What it is (e.g., "weekly live Q&A", "monthly teardown", "daily tip") |
| frequency | How often |
| time_investment | How much of the creator's time per occurrence |
| value_to_member | Why members stay for this specifically |

### Cadence Rules

- **Total creator time must not exceed 5-10 hours per week** at the target member count. If it does, redesign.
- **At least one synchronous touchpoint** -- Members need to feel connected to a live human, not just consuming async content.
- **Leverage member-generated value** -- Accountability pods, peer feedback, show-your-work threads. The best communities are not one-to-many broadcasts.
- **Async content should be evergreen** -- Recorded sessions, resource libraries, and templates compound over time.
- **Do not commit to daily content** unless you have a system that makes it sustainable (e.g., AI-assisted, repurposed from other work, delegated).

---

## Phase 6: Launch Planning

Plan the launch from the user's current audience size -- even if it is zero.

### Pre-Launch (2-4 weeks before opening)

Define specific steps: where to post, how to collect a waitlist, what free content to publish that demonstrates community value, and who to reach out to individually (warm outreach).

### Founding Member Offer

The deal for the first N members: locked-in pricing below eventual public price, limited quantity for urgency, additional access or perks not available later. Specific N (e.g., "first 50 members") -- not vague.

### Launch Channels

Be specific -- not "social media" but which platform, which community, which format. Prioritize channels where the persona already spends time. Include both owned channels (email list) and borrowed channels (communities, guest appearances).

### First 30 Days

- Week 1: onboarding, welcome, first live session
- Week 2: first content cadence delivery, engagement prompts
- Week 3: member spotlight, community rituals established
- Week 4: feedback collection, cadence adjustment, founding member check-in

### Growth Strategy

Define: referral mechanics, content marketing that drives sign-ups, partnerships with complementary audiences, and platform-native discovery/SEO.

---

## Phase 7: Economics

Conservative projections. The goal is a realistic picture, not a pitch deck.

### Revenue Projections

| Metric | What to Estimate |
|--------|-----------------|
| target_members_month_1 | Realistic count based on current audience and launch plan |
| target_members_month_6 | Growth trajectory accounting for churn |
| target_members_month_12 | Steady-state target |
| monthly_price | From Phase 4 pricing |
| projected_mrr_month_1 | members * price |
| projected_mrr_month_6 | members * price (after churn) |
| projected_mrr_month_12 | members * price (after churn) |
| churn_assumption | Monthly churn rate (5-10% is typical for paid communities) |
| break_even_members | How many members to cover platform costs + creator time |
| time_investment_weekly | Creator hours per week |

### Economics Rules

- **Use 7-10% monthly churn** for initial projections. Optimistic churn assumptions kill community businesses.
- **Break-even must account for creator time** -- not just platform costs. If the creator values their time at $X/hour and spends Y hours/week, that is a real cost.
- **Month 1 projections should be modest** -- 10-30 members for a launch from a small audience, 50-100 for a launch from an established audience.
- **Do not project hockey-stick growth** -- linear or slightly accelerating growth is realistic for communities.

---

## Phase 8: Structure Design

Design the internal architecture of the community.

### Channels or Spaces

For each channel/space:

| Field | Description |
|-------|-------------|
| name | Clear, descriptive name |
| purpose | What this space is for |
| who_posts | "creator only", "members", or "both" |

### Structural Rules

- **Start with fewer channels** -- 3-5 is plenty at launch. You can always add more. Too many empty channels makes the community feel dead.
- **Every channel must have a clear purpose** -- If you cannot explain in one sentence why this channel exists, cut it.
- **Include a wins/progress channel** -- This is where members share results. It provides social proof for retention AND for marketing.

### Onboarding Flow

Goal: get new members to post within 24 hours. Steps: welcome message, introduction prompt, quick win (the ONE resource for immediate value), connection (buddy pairing or relevant thread).

### Engagement Mechanics

What keeps people active: challenges (time-bound, achievable), accountability structures (pods, pairs), gamification (Skool native points/leaderboards), regular prompts (weekly question, monthly theme), member spotlights.

### Retention Hooks

What prevents churn: relationship lock-in, progress tracking, exclusive access, reputation/status built in community, upcoming events to look forward to.

---

## Phase 9: Bundling Strategy

Connect the community to the broader product ecosystem. A community should not exist in isolation.

### Standalone Products

What one-time products (from offer-scope) complement the community? Community as ongoing support for product purchases. Products as lead magnets for community.

### Value Ladder

Map the complete path: Free content -> Low-ticket product ($19-49) -> Community ($X/mo) -> Premium tier / coaching ($XXX/mo)

### Upsell Path

What do community members upgrade to? (coaching, mastermind, done-for-you services)

### Downsell Path

When someone cancels, what do you offer instead? (lower tier, pause, one-time product, alumni channel)

---

## Output

The pitch produces two files, saved to the Obsidian vault:

**Vault path:** `${VAULT}/Admin/Product-Discovery/Offers/`

### 1. JSON Spec: `{vault}/Admin/Product-Discovery/Offers/community-pitch-{domain-slug}-{YYYY-MM-DD}.json`

Structured data following the schema in [references/output-schema.json](references/output-schema.json). Must validate against that schema. Wrapped in a PipelineEnvelope:

```json
{
  "skill": "community-pitch",
  "version": "1.0",
  "session_id": "...",
  "timestamp": "...",
  "input_refs": ["persona-ref", "signal-scan-ref"],
  "output": { ... CommunityPitchOutput ... }
}
```

### 2. Markdown Summary: `{vault}/Admin/Product-Discovery/Offers/community-pitch-{domain-slug}-{YYYY-MM-DD}.md`

Human-readable plan with these sections: Community Concept (name, tagline, transformation, core promise, why not free), Platform Recommendation, Membership Tiers table, Content Cadence table with total weekly creator time, Launch Plan (pre-launch, founding member strategy, launch channels, first 30 days week-by-week, growth strategy), Economics table (members + MRR at month 1/6/12, churn, break-even, creator time), Community Structure (channels table, onboarding flow, engagement mechanics, retention hooks), Bundling Strategy (standalone products, upsell/downsell paths, value ladder), Kill Criteria checklist, and References (persona_ref, decision_ref, signal_scan_ref).

---

## Resources

### references/

- `output-schema.json` -- JSON Schema for the structured community pitch output. Load when producing the JSON file to validate against.

---

## Quality Checklist

Run this checklist before delivering the pitch:

- [ ] Community-market fit score justified with evidence from persona data for each of the 5 dimensions
- [ ] Core promise is ONE thing, not five things
- [ ] Pricing anchored to persona WTP data (not aspirational)
- [ ] Content cadence total weekly creator time is 5-10 hours or less
- [ ] No daily content commitment unless sustainability system is defined
- [ ] Launch plan starts from current audience size (even if zero)
- [ ] Month 1 member projections are modest (10-30 for small audience, 50-100 for established)
- [ ] Churn assumption is 7-10% monthly (not optimistic)
- [ ] Economics include creator time cost, not just platform fees
- [ ] Kill criteria defined before launch
- [ ] Bundling strategy connects to existing offer-scope products
- [ ] Platform recommendation has specific rationale tied to persona needs
- [ ] Onboarding flow gets new members to post within 24 hours
- [ ] Community starts with 3-5 channels maximum
- [ ] Founding member offer has a specific N and specific pricing
- [ ] JSON output validates against `references/output-schema.json`
- [ ] Output is wrapped in PipelineEnvelope with correct input_refs
- [ ] Both JSON and markdown files are saved to vault `Admin/Product-Discovery/Offers/`
- [ ] All upstream references (persona_ref, decision_ref, signal_scan_ref) are linked
