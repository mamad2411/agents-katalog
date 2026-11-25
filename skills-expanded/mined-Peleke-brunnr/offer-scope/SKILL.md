---
name: offer-scope
description: Offer scoping engine -- takes persona extraction output (pain stories, decision points, buying triggers, archetypes) and signal scan SPEND data, then produces a complete 1-day build spec with positioning, distribution plan, and revenue model. Use when converting validated persona insights into a shippable product spec.
license: MIT
metadata:
  openclaw:
    emoji: "\U0001F3AF"
---

# Offer Scope

Transform persona extraction output and signal scan SPEND data into a complete 1-day build spec. Produces a structured JSON spec and a human-readable markdown summary with value equation, positioning copy, distribution plan, revenue projections, and kill criteria.

## Step 0: Load Conventions

Before doing ANYTHING, read the shared conventions file:

```
Read ${SKILLS_DIR}/_conventions.md
```

This file defines: canonical vault path, folder-to-type mapping, frontmatter contract, valid statuses, tag hierarchy, cross-reference syntax, and the PipelineEnvelope schema. All output from this skill MUST conform to those conventions. If there is a conflict between this SKILL.md and `_conventions.md`, the conventions file wins.

## Pipeline Position

```
signal-scan -> decision-log -> persona-extract -> **offer-scope** -> hunter-log
```

This skill consumes the output of `persona-extract` and `signal-scan`, and feeds into `hunter-log` for execution tracking.

## When to Use

- Converting validated persona insights into a shippable product spec
- Scoping a 1-day build from persona pain stories and decision points
- Generating positioning copy grounded in real persona language
- Creating a revenue model anchored to SPEND data
- Deciding whether to build or kill an offer before committing time

## Trigger Phrases

- "Scope an offer for [persona]"
- "Build spec from this persona"
- "What should I ship for [persona] in one day?"
- "Turn this persona into a product"
- "/offer-scope [persona-extract output]"

---

## Prerequisites

Before starting, the following must be available:

1. **Persona extraction output** -- A completed persona-extract result containing: persona name, pain stories (with situation/pain/workaround/emotional state/evidence), decision triggers, objections, willingness-to-pay data, and channel behavior
2. **Signal scan SPEND data** -- SPEND signals from a completed signal-scan with price ranges, volume evidence, and platform data
3. **Domain and opportunity** -- The specific domain and opportunity area being targeted
4. **Constraints** -- Ship time (default: 1 day), format preferences, distribution channels available

If any of these are missing, prompt the user to run the upstream skill first or provide the data manually.

---

## Input

The skill expects the following input structure (typically assembled from upstream skill outputs):

```typescript
interface OfferScopeInput {
  persona: {
    persona_name: string
    pain_stories: {
      situation: string
      pain: string
      current_workaround: string
      emotional_state: string
      evidence: string
    }[]
    decision_triggers: { trigger: string, urgency: string, channel: string }[]
    objections: { objection: string, counter: string }[]
    willingness_to_pay: { range: string, evidence: string, anchor_products: string[] }
    channels: { platform: string, behavior: string }[]
  }
  domain: string
  opportunity: string
  spend_signals: {
    signal: string
    price_range: string
    volume_evidence: string
    platform: string
  }[]
  constraints: string[]  // e.g. ["must ship in 1 day", "PDF or Notion template only"]
}
```

---

## Workflow

```
Persona + SPEND Data + Constraints (from upstream skills)
    |
Phase 1: Decision Point Selection (highest-value intervention point)
    |
Phase 2: Value Equation Design (Hormozi's 4 quadrants)
    |
Phase 3: Format Selection (constrained by ship time + persona context)
    |
Phase 4: Scope Definition (sections, time estimates, total <= 8 hours)
    |
Phase 5: Positioning & Copy (persona's exact language)
    |
Phase 6: Distribution Planning (specific channels + launch strategy)
    |
Phase 7: Revenue Modeling (conservative projections + kill criteria)
    |
Output: JSON spec + Markdown summary -> hunter/docs/
```

---

## Phase 1: Decision Point Selection

From the persona's decision triggers, select the ONE with the highest composite score across three dimensions:

- **Pain intensity** -- How much does this hurt? (from pain stories referencing this trigger)
- **Urgency** -- How time-sensitive is the trigger? (from the trigger's urgency field)
- **Willingness to pay** -- Will they spend money at this moment? (from willingness-to-pay data)

### Selection Rules

- The selected decision point must connect to at least 3 pain stories from the persona data. If no single trigger connects to 3+, widen scope to combine the top 2 related triggers.
- State the selection reasoning explicitly: which trigger, why it scores highest, which pain stories it connects to.
- If multiple triggers score equally, prefer the one with the strongest SPEND data anchoring.

**Output**: One decision point with justification and connected pain story references.

---

## Phase 2: Value Equation Design

Apply Hormozi's value equation to the selected decision point. All four quadrants must be addressed with specific, evidence-based answers -- not generic marketing language.

| Quadrant | Question | Source |
|----------|----------|--------|
| Dream Outcome | What does the buyer REALLY want? | Persona's emotional state + desired future from pain stories |
| Perceived Likelihood | Why will they believe this works? | Operator's credentials + social proof matched to persona's authority bias |
| Time Delay | How fast do they see results? | Minimize -- what result can they get IMMEDIATELY upon purchase? |
| Effort & Sacrifice | How much work do they have to do? | Minimize -- how does the product do the work FOR them? |

### Value Equation Rules

- Dream Outcome must use the persona's language, not marketer-speak. If the persona says "I just want to stop getting paged at 2am", the dream outcome is about sleeping through the night, not "operational excellence."
- Perceived Likelihood must connect to something the operator actually has (real credentials, real results, real testimonials). Do not fabricate social proof.
- Time Delay should identify the fastest possible win -- what changes the moment they open the product?
- Effort & Sacrifice should specify what the product eliminates. Decision trees, templates, and checklists score well because the buyer follows instead of inventing.

---

## Phase 3: Format Selection

Choose the product format based on three constraints, evaluated in order:

### 1. Ship Time

| Constraint | Viable Formats |
|------------|---------------|
| 1 day (6-8 hours) | PDF, Notion template, short video (< 30 min) |
| 3 days | PDF bundle, video series (2-3 videos), workshop outline |
| 1 week | Mini-course, tool/calculator, community launch |
| 2+ weeks | Full course, SaaS, comprehensive tool |

### 2. Persona Consumption Context

Where and when does this persona consume content? Map from persona channel data:
- **2am after an incident** -> PDF or checklist (no video, they need answers fast)
- **Lunch break learning** -> Short video or template
- **Commute** -> Audio or short-form content
- **Dedicated study time** -> Course or workshop
- **In the moment of the problem** -> Template, checklist, decision tree

### 3. Price Ceiling

Format constrains achievable price point:

| Format | Typical Price Ceiling | Exceptions |
|--------|----------------------|------------|
| PDF / guide | $19-49 | Premium niches can go higher |
| Notion template | $19-39 | |
| Short video | $29-49 | |
| Video series | $49-149 | |
| Workshop | $97-297 | |
| Course | $197-997 | |
| Tool / SaaS | $9-49/mo | |
| Consultation | $150-500/hr | |

Cross-reference with SPEND data. If the persona's willingness-to-pay ceiling is $30, do not spec a $497 course.

**Output**: Selected format with reasoning across all three constraints.

---

## Phase 4: Scope Definition

Define exactly what ships. This is the most critical phase -- scope creep here kills the 1-day timeline.

### Define the Single Transformation

State in one sentence what changes for the buyer after using this product. This is not a feature list. It is the before/after:

> "Before: [persona's current painful state]. After: [specific improved state]."

### Section Planning

Define 4-7 sections or components. For each section:

| Field | Description |
|-------|-------------|
| title | Clear, benefit-oriented section name |
| estimated_time | How long to create this section (in hours) |
| content_type | One of: decision tree, checklist, case study, template, framework, guide, reference, worksheet |

### Scope Rules

- Total estimated hours must not exceed 8. If it does, cut sections until it fits. Cut from the bottom of the value stack (reference material first, core decision tools last).
- Every section must directly serve the single transformation. If a section is "nice to have" but not essential to the transformation, cut it.
- At least one section must be a decision tool (decision tree, checklist, or framework) -- the thing that does the thinking for the buyer.
- Include a "Quick Start" or "Start Here" section as the first section so the buyer gets immediate value.
- List all tools needed to build (e.g., "Claude", "Canva", "Gumroad", "Notion").

---

## Phase 5: Positioning & Copy

Generate positioning using the persona's EXACT language. This is not creative writing -- it is structured extraction from persona data.

### Headline

Pull directly from pain stories. The headline should make the persona think "this person is reading my mind."

- Use their words, not yours
- Reference the specific situation, not the abstract problem
- Test: would this headline make sense posted in the community where the persona hangs out?

### Subheadline

State the transformation in concrete terms:
- What they get (the product)
- What changes (the outcome)
- How fast (time to result)

### Bullet Points (3-5)

Each bullet follows the formula: **Feature -> Benefit -> Feeling**

> "[Feature]: [what it does for them] so you can [how their life changes]"

### Objection Handlers

Map directly from the persona's objections list. For each objection:
- Acknowledge it (do not dismiss)
- Counter with evidence or structural guarantee
- Use the counter from persona data as the starting point

### Social Proof Angle

Match the operator's credentials to the persona's authority bias. What kind of proof does this persona respect?
- Practitioners respect "I've done this 50 times"
- Managers respect "used by teams at [company]"
- Technical people respect "built on [methodology/data]"

### Guarantee

Risk reversal appropriate to the price point:

| Price Range | Appropriate Guarantee |
|-------------|----------------------|
| < $20 | "If it doesn't help, email me and I'll refund you" |
| $20-99 | 30-day money-back, no questions asked |
| $100-499 | 30-day guarantee + bonus if they do the work and it fails |
| $500+ | Results-based guarantee with specific criteria |

---

## Phase 6: Distribution Planning

Where and how to sell. Every recommendation must be specific enough to act on immediately.

### Launch Channel

Select the single best channel for the initial launch based on persona channel data:
- Which specific community, subreddit, or platform?
- What is the persona's behavior on that platform? (lurker, commenter, poster?)
- What content format performs well there?

### Launch Strategy

Value-first approach. The template:

1. **Give away 80% of the insight** -- Post the core framework, decision logic, or key insight as free content in the community
2. **Sell the organized/actionable version** -- The product is the insight packaged into a format that saves time (the PDF, the template, the checklist)
3. **Specific post structure** -- Draft the actual post outline (title, hook, body structure, CTA)

### Ongoing Channels

After launch, where does distribution continue?
- List 2-3 specific channels with expected cadence
- Note whether email capture is warranted (yes if repeat purchase potential or upsell path exists)

---

## Phase 7: Revenue Modeling

Realistic projections with explicit assumptions. Optimism here is the enemy.

### Unit Price

Derive from:
- Value equation output (what is the transformation worth?)
- SPEND data anchoring (what do they already pay for similar things?)
- Format ceiling (what does this format typically sell for?)
- Take the LOWEST of these three as the starting price. You can raise later. You cannot undo a failed launch.

### Projections

| Timeframe | What to Estimate |
|-----------|-----------------|
| First week | Units sold, total revenue |
| First month | Units sold, total revenue |

### Projection Rules

- State every assumption explicitly: conversion rate, traffic estimate, average order value
- Use conservative conversion rates: 1-2% for cold traffic, 3-5% for warm community traffic, 5-10% for email list
- If you have no traffic data, estimate from the community size (subreddit subscribers, Discord members) and assume 0.5-1% see the post
- Revenue targets should feel achievable, not aspirational. The goal is to validate, not to get rich on day one.

### Kill Criteria

Define before building. These are the conditions under which you abandon the product and move on:

- Minimum sales threshold for first week
- Minimum revenue threshold for first month
- Maximum time investment before calling it (including marketing time)
- Qualitative signals (e.g., "no one engages with the free content post")

Kill criteria prevent sunk cost fallacy. Write them down before building so you commit to them when you are not emotionally invested.

---

## Output

The scope produces two files, saved to the Obsidian vault:

**Vault path:** `${VAULT}/Admin/Product-Discovery/Offers/`

### 1. JSON Spec: `{vault}/Admin/Product-Discovery/Offers/offer-scope-{domain-slug}-{YYYY-MM-DD}.json`

Structured data following the schema in [references/output-schema.json](references/output-schema.json). Must validate against that schema.

### 2. Markdown Summary: `{vault}/Admin/Product-Discovery/Offers/{domain-slug}-{YYYY-MM-DD}.md`

Human-readable spec with the following sections:

```markdown
# Offer Scope: [Product Name]

**Date**: [date]
**Domain**: [domain]
**Opportunity**: [opportunity]
**Persona**: [persona_name]
**Format**: [format]
**Price**: [price]
**Ship Time**: [time]

## Decision Point

[Selected decision point with justification]

**Connected pain stories**:
- [pain story 1 summary + evidence]
- [pain story 2 summary + evidence]
- [pain story 3 summary + evidence]

## Value Equation

| Quadrant | Design |
|----------|--------|
| Dream Outcome | [description] |
| Perceived Likelihood | [description] |
| Time Delay | [description] |
| Effort & Sacrifice | [description] |

## Build Spec

**Deliverable**: [what ships -- e.g. "A 25-page PDF with decision trees..."]
**Total Build Time**: [X hours]
**Tools Needed**: [list]

| # | Section | Time | Content Type |
|---|---------|------|-------------|
| 1 | [title] | [time] | [type] |
| 2 | [title] | [time] | [type] |
| ... | ... | ... | ... |

## Positioning

**Headline**: [headline]
**Subheadline**: [subheadline]

**Benefits**:
- [bullet 1]
- [bullet 2]
- [bullet 3]

**Objection Handlers**:
- [objection] -> [counter]
- [objection] -> [counter]

**Social Proof Angle**: [approach]
**Guarantee**: [guarantee]

## Distribution Plan

**Launch Channel**: [specific channel]
**Launch Strategy**:
1. [step 1]
2. [step 2]
3. [step 3]

**Ongoing Channels**: [list]
**Email Capture**: [yes/no + rationale]

## Revenue Model

**Unit Price**: $[price]

| Timeframe | Units | Revenue |
|-----------|-------|---------|
| First week | [n] | $[n] |
| First month | [n] | $[n] |

**Assumptions**:
- [assumption 1]
- [assumption 2]

## Kill Criteria

- [ ] [criterion 1]
- [ ] [criterion 2]
- [ ] [criterion 3]

## References

- **Persona**: [persona_ref]
- **Decision Log**: [decision_ref]
- **Signal Scan**: [signal_scan_ref]
```

---

## Resources

### references/

- `output-schema.json` -- JSON Schema for the structured offer scope output. Load when producing the JSON file to validate against.

---

## Quality Checklist

Run this checklist before delivering the spec:

- [ ] Selected decision point has evidence from 3+ persona pain stories
- [ ] Value equation all 4 quadrants are addressed with persona-specific detail (not generic marketing)
- [ ] Format matches persona consumption context (where/when they consume)
- [ ] Total build time <= 8 hours with per-section estimates that add up
- [ ] Headline uses persona's actual language (not marketer-speak)
- [ ] Price is anchored to SPEND data (not pulled from air)
- [ ] Distribution plan targets a specific community/platform (not "social media")
- [ ] Launch strategy follows value-first approach (give 80%, sell the packaged version)
- [ ] Kill criteria are defined before building
- [ ] Revenue targets are conservative with assumptions stated explicitly
- [ ] The offer solves ONE problem completely, not five problems partially
- [ ] JSON output validates against `references/output-schema.json`
- [ ] Both JSON and markdown files are saved to vault `Admin/Product-Discovery/Offers/`
- [ ] All upstream references (persona_ref, decision_ref, signal_scan_ref) are linked
- [ ] Pipeline kanban updated: move card to "Offer Scoped" column (see _conventions.md Pipeline Kanban Contract)
