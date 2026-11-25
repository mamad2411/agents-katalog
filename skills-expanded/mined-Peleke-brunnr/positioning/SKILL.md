---
name: positioning
description: "Strategic positioning engine using Dunford's 'Obviously Awesome' framework. Takes offer-scope output, persona data, and SWOT findings, then produces a positioning canvas, messaging hierarchy, ICP profile, and competitive landscape. Use when deepening positioning before pitch."
license: MIT
metadata:
  context: fork
  openclaw:
    emoji: "\U0001F3AF"
---

# Positioning

Transform upstream pipeline data into a complete strategic positioning package using April Dunford's "Obviously Awesome" framework. Produces a positioning canvas (competitive alternatives, unique attributes, value articulation, ICP, market category, emotional hooks), a messaging hierarchy, an ICP profile, and a competitive landscape map -- all grounded in web research and upstream pipeline data.

## Step 0: Load Conventions

Before doing ANYTHING, read the shared conventions file:

```
Read ${SKILLS_DIR}/_conventions.md
```

This file defines: canonical vault path, folder-to-type mapping, frontmatter contract, valid statuses, tag hierarchy, cross-reference syntax, and the PipelineEnvelope schema. All output from this skill MUST conform to those conventions. If there is a conflict between this SKILL.md and `_conventions.md`, the conventions file wins.

## Pipeline Position

```
signal-scan -> decision-log -> persona-extract -> swot-analysis -> offer-scope -> **positioning** -> pitch -> hunter-log
```

This skill consumes the output of `offer-scope`, `persona-extract`, and `swot-analysis`, and feeds into `pitch` for go-to-market materials. Positioning does NOT advance the kanban card (enrichment step, like swot-analysis). The card stays in "Offer Scoped" until pitch runs.

## When to Use

- Deepening positioning beyond the copy-level output from offer-scope Phase 5
- Running competitive alternatives analysis with web-validated evidence
- Identifying unique attributes that are truly differentiating (not just nice-to-have)
- Building a complete ICP profile specific enough to find 10 prospects in 30 minutes
- Selecting and validating a market category against web evidence
- Discovering emotional hooks and anti-messaging for pitch materials
- Planning expansion sequence messaging (what to say now vs. later vs. never)
- Mapping competitive moats with messaging order for different conversation stages

## Trigger Phrases

- "Position this offer"
- "Run positioning for [product]"
- "What's our competitive positioning?"
- "Help me figure out what makes this obviously awesome"
- "Who are the real alternatives and what makes us different?"
- "/positioning [offer-scope output]"

---

## Prerequisites

Before starting, the following must be available:

1. **Offer-scope output** -- A completed offer-scope result containing: product name, format, price, value equation, build spec, positioning (headline, bullets, objections), distribution plan, and revenue model
2. **Persona extraction output** -- The persona used by offer-scope, containing: pain stories (with situation/pain/workaround/emotional state/evidence), decision triggers, objections, willingness-to-pay data, and channel behavior. Four Forces data (push, pull, habit, anxiety) is especially valuable.
3. **SWOT analysis output** (optional but recommended) -- If available, provides: validated strengths (→ unique attributes), key weaknesses (→ anti-messaging), moat assessment (→ competitive moat identification)
4. **Decision log entry** -- The decision record for the chosen opportunity
5. **Signal scan data** -- The original signal scan with PAIN, SPEND, COMPETITIVE, and AUDIENCE signals

If offer-scope is missing, the skill cannot run. If SWOT is missing, Phases 1, 2, and 8 still work but will lack the cross-validation layer.

### Seed Mode

If an existing positioning exercise exists (e.g., a prior brainstorm, a competitor analysis, or a positioning document from another context), it can be provided as a seed. In seed mode, the skill:

1. Parses the existing positioning into the 8-phase structure
2. Validates each phase against Dunford's criteria
3. Deepens with web research where the seed is thin
4. Flags contradictions between the seed and upstream pipeline data
5. Produces the same output artifacts as a fresh run

Provide the seed as a file path or inline content alongside the normal prerequisites.

---

## Input

The skill expects the following input structure (assembled from upstream skill outputs):

```typescript
interface PositioningInput {
  offer: {
    product_name: string
    format: string
    price_point: string
    value_equation: {
      dream_outcome: string
      perceived_likelihood: string
      time_delay: string
      effort_sacrifice: string
    }
    positioning: {
      headline: string
      subheadline: string
      bullet_points: string[]
      objection_handlers: { objection: string, counter: string }[]
      social_proof_angle: string
      guarantee: string
    }
    build_spec: {
      deliverable: string
      transformation: string
      sections: { title: string, estimated_time: string, content_type: string }[]
    }
  }
  persona: {
    persona_name: string
    pain_stories: {
      situation: string
      pain: string
      current_workaround: string
      emotional_state: string
      evidence: string
    }[]
    four_forces?: {
      push: string[]       // what pushes them away from current state
      pull: string[]       // what attracts them to a new solution
      habit: string[]      // what keeps them doing what they do now
      anxiety: string[]    // what makes them nervous about switching
    }
    decision_triggers: { trigger: string, urgency: string, channel: string }[]
    objections: { objection: string, counter: string }[]
    willingness_to_pay: { range: string, evidence: string, anchor_products: string[] }
    channels: { platform: string, behavior: string }[]
  }
  swot?: {
    verdict: string
    validated_strengths: string[]
    key_risks: string[]
    modifications: string[]
    moat_assessment: { current_strength: string, timeline: object }
  }
  domain: string
  opportunity: string
  offer_ref: string
  persona_ref: string
  swot_ref?: string
  decision_ref: string
  signal_scan_ref: string
  seed?: string  // path to existing positioning doc or inline content
}
```

---

## Workflow

```
Offer Spec + Persona + SWOT (from upstream) + optional Seed
    |
Phase 1: Competitive Alternatives Analysis (web search)
    |
Phase 2: Unique Attributes Mapping
    |
Phase 3: Value Articulation
    |
Phase 4: Target Customer Profiling (ICP + anti-ICP)
    |
Phase 5: Market Category Selection (web-validated)
    |
Phase 6: Emotional Hook Discovery  ← Bragi review gate
    |
Phase 7: Expansion Sequence Mapping
    |
Phase 8: Competitive Moat Identification
    |
Output: positioning-canvas.md + messaging-hierarchy.md + icp-profile.md + competitive-landscape.md + positioning.json -> vault
```

---

## Phase 1: Competitive Alternatives Analysis

Identify what customers do TODAY without your product. This is NOT a list of competitors -- it is a list of alternatives, including inaction.

### What to research (via web search):

- **Direct competitors**: Products that solve the same problem for the same audience. Search for them by name, price, format, and positioning.
- **Indirect competitors**: Products that solve the problem differently (e.g., a course vs. a template, a community vs. a book).
- **DIY alternatives**: Blog posts, YouTube playlists, free tools, Stack Overflow threads -- anything the persona currently uses to solve the problem without paying.
- **Inaction**: Doing nothing. This is ALWAYS an alternative. What happens when the persona just lives with the pain? How common is this?
- **Internal solutions**: Building their own (spreadsheets, internal wikis, homegrown scripts). How many people in the target audience have already built something?

### For each alternative, document:

| Field | Description |
|-------|-------------|
| name | The alternative (product name, category, or behavior) |
| type | `direct_competitor` \| `indirect_competitor` \| `diy` \| `inaction` \| `internal` |
| description | What it is and how the persona uses it |
| strengths | What this alternative does well (be honest) |
| weaknesses | Where this alternative falls short for the target persona |
| price | Cost (including time cost for free alternatives) |
| evidence | How you know this is a real alternative (source URL, persona data, signal scan) |

### Rules

- Minimum 4 alternatives, maximum 8. If you cannot find 4, the market may not exist.
- Inaction MUST be listed if the persona commonly does nothing about the pain. Evidence: check persona pain stories for workarounds that amount to "I just deal with it."
- Every alternative must have evidence from web research, not assumptions.
- Do NOT list alternatives the persona has never heard of or would never consider. These must be real alternatives that real people in the target audience actually use.
- Rank alternatives by how frequently the target persona uses them (most common first).

---

## Phase 2: Unique Attributes Mapping

For each attribute of your product, evaluate whether it is truly unique compared to the alternatives identified in Phase 1.

### Attribute Classification

| Classification | Definition | Advances? |
|---------------|------------|-----------|
| `truly_unique` | No alternative offers this at all | Yes |
| `best_in_class` | Alternatives offer something similar but yours is demonstrably better | Yes |
| `table_stakes` | Most alternatives also offer this | No |
| `irrelevant` | The target persona does not care about this | No |

### For each attribute:

| Field | Description |
|-------|-------------|
| attribute | What the product does or has |
| classification | One of the four classifications above |
| technical_basis | WHY this attribute exists (not marketing -- the actual mechanism) |
| alternatives_comparison | How each Phase 1 alternative handles this (or doesn't) |
| evidence | Proof that this is truly unique or best-in-class |

### Rules

- Only `truly_unique` and `best_in_class` attributes advance to Phase 3.
- Every attribute must have a technical basis -- "we're better" is not a technical basis. "Our decision trees use the actual AWS pricing API data from the last 90 days" is.
- If SWOT validated_strengths exist, cross-reference. SWOT strengths that map to truly_unique attributes are the strongest positioning foundations.
- If you cannot identify at least 2 attributes that are `truly_unique` or `best_in_class`, flag this as a positioning weakness. The product may be undifferentiated.
- Minimum 4 attributes evaluated, at least 2 must advance.

---

## Phase 3: Value Articulation

For each advancing attribute (from Phase 2), articulate the value it delivers across three dimensions.

### Value Dimensions

| Dimension | Question | Example |
|-----------|----------|---------|
| Functional | What does this let the customer DO? | "Make a production-ready Terraform decision in 5 minutes instead of 3 days of research" |
| Emotional | How does this make the customer FEEL? | "Stop feeling like a fraud when the senior engineer asks 'why did you choose this?'" |
| Social | How does this change how others SEE the customer? | "Walk into the architecture review with a defensible decision instead of a guess" |

### For each value statement:

| Field | Description |
|-------|-------------|
| attribute | The advancing attribute this value derives from |
| dimension | `functional` \| `emotional` \| `social` |
| value_statement | One sentence stating the value in persona language |
| intensity | `high` \| `medium` \| `low` -- how much the persona cares |
| evidence | Persona data or signal that proves intensity (pain story quote, signal scan finding) |

### Rules

- Every advancing attribute must have at least one value statement per dimension (functional, emotional, social).
- The highest-intensity value statement across ALL attributes becomes the **lead message** for the messaging hierarchy.
- Use persona language, not marketer language. If the persona says "I just want to stop guessing," the value statement is about stopping guessing, not about "data-driven decision excellence."
- Cross-reference with persona Four Forces if available:
  - Push forces → functional value (what pushes them away from current state)
  - Pull forces → emotional value (what attracts them to a new solution)
  - Habit forces → map to alternatives in Phase 1 (what keeps them in the status quo)
  - Anxiety forces → anti-messaging in Phase 6 (what makes them nervous about switching)

---

## Phase 4: Target Customer Profiling (ICP)

Build an ultra-specific Ideal Customer Profile AND an anti-ICP. The ICP must be specific enough to find 10 of them in 30 minutes of searching.

### ICP Structure

| Field | Description |
|-------|-------------|
| title | Job title or role (be specific: "Senior DevOps Engineer at a Series B startup" not "DevOps professional") |
| company_stage | Company size/stage where this pain is worst |
| trigger_moment | The specific moment they realize they need this (from persona decision triggers) |
| current_state | What their day/week looks like right now (from persona pain stories) |
| desired_state | What they want their day/week to look like (from value articulation) |
| budget_authority | Can they buy this themselves or do they need approval? |
| where_to_find | Specific communities, platforms, events, publications where these people congregate |
| how_to_identify | Observable signals that someone is this person (what they post, ask, complain about) |
| investor_narrative | One paragraph explaining why THIS customer segment matters -- written as if pitching to an investor. Why does solving their problem unlock a market? |

### Anti-ICP Structure

| Field | Description |
|-------|-------------|
| title | Who this is NOT for |
| why_not | Why they will not buy or will be unhappy if they do |
| warning_signs | How to recognize them early (before they waste your time or leave bad reviews) |

### Rules

- The ICP must be specific enough to search LinkedIn or a subreddit and find 10 matching people within 30 minutes. "DevOps engineers" is too broad. "Senior DevOps engineers at Series B startups who have posted about Terraform decision fatigue in the last 6 months" is specific enough.
- Anti-ICP must have at least 2 entries. Common anti-ICPs: beginners (if the product assumes intermediate knowledge), enterprise buyers (if the product is indie-scale), people who want done-for-you (if the product is a framework/tool).
- Budget authority matters. If the ICP needs manager approval for a $29 purchase, that is a friction point to note.
- `where_to_find` must list specific, searchable locations -- not "social media" but "r/devops, DevOps Weekly newsletter, KubeCon hallway track."

---

## Phase 5: Market Category Selection

Select the market category that makes the product's value obvious. This is the Dunford insight: the category tells the customer what to expect, what to compare you to, and how much to pay.

### Step 1: Generate 3-5 Category Candidates

For each candidate:

| Field | Description |
|-------|-------------|
| category | The market category name (e.g., "DevOps decision framework," "infrastructure learning platform," "practitioner toolkit") |
| customer_expectation | What a customer expects from this category (features, price, format) |
| competitive_set | Who else is in this category? |
| advantage | Does your product win when compared to others in this category? |
| risk | What expectations does this category set that your product might not meet? |

### Step 2: Web-Validate Each Candidate

For each category, search for:
- How many products exist in this category?
- What do customers pay for products in this category?
- What do customers expect from products in this category?
- Is the category growing, stable, or shrinking?

### Step 3: Select Using Dunford Criteria

```
Read ${SKILLS_DIR}/positioning/references/category-selection-guide.md
```

The selected category must:
1. Make your unique attributes feel IMPORTANT (not just nice-to-have)
2. Set expectations your product can EXCEED (not just meet)
3. Be recognized by the target customer (they use this word when searching or discussing)
4. NOT be a commodity category where the customer's first question is "which one is cheapest?"

### Rules

- Explicitly reject commodity framings. If a category candidate leads to price competition, explain why and discard it.
- The selected category must be validated against real search behavior. Do people actually search for this term?
- If no existing category fits, consider whether the product is creating a new category. New categories are harder (you must educate the market) but defensible if done right.
- Document the reasoning for both the selected category and each rejected candidate.

---

## Phase 6: Emotional Hook Discovery

Discover the emotional framing that makes the positioning resonate on a gut level. This is where strategy becomes language.

### Hook Structure

| Field | Description |
|-------|-------------|
| primary_hook | The main emotional angle (one sentence) |
| framing | `relief` (escape from pain) or `aspiration` (move toward gain) |
| why_this_framing | Evidence from persona data for why this framing works better |
| anti_framing | Words, phrases, and tones to NEVER use. These are poison for the target audience. |
| second_hook | Alternative emotional angle for warm conversations (when the primary hook has already landed) |

### Relief vs. Aspiration

| Framing | When to Use | Example |
|---------|-------------|---------|
| Relief | When the persona's pain is acute and specific (they are actively suffering) | "Stop guessing. Start deciding." |
| Aspiration | When the persona's pain is chronic but manageable (they want to level up) | "The decision framework senior engineers wish they had on day one." |

### Anti-Framing Rules

The anti-framing list is critical. These are words and phrases that will make the target audience tune out, cringe, or distrust you.

Sources for anti-framing:
- Persona objections (what they push back on)
- Persona anxiety forces (what makes them nervous about buying)
- Community norms (what gets downvoted or mocked in their communities)
- Overused marketing language in the category

Examples of common anti-framing for technical audiences:
- "Transform your career" (too grand, triggers BS detector)
- "10x your productivity" (Silicon Valley cringe)
- "Comprehensive guide" (implies long, boring read)
- "Unlock your potential" (self-help register, wrong audience)

### Rules

- The primary hook must use persona language, not marketing language.
- Anti-framing must have at least 5 entries with specific reasoning for each.
- Test the hook: would this sentence feel natural posted in the persona's primary community? If it would get mocked on r/devops, it is wrong.
- **Bragi review gate**: The primary hook, second hook, and anti-framing list MUST be reviewed by the buildlog_gauntlet Bragi persona before finalizing. This is human-facing prose and must clear the prose quality gate defined in `_conventions.md`.

---

## Phase 7: Expansion Sequence Mapping

Map what messaging to use at each stage of the product's lifecycle. Not everything should be said on day one.

### Stages

| Stage | Timeframe | Messaging Discipline |
|-------|-----------|---------------------|
| `now` | Launch through Month 3 | **Sell hard.** Lead with the primary hook and unique attributes. Every message should drive toward the first sale. |
| `next` | Months 4-12 | **Vision slide.** Expand messaging to include second hook, community value, and future roadmap. Warm audience, not cold. |
| `after` | Year 2+ | **Internal only.** Long-term positioning plays (new categories, enterprise, adjacent markets). Do NOT message these externally until the `now` stage is validated. |

### For each stage:

| Field | Description |
|-------|-------------|
| stage | `now` \| `next` \| `after` |
| timeframe | Specific months/quarters |
| key_messages | What to say (2-3 core messages) |
| channels | Where to say it |
| avoid | What NOT to say yet (premature messaging that would confuse the current audience) |

### Rules

- The `now` stage messages must be derived directly from Phase 3 (value articulation) and Phase 6 (emotional hooks).
- The `next` stage can introduce secondary value propositions that are not yet validated.
- The `after` stage should reference Phase 8 (moat identification) -- what becomes messaging when the moat is real.
- The `avoid` field is critical. Premature messaging about future features, enterprise plans, or category creation will confuse early adopters and dilute positioning.

---

## Phase 8: Competitive Moat Identification

Identify technical, market, data, and brand moats with specific messaging order for different conversation stages.

### Moat Types

| Type | Description | Example |
|------|-------------|---------|
| `technical` | Something built into the product that is hard to replicate | "Decision trees generated from real production incident data" |
| `market` | A market position or network effect that compounds over time | "Largest community of mid-level DevOps engineers sharing decision frameworks" |
| `data` | Proprietary data or data network effects | "Aggregated decision outcomes from 500+ production environments" |
| `brand` | Brand recognition, trust, or authority in the niche | "The person practitioners cite when explaining their Terraform choices" |

### For each moat:

| Field | Description |
|-------|-------------|
| moat_type | `technical` \| `market` \| `data` \| `brand` |
| description | What the moat is (one sentence) |
| current_strength | `none` \| `thin` \| `emerging` \| `moderate` \| `strong` |
| timeline_to_strength | When this becomes a real moat (months) |
| messaging_order | When to talk about this moat |

### Messaging Order

| Order | When | Audience |
|-------|------|----------|
| `first_conversation` | Day 1, cold traffic, landing page | Everyone -- this is your lead positioning |
| `second_conversation` | Follow-up, email sequence, warm traffic | People who have already shown interest |
| `investor_only` | Pitch decks, advisor conversations | People evaluating the business, not buying the product |

### Rules

- Cross-reference with SWOT moat_assessment if available. SWOT already evaluated Helmer's 7 Powers -- this phase maps those findings to messaging strategy.
- Be realistic about current moat strength. Most indie products at launch have `none` or `thin` moats.
- The messaging_order matters. Do NOT lead with a moat you do not yet have. "Largest community" is only a first_conversation message if the community already exists.
- At least one moat must be `first_conversation` -- something you can credibly claim today.

---

## Output

The positioning skill produces five artifacts:

### 1. Positioning Canvas: `{vault}/Admin/Product-Discovery/Positioning/{product-slug}-positioning-canvas-{YYYY-MM-DD}.md`

The filled Dunford canvas containing all 8 phases in human-readable format.

```markdown
---
type: positioning-canvas
date: YYYY-MM-DD
status: complete
tags:
  - hunter/positioning
  - hunter/domain/{domain-slug}
  - hunter/opportunity/{opportunity-slug}
offer_ref: "{offer-slug}"
persona_ref: "{persona-slug}"
swot_ref: "{swot-slug}"
decision_ref: "{decision-slug}"
signal_scan_ref: "{signal-scan-slug}"
---

# Positioning Canvas: [Product Name]

**Date**: [date]
**Domain**: [domain]
**Opportunity**: [opportunity]
**Market Category**: [selected category from Phase 5]

---

## Phase 1: Competitive Alternatives

### Alternative 1: [Name] ([type])
**Description**: [what it is]
**Strengths**: [honest assessment]
**Weaknesses**: [for the target persona]
**Price**: [cost including time]
**Evidence**: [source]

[...repeat for all alternatives]

---

## Phase 2: Unique Attributes

| Attribute | Classification | Technical Basis | Alternatives Comparison |
|-----------|---------------|-----------------|------------------------|
| [attr] | [classification] | [basis] | [comparison] |

**Advancing attributes** (truly_unique or best_in_class):
1. [attribute + reasoning]
2. [attribute + reasoning]

---

## Phase 3: Value Articulation

### Lead Message
> [highest-intensity value statement]

### Value Map

| Attribute | Functional | Emotional | Social |
|-----------|-----------|-----------|--------|
| [attr 1] | [value] | [value] | [value] |
| [attr 2] | [value] | [value] | [value] |

---

## Phase 4: Target Customer (ICP)

### Ideal Customer
**Title**: [specific title]
**Company Stage**: [stage]
**Trigger Moment**: [the moment they need this]
**Current State**: [their day today]
**Desired State**: [their day after]
**Budget Authority**: [can they buy solo?]
**Where to Find**: [specific locations]
**How to Identify**: [observable signals]

### Investor Narrative
[one paragraph]

### Anti-ICP
| Who | Why Not | Warning Signs |
|-----|---------|---------------|
| [title] | [reason] | [signals] |

---

## Phase 5: Market Category

**Selected Category**: [category]
**Why**: [reasoning]

### Rejected Categories
| Category | Reason for Rejection |
|----------|---------------------|
| [cat] | [reason] |

---

## Phase 6: Emotional Hooks

**Primary Hook**: [hook]
**Framing**: [relief/aspiration]
**Why This Framing**: [evidence]

**Second Hook**: [hook]

### Anti-Messaging (NEVER use these)
| Word/Phrase | Why It Fails |
|-------------|-------------|
| [phrase] | [reason] |

---

## Phase 7: Expansion Sequence

| Stage | Timeframe | Key Messages | Channels | Avoid |
|-------|-----------|-------------|----------|-------|
| Now | [months] | [messages] | [channels] | [avoid] |
| Next | [months] | [messages] | [channels] | [avoid] |
| After | [months] | [messages] | [channels] | [avoid] |

---

## Phase 8: Competitive Moats

| Moat Type | Description | Current Strength | Timeline | Messaging Order |
|-----------|-------------|-----------------|----------|-----------------|
| [type] | [desc] | [strength] | [timeline] | [order] |

---

## Sources

- [All sources cited, with URLs]

## References

- **Offer Scope**: [[Admin/Product-Discovery/Offers/{offer-slug}]]
- **Persona**: [[Admin/Product-Discovery/Personas/{persona-slug}]]
- **SWOT**: [[Admin/Product-Discovery/SWOT/{swot-slug}]]
- **Decision Log**: [[Admin/Product-Discovery/Decisions/{decision-slug}]]
- **Signal Scan**: [[Admin/Product-Discovery/Signal-Scans/{signal-scan-slug}]]
```

### 2. Messaging Hierarchy: `{vault}/Admin/Product-Discovery/Positioning/{product-slug}-messaging-hierarchy-{YYYY-MM-DD}.md`

What to say first, second, third -- and what to NEVER say.

```markdown
---
type: messaging-hierarchy
date: YYYY-MM-DD
status: complete
tags:
  - hunter/positioning
  - hunter/domain/{domain-slug}
positioning_canvas_ref: "{canvas-slug}"
---

# Messaging Hierarchy: [Product Name]

## First Conversation (cold traffic, landing page, ads)

**Lead with**: [lead message from Phase 3 -- highest-intensity value statement]
**Support with**: [2-3 supporting messages from advancing attributes]
**Emotional hook**: [primary hook from Phase 6]
**Category frame**: "[Product Name] is a [category from Phase 5] that [unique attribute]"

## Second Conversation (warm traffic, email, follow-up)

**Lead with**: [second hook from Phase 6]
**Expand to**: [secondary value propositions]
**Social proof**: [what proof to show at this stage]

## Third Conversation (community, repeat engagement)

**Lead with**: [community value, belonging, peer learning]
**Deepen with**: [roadmap, vision, expansion stage messaging]

## Anti-Messaging (NEVER say these)

| Word/Phrase | Why It Fails | Use Instead |
|-------------|-------------|-------------|
| [phrase] | [reason] | [alternative] |

## Messaging by Channel

| Channel | First Message | Tone | Avoid |
|---------|--------------|------|-------|
| [channel] | [message] | [tone] | [avoid] |
```

### 3. ICP Profile: `{vault}/Admin/Product-Discovery/Positioning/{product-slug}-icp-profile-{YYYY-MM-DD}.md`

Ultra-specific target customer profile from Phase 4.

```markdown
---
type: icp-profile
date: YYYY-MM-DD
status: complete
tags:
  - hunter/positioning
  - hunter/domain/{domain-slug}
positioning_canvas_ref: "{canvas-slug}"
persona_ref: "{persona-slug}"
---

# ICP Profile: [Product Name]

[Full Phase 4 output -- ICP + anti-ICP + investor narrative]
```

### 4. Competitive Landscape: `{vault}/Admin/Product-Discovery/Positioning/{product-slug}-competitive-landscape-{YYYY-MM-DD}.md`

Alternatives + unique attributes + 2x2 positioning map.

```markdown
---
type: competitive-landscape
date: YYYY-MM-DD
status: complete
tags:
  - hunter/positioning
  - hunter/domain/{domain-slug}
positioning_canvas_ref: "{canvas-slug}"
---

# Competitive Landscape: [Product Name]

## Alternatives (from Phase 1)
[Full Phase 1 output]

## Unique Attributes (from Phase 2)
[Full Phase 2 output]

## 2x2 Positioning Map

Axes selected from the two most differentiating attributes:
- X-axis: [attribute 1 spectrum, e.g., "Generic → Domain-specific"]
- Y-axis: [attribute 2 spectrum, e.g., "Reference material → Decision tool"]

| Product/Alternative | [X-axis position] | [Y-axis position] |
|--------------------|--------------------|-------------------|
| **[Your product]** | [position] | [position] |
| [Alternative 1] | [position] | [position] |
| [Alternative 2] | [position] | [position] |
```

### 5. JSON Spec: `{vault}/Admin/Product-Discovery/Positioning/{product-slug}-positioning-{YYYY-MM-DD}.json`

Structured data following the schema in [references/output-schema.json](references/output-schema.json). Must validate against that schema.

---

## Vault Output Contract

All output files are written to the Obsidian vault (iCloud-synced):

```
${VAULT}/Admin/Product-Discovery/Positioning/
```

- Filename format: `{product-slug}-{artifact}-{YYYY-MM-DD}.md` and `{product-slug}-positioning-{YYYY-MM-DD}.json`
- If a file already exists at the target path: APPEND under `## Update: {ISO timestamp}`, do NOT overwrite
- Frontmatter MUST include: `type` (one of the four artifact types), `date`, `status: complete`, `tags` (minimum: `hunter/positioning`)

---

## Resources

### references/

- `output-schema.json` -- JSON Schema for the structured positioning output. Load when producing the JSON file to validate against.
- `dunford-framework.md` -- April Dunford's "Obviously Awesome" framework reference. Consult for framework questions or phase methodology clarification.
- `positioning-canvas-template.md` -- Blank positioning canvas template. Use as starting scaffold for Phase 1-8 output.
- `category-selection-guide.md` -- Market category evaluation criteria. Load during Phase 5 for category selection methodology.

### README.md

- The full Strategic Positioning framework reference, including intellectual lineage (Dunford, Ries/Trout, Moore, Christensen, Kim/Mauborgne), detailed methodology, anti-patterns, and calibration examples. Consult for deep framework questions during a positioning session.

---

## Quality Checklist

Run this checklist before delivering the positioning output:

- [ ] Minimum 4 competitive alternatives identified, each with web-researched evidence
- [ ] Inaction listed as an alternative if persona commonly does nothing about the pain
- [ ] Minimum 4 attributes evaluated, at least 2 advancing as truly_unique or best_in_class
- [ ] Every advancing attribute has a technical basis (not just "we're better")
- [ ] Value articulated across all three dimensions (functional, emotional, social) for each advancing attribute
- [ ] Lead message identified as highest-intensity value statement
- [ ] ICP is specific enough to find 10 matching people in 30 minutes of searching
- [ ] Anti-ICP has at least 2 entries
- [ ] 3-5 category candidates generated and web-validated
- [ ] Selected category makes unique attributes feel important, not just nice-to-have
- [ ] Commodity framings explicitly rejected with reasoning
- [ ] Emotional hook uses persona language (not marketing language)
- [ ] Anti-messaging has at least 5 entries with specific reasoning
- [ ] Phase 6 (emotional hooks) reviewed by Bragi (prose quality gate)
- [ ] Messaging hierarchy reviewed by Bragi (prose quality gate)
- [ ] Expansion sequence has clear now/next/after with messaging discipline per stage
- [ ] `avoid` messaging is specified for each expansion stage
- [ ] At least one moat has `first_conversation` messaging order
- [ ] Moat strengths are realistic (most indie products at launch have none/thin)
- [ ] Cross-referenced with SWOT moat_assessment if available
- [ ] All 5 output artifacts produced (canvas, messaging hierarchy, ICP, competitive landscape, JSON)
- [ ] JSON output validates against `references/output-schema.json`
- [ ] All files saved to vault `Admin/Product-Discovery/Positioning/`
- [ ] All upstream references linked (offer_ref, persona_ref, swot_ref, decision_ref, signal_scan_ref)
- [ ] Pipeline kanban NOT moved (enrichment step -- card stays in "Offer Scoped")
