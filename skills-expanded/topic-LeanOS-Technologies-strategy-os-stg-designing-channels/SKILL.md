---
name: stg-designing-channels
description: >
  Selects GTM acquisition channels, estimates per-channel CAC, designs
  channel mix with investment allocation, and sequences channels by
  phase. Constrained by ACV-channel viability from pricing and growth
  architecture from solutions. Produces channel strategy for unit
  economics hypothesis.
serves: strategist
domain: channel-strategy
affects: unit-economics-hypothesis
depends-on:
  - stg-segmenting-customers (segment characteristics, where they gather)
  - stg-designing-pricing (ACV-channel constraints)
  - stg-designing-solutions (growth architecture)
  - stg-analyzing-competition (competitor acquisition channels)
produces: Channel Strategy section for unit economics hypothesis
---

# Channel Strategy Design

Select GTM acquisition channels, estimate per-channel CAC, design channel mix with investment allocation, and sequence channels by phase. Constrained by ACV-channel viability from pricing and growth architecture from solutions.

## Procedure

### Step 1: Load Constraints [S]

Read upstream outputs:
- ACV-channel constraint from stg-designing-pricing Step 4 (< $1K: zero-touch only; $1K-$10K: light-touch; > $10K: sales-assisted viable)
- Growth architecture from stg-designing-solutions Step 2 (PLG/Network/Traditional/Hybrid)
- Growth loops from stg-designing-solutions Step 6
- Segment characteristics from stg-segmenting-customers (where they gather, observable filters)
- Competitor channels from stg-analyzing-competition
- Pricing tier structure from stg-designing-pricing Step 4
- Mode (VENTURE/BOOTSTRAP/HYBRID) from governor

Assemble constraint summary with sources.

**Gate:** `constraints_loaded: bool` -- ACV-channel constraint, growth architecture, and segment characteristics all available.
- Pass: Step 2.
- Fail: If ACV-channel constraint missing, derive from ARPU range (ARPU x 12 = rough ACV). If growth architecture missing, infer from ACV and buyer type with reduced confidence. Flag missing upstream outputs.

### Step 2: Enumerate Candidate Channels [K-grounded]

**Grounded in:** segment characteristics, growth architecture, competitor channels.

Enumerate 5-8 candidate channels. For each, state the specific mechanism by which it reaches the segment.

Channel taxonomy:

| Category | Channels | Typical ACV Fit |
|----------|----------|-----------------|
| Zero-touch | SEO/content, product-led viral, community/open-source, marketplace listings | < $5K |
| Light-touch | Paid search (SEM), paid social, webinars, developer communities, email outreach, partnerships/integrations | $1K-$25K |
| Sales-assisted | Outbound sales (SDR/AE), events/conferences, channel partners, analyst relations | > $10K |

For each candidate:
- **Mechanism:** How this channel reaches the target segment SPECIFICALLY. "Content marketing" is not a mechanism. "Technical blog posts targeting [segment role] searching for [problem-related queries]" is a mechanism.
- **Segment fit:** Why this channel reaches this segment (cite segment characteristics).
- **Competitor presence:** Are competitors using this channel? (from competitive analysis).

WebSearch for: "[segment] acquisition channels", "[industry] marketing benchmarks", "[competitor] marketing strategy".

**Gate:** `candidates_enumerated: bool` -- at least 5 candidates, each with specific mechanism and segment fit rationale.
- Pass: Step 3.
- Fail: If < 5, broaden search. Document constrained landscape as finding.

### Step 3: Filter by ACV-Channel Viability [R]

Apply ACV-channel constraint as hard filter:

| ACV Range | Eliminate | Keep |
|-----------|----------|------|
| < $1K | Sales-assisted channels | Zero-touch, low-cost light-touch |
| $1K-$10K | High-touch sales (enterprise AE, multi-month cycles) | Zero-touch, light-touch, inside sales |
| > $10K | None eliminated by ACV alone | All viable |

Record eliminated channels with rationale. Check surviving channels against growth architecture alignment.

**Gate:** `channels_filtered: bool` -- elimination log with ACV rationale, surviving channels align with growth architecture.
- Pass: Step 4.
- Fail: If all eliminated, flag: "At this ACV, viable channels extremely constrained. Product must be self-selling or unit economics at risk."

### Step 4: Estimate Per-Channel CAC [S]

For each surviving channel, estimate CAC as a range.

Method:
1. WebSearch for benchmarks: "[channel] CAC benchmark [industry]", "cost per acquisition [channel] SaaS"
2. If no benchmarks, estimate from first principles:
   - Content: production cost / traffic / conversion rate
   - Paid: CPC / conversion rate
   - Sales: AE cost / deals per year

For each channel produce:
- CAC range (low -- high)
- Tier (T1 if published benchmark with source; T2 if synthesized; T3 if first-principles estimate)
- Source (URL or calculation method)
- Ramp time (content/SEO: 6-12 months; paid: immediate; sales: 3-6 months)

**Gate:** `cac_estimated: bool` -- every channel has CAC range, tier, source, ramp time.
- Pass: Step 5.
- Fail: Unknown CAC flagged as "CAC unknown [T3]" with widest reasonable range. Do not drop -- unknown is information.

### Step 5: Design Channel Mix and Investment Split [K-grounded]

**Grounded in:** filtered channels, per-channel CAC, growth architecture, mode.

Two phases:

**Phase 1 -- Bootstrap/Early (months 0-12 or until PMF):**
- Prioritize: lowest CAC, fastest ramp, strongest segment fit
- BOOTSTRAP: 70%+ to revenue-positive/low-cost channels
- VENTURE: can allocate up to 40% to higher-CAC channels if growth rate justifies
- Identify 1-2 "foundation channels"

**Phase 2 -- Scale (post PMF):**
- Add channels viable at scale (paid with known conversion, sales with proven playbook)
- Shift toward best CAC-at-scale characteristics
- Identify "scale channel" for majority growth

Investment table per phase (must sum to 100% per phase).

Calculate blended CAC per phase: sum(channel_CAC_midpoint x channel_investment_%).

**Gate:** `mix_designed: bool` -- splits sum to 100% per phase, blended CAC calculated, rationale documented.
- Pass: Step 6.
- Fail: If even splits (20/20/20/20/20), challenge: no strategic priority. Concentrate 50%+ on foundation channels in Phase 1.

### Step 6: Validate Channel-Economics Coherence [R]

Check blended CAC against LTV:CAC requirement.

| Check | Pass Condition |
|-------|----------------|
| LTV:CAC | LTV_low / blended_CAC_high > 3:1 (VENTURE) or > 5:1 (BOOTSTRAP) |
| Payback | blended_CAC / (monthly ARPU x gross margin) < 18 months (VENTURE) or < 6 months (BOOTSTRAP) |

If fails: identify which channels drag CAC above threshold. State specific numbers and options: (a) shift mix, (b) increase ARPU, (c) reduce churn, (d) accept risk. Do NOT silently adjust to make numbers work.

If passes: state margin of safety with specific numbers.

**Gate:** `coherence_validated: bool` -- LTV:CAC and payback checked with specific numbers.
- Pass: Step 7.
- Fail: Coherence failure is a finding, not a blocker. Report with numbers and options.

### Step 7: Write Channel Strategy Section [S]

Write matching the register template format exactly:

```
**Channel Strategy:**

| Channel | Segment Reach | CAC Estimate (range) | Investment Split | Tier | Source |
|---------|--------------|---------------------|-----------------|------|--------|
| {channel} | {specific mechanism} | {low -- high} | {Phase 1% / Phase 2%} | {T1/T2/T3} | {source} |

- Channel-economics coherence: {pass/fail with specific LTV:CAC ratio and blended CAC}
- ACV-channel constraint: {channel types viable at this ACV, channels eliminated}
- Sequencing rationale: {Phase 1 channels and why first; Phase 2 additions and trigger}
```

Also produce structured outputs for stg-calculating-economics:
- Blended CAC range (Phase 1 and Phase 2)
- S&M investment estimate
- Per-channel CAC ranges

**Gate:** `section_written: bool` -- all template fields populated, coherence result with numbers, sequencing documented.
- Pass: Done.
- Fail: Fix missing fields. Every column must be populated. Coherence must cite specific numbers.

## Quality Criteria

- ACV-channel constraint consumed from pricing (not re-derived)
- Growth architecture consumed from solutions (not re-derived)
- Minimum 5 candidates evaluated (possibility space visible)
- Every channel has specific mechanism for reaching segment (not generic category)
- Per-channel CAC is range with tier label and source
- Investment splits sum to 100% per phase with rationale
- Blended CAC checked against LTV:CAC requirement
- Sequencing distinguishes bootstrap/early from scale phase
- Eliminated channels documented (possibility space)
- All CAC benchmarks cite sources

## Failure Modes

| Mode | Signal | Recovery |
|------|--------|----------|
| Channel list is generic | "content marketing", "social media" without mechanism | Every channel must state HOW it reaches THIS segment specifically |
| CAC benchmarks fabricated | Round numbers without sources ($50, $100) | WebSearch for benchmarks. If none, first-principles with T3 label |
| Even investment split | 20/20/20/20/20 | No strategic priority. Concentrate 50%+ on foundation channels |
| Economics mismatch ignored | Blended CAC exceeds threshold but says "viable" | Report specific numbers. Do not adjust silently |
| Scope creep into Revenue OS | Content calendars, outreach templates, campaign designs | This skill selects channels and estimates costs. Execution is Revenue OS |
| Missing phase sequencing | All channels simultaneous | Content/SEO has 6-12 month ramp. Paid is immediate. Sequence accordingly |

## Boundaries

**In scope:** Channel enumeration, ACV-channel filtering, per-channel CAC estimation, channel mix with investment allocation, phase sequencing, channel-economics coherence, structured output for economics consumption.

**Out of scope:** Pricing design/tier architecture (stg-designing-pricing), LTV/CAC/payback calculation/cost structure/scenario analysis (stg-calculating-economics), growth architecture/growth loops (stg-designing-solutions), competitive landscape mapping (stg-analyzing-competition -- though competitor channel data consumed), GTM execution: content calendars, outreach cadences, campaign design, nurture flows, launch sequencing (Revenue OS).
