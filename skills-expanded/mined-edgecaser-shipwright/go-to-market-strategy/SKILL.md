---
name: go-to-market-strategy
description: "Builds a comprehensive GTM plan covering beachhead segment selection, ideal customer profile, messaging, channel strategy, launch timeline, and success metrics. Based on Geoffrey Moore's market adoption lifecycle and modern PLG/sales-led hybrid approaches."
category: gtm
default_depth: standard
---

# Go-to-Market Strategy

Read `docs/workflow-contract.md` once per session before applying this skill. Resolve it from the nearest ancestor of this file containing `manifest.json`; all Shipwright paths are relative to that root.

## Description

Builds a comprehensive GTM plan covering beachhead segment selection, ideal customer profile, messaging, channel strategy, launch timeline, and success metrics. Based on Geoffrey Moore's market adoption lifecycle and modern PLG/sales-led hybrid approaches.

## When to Use

- Launching a new product or entering a new market
- Expanding to a new segment or geography
- Repositioning an existing product for a new buyer
- Preparing a launch plan for a major feature release

## Depth

| Scope | Use When | Sections to Include |
|---|---|---|
| **Light** | Quick segment check or internal alignment sketch | Beachhead Segment, Messaging Framework |
| **Standard** | New product launch or market entry | All sections (Steps 1-5) |
| **Deep** | Multi-segment expansion or major repositioning | All sections + competitive positioning per segment, channel unit-economics model, post-launch iteration cadence |

**Omit rules:** At Light depth, skip ICP detail, Channel Strategy, and Launch Timeline. Produce only the Beachhead Segment selection rationale and core Messaging Framework.

## Framework

### Step 1: Beachhead Segment

Identify the single segment you'll win first before expanding:

```markdown
## Beachhead Segment Analysis

### Candidate Segments
| Segment | Size | Pain Severity | Accessibility | Willingness to Pay | Score |
|---|---|---|---|---|---|
| [Segment A] | [S/M/L] | [1-5] | [1-5] | [1-5] | [total] |
| [Segment B] | ... | ... | ... | ... | ... |

### Selected Beachhead: [Segment Name]
**Why this segment first:**
- [Reason 1, e.g., "Highest pain severity, shortest sales cycle"]
- [Reason 2, e.g., "We have existing relationships and credibility"]
- [Reason 3, e.g., "Success here creates referrals to adjacent segments"]

**Expansion path from beachhead:**
[Beachhead] → [Adjacent segment 1] → [Adjacent segment 2] → [Mainstream market]
```

### Step 2: Ideal Customer Profile (ICP)

```markdown
## Ideal Customer Profile

### Company Characteristics
- **Industry:** [verticals]
- **Size:** [employee count / revenue range]
- **Stage:** [startup / growth / enterprise]
- **Tech stack:** [relevant technologies they use]
- **Budget authority:** [who controls the budget]

### Buyer Persona
- **Title:** [typical title]
- **Reports to:** [their boss]
- **Measured on:** [their KPIs]
- **Day-to-day pain:** [what frustrates them daily]
- **Trigger event:** [what makes them start looking for a solution NOW]

### Qualification Criteria
**Must-have (deal breakers):**
- [ ] [Criterion, e.g., "Actively experiencing the problem"]
- [ ] [Criterion, e.g., "Has budget allocated for this category"]

**Disqualification signals:**
- [Signal, e.g., "Just signed a 2-year contract with competitor"]
- [Signal, e.g., "No technical resources to implement"]
```

### Step 3: Messaging Framework

```markdown
## Messaging Framework

### Core Narrative
**Before [product]:** [Describe the painful status quo]
**After [product]:** [Describe the transformed state]
**How:** [The bridge, what the product enables]

### Message Hierarchy
| Level | Message | Audience |
|---|---|---|
| Tagline | [7 words max, headline positioning] | Everyone |
| Value prop | [1-2 sentences, key benefit] | Website visitors |
| Elevator pitch | [30 seconds, problem, solution, proof] | Prospects |
| Full narrative | [2-3 minutes, complete story] | Sales conversations |

### Proof Points
- [Metric: e.g., "Reduces onboarding time by 60%"]
- [Social proof: e.g., "Used by 500+ teams at companies like X, Y, Z"]
- [Case study: e.g., "[Customer] achieved [result] in [timeframe]"]
```

### Step 4: Channel Strategy

```markdown
## Channel Strategy

### Awareness Channels (how they discover us)
| Channel | Investment | Expected Reach | CAC Estimate | Timeline to Results |
|---|---|---|---|---|
| [Content / SEO] | [effort] | [reach] | [$X] | [months] |
| [Paid ads] | [budget] | [reach] | [$X] | [weeks] |
| [Community] | [effort] | [reach] | [$X] | [months] |
| [Partnerships] | [effort] | [reach] | [$X] | [months] |

### Conversion Channels (how they evaluate and buy)
- **Self-serve:** [Free trial / freemium, what triggers conversion]
- **Sales-assisted:** [Demo request flow, qualification criteria for sales touch]
- **Hybrid:** [PLG + sales, when does sales engage?]

### Retention Channels (how we keep them)
- [Onboarding emails, cadence and content]
- [In-app guidance, key activation moments]
- [Customer success, trigger for CSM engagement]
```

### Step 5: Launch Plan

```markdown
## Launch Timeline

### Pre-Launch (T-minus 4 weeks)
- [ ] Internal enablement (sales, support, CS training)
- [ ] Beta feedback incorporated
- [ ] Marketing assets ready (landing page, blog, email, social)
- [ ] Press/analyst briefings (if applicable)
- [ ] Monitoring and alerting configured

### Launch Day (T-0)
- [ ] Feature flag flipped / deployment
- [ ] Blog post published
- [ ] Email sent to [segment]
- [ ] Social media announcements
- [ ] Internal Slack announcement

### Post-Launch (T-plus 1-4 weeks)
- [ ] Monitor adoption metrics daily
- [ ] Collect early user feedback
- [ ] Address critical bugs within 24 hours
- [ ] Week 1 retrospective
- [ ] Week 4 success assessment against targets

## Success Metrics
| Metric | Target | Measurement Method | Review Cadence |
|---|---|---|---|
| [Adoption] | [target] | [source] | [daily/weekly] |
| [Activation] | [target] | [source] | [weekly] |
| [Revenue impact] | [target] | [source] | [monthly] |
```

## Minimum Evidence Bar

**Required inputs:** Target market context, product value proposition, and at least one of: customer interviews, usage data, or validated problem hypothesis.

**Acceptable evidence:** Customer discovery interviews (5+), survey data, market-size estimates from credible sources (analyst reports, census data, industry publications), existing usage or sales pipeline data, competitor pricing pages.

**Insufficient evidence:** If no customer interviews or usage data exist, stop and recommend running the **discovery-interview-prep** or **jobs-to-be-done** skill to conduct 5-10 discovery interviews before attempting this skill.

**Hypotheses vs. findings:**
- **Findings:** Beachhead Segment scoring and ICP qualification criteria must reference real data or interviews.
- **Hypotheses:** Channel Strategy CAC estimates and Launch Timeline adoption targets may be projected, must be labeled "Assumption, validate in first 30 days."

## Output Format

Produce a GTM Plan with:
1. **Beachhead Segment**, who we're targeting first and why
2. **ICP**, detailed ideal customer profile
3. **Messaging Framework**, narrative, hierarchy, proof points
4. **Channel Strategy**, awareness, conversion, retention
5. **Launch Timeline**, pre-launch, launch day, post-launch
6. **Success Metrics**, what we're measuring and target values

**Shipwright Signature (required closing):**
7. **Decision Frame**, recommended beachhead and primary channel, trade-off vs. alternatives, confidence level with evidence quality, owner (head of product or marketing), decision date, revisit trigger (post-launch metric review)
8. **Unknowns & Evidence Gaps**, unvalidated ICP assumptions, untested channels, missing pricing sensitivity data
9. **Pass/Fail Readiness**, PASS if beachhead is scored with real data and messaging is grounded in customer language; FAIL if segment selection is unsupported or no trigger event is identified. **Light-depth exception:** At Light depth, PASS requires only a scored beachhead selection rationale and a core messaging framework; trigger event identification is not evaluated.
10. **Recommended Next Artifact**, Which Shipwright skill to run next and why

## Common Mistakes to Avoid

- **Targeting everyone**, A beachhead of "all SMBs" is no beachhead at all
- **Features-first messaging**, Lead with the customer problem and outcome, not your feature list
- **No trigger event**, Without knowing what makes someone search NOW, your timing will be wrong
- **Channel spray-and-pray**, Pick 2-3 channels and go deep; spreading thin across 10 channels fails
- **Measuring only vanity metrics**, Page views and signups matter less than activation and revenue

## Weak vs. Strong Output

**Weak:**
> "Target segment: SMBs. They need our product because it saves time and money."

No segment scoring, no pain severity, no reason this segment wins over alternatives.

**Strong:**
> "Beachhead: Series A-B fintech startups (50-200 employees). Pain severity 5/5, manual compliance reporting costs them 40+ hrs/month and blocks SOC 2 certification. Accessibility 4/5, three warm intros via YC network. Selected over healthtech (higher pain but 18-month sales cycles) and e-commerce (lower willingness to pay)."

Scored, compared against alternatives, with a clear reason this segment is first.
