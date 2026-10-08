---
name: stg-designing-gtm
description: >
  Designs the complete GTM plan for the hypothesis register. Sequences
  channels by phase with gate criteria, builds messaging framework from
  value proposition, sets target KPIs per phase, derives operational
  constraints from all hypotheses, and defines success/kill criteria.
  Use when constructing register section 7 (GTM Plan) during BUILD.
serves: strategist
domain: go-to-market-strategy
affects: gtm-plan-proposal
depends-on:
  - stg-segmenting-customers (segment access paths)
  - stg-designing-channels (channel strategy, per-channel CAC)
  - stg-designing-pricing (ACV range, pricing tiers)
  - stg-designing-solutions (growth architecture, growth loops)
produces: GTM Plan (Proposed) section for hypothesis register
---

# GTM Plan Design

Design the complete go-to-market plan for the hypothesis register.
Translate channel strategy, value proposition, growth architecture,
and segment data into a phased execution plan with gates, KPIs,
messaging, constraints, and kill criteria.

## Procedure

### Step 1: Load Inputs [S]

Read upstream outputs:

- **Value Proposition** (register section 4): claim, JTBD dimensions,
  differentiator, alternative, unique capability, clause validation status.
- **Channel Strategy** from Unit Economics (register section 3): ranked
  channel list with per-channel CAC, investment splits, phase sequencing,
  channel-economics coherence result.
- **Growth Architecture** (register section 5): PLG / Network / Sales-Led /
  Hybrid, required conditions, rationale.
- **Segment Hypothesis** (register section 2): primary segment, trigger event,
  budget owner, where they gather, observable characteristics, access paths.
- **Pricing** from Unit Economics (register section 3): ACV range, tier
  structure, upgrade triggers.
- **Mode** (VENTURE / BOOTSTRAP / HYBRID) from governor.

Assemble input summary with sources.

**Gate:** `inputs_loaded: bool` -- channel strategy, growth architecture,
value proposition, and segment hypothesis all available.
- Pass: Step 2.
- Fail: If channel strategy missing, cannot design GTM -- stg-designing-channels
  must run first. If growth architecture missing, infer from ACV and buyer type
  with reduced confidence and flag.

### Step 2: Select GTM Architecture [R]

Match growth architecture to GTM execution pattern. The architecture
constrains which GTM motions are viable. Getting this wrong misallocates
every downstream dollar and hire.

| Growth Architecture | GTM Pattern | Primary Motion | Key Metric |
|---------------------|-------------|----------------|------------|
| PLG | Self-serve acquisition + expansion | Signup -> Activation -> Conversion -> Expansion | Activation rate (% reaching aha moment) |
| Network/Viral | Seed + grow network | Recruit constrained side -> density -> expansion | K-factor and cycle time |
| Sales-Led | Outbound + inbound pipeline | Pipeline generation -> qualification -> close | Pipeline-to-close rate |
| Hybrid | PLG bottom-up + sales expansion | Self-serve < $5K, sales-assist $5K-$50K, enterprise > $50K | PQL-to-close rate |
| Marketplace | Supply-side recruitment + demand activation | Curate supply -> create demand -> liquidity | Liquidity rate (% listings transacting) |

Architecture-GTM mismatches to check:

| Mismatch | Signal |
|----------|--------|
| PLG with ACV > $10K | High-ACV buyers expect demos, security reviews, procurement |
| Sales-led with ACV < $2K | A $2K deal cannot support $15K+ fully-loaded CAC |
| Viral mechanics on non-collaborative tool | No natural invitation reason; incentives compensate but K stays < 0.3 |
| Enterprise sales without customer success | Churn kills LTV; need > 90% retention to justify CAC |

**Gate:** `architecture_matched: bool` -- one GTM pattern selected, no
architecture-GTM mismatch detected.
- Pass: Step 3.
- Fail: If mismatch detected, document the mismatch with specific numbers
  (ACV vs CAC threshold) and flag as a finding. Proceed with the closest
  viable pattern and note the risk.

### Step 3: Design Phase-Gated Channel Sequence [K-grounded]

**Grounded in:** channel strategy from Step 1, GTM pattern from Step 2,
mode (VENTURE/BOOTSTRAP/HYBRID).

Design three phases. Each phase has: channels, budget allocation, exit
gate to next phase, and estimated timeline.

**Phase 1: Validation (Pre-PMF)**

Objective: find working acquisition with minimal spend. Learn, do not scale.

Select 1-2 channels maximum from channel strategy. Criteria:
- Lowest absolute cost to test (not lowest CAC -- lowest total spend to learn)
- Fastest feedback loop (paid > content, outbound > inbound for learning speed)
- Strongest founder-channel fit

Phase 1 channel selection by GTM pattern:

| GTM Pattern | Foundation Channel 1 | Foundation Channel 2 |
|-------------|---------------------|---------------------|
| PLG | Product-led viral + content SEO | Community / dev relations |
| Sales-Led | Founder-led outbound (first 10-20 deals) | Inbound content for demo pipeline |
| Network | Manual supply-side recruitment | Community seeding |
| Hybrid | Content + PLG signup | Founder-led sales on expansion deals |
| Marketplace | Manual supply curation | Demand seeding in one geography/vertical |

Budget allocation: 70-80% to foundation channel, 20-30% to secondary.

Exit gate to Phase 2 (ALL must hold):
- Channel produces repeatable acquisition (not one-off spikes)
- CAC is measurable and within 2x of target blended CAC
- Conversion funnel has > 100 data points at each stage
- Time to convert is understood with specific range

**Phase 2: Traction (Post-PMF)**

Objective: scale working channels, add one adjacent channel.

Add channels that:
- Require the volume/data Phase 1 produced (paid needs conversion data)
- Have lower marginal CAC at scale than Phase 1 channels
- Diversify acquisition risk (must not be > 70% from one channel)

Phase 2 additions by GTM pattern:

| GTM Pattern | Scale Addition | Why Now |
|-------------|---------------|---------|
| PLG | Paid search/social, partnerships | Have conversion data to optimize paid |
| Sales-Led | SDR team, events, channel partners | Have playbook from founder-led sales |
| Network | Paid acquisition for demand side | Supply side seeded, need demand |
| Hybrid | Inside sales team, paid | PLG provides PQL data for sales targeting |
| Marketplace | Paid demand acquisition, content | Supply curated, need demand volume |

Budget: 50-60% scale channel, 20-30% foundation (maintenance), 10-20% experimental.

Exit gate to Phase 3 (ALL must hold):
- At least 2 channels producing consistent acquisition
- No single channel > 70% of total acquisition
- Blended CAC within target range
- Net revenue retention measurable

**Phase 3: Scale (Optimization)**

Objective: maximize efficiency, add programmatic channels.

- Compounding channels mature (content/SEO at 18-24 months)
- Retargeting/remarketing across channels
- International expansion if applicable
- Analyst/PR for brand leverage

Budget: 40-50% primary, 20-30% secondary, 10-20% compounding, 10% experimental.

For each phase, state: channels active, budget split (must sum to 100%),
timeline estimate, and exit gate criteria.

**Gate:** `sequence_designed: bool` -- three phases with channels,
budgets summing to 100%, exit gates with specific measurable criteria.
- Pass: Step 4.
- Fail: If phases lack exit gates, add specific measurable criteria.
  If budgets do not sum to 100%, rebalance.

### Step 4: Define Target KPIs per Phase [R]

For each phase, define 3-5 KPIs. KPIs must be specific, measurable,
and tied to the GTM pattern.

KPI selection by GTM pattern and phase:

**PLG KPIs:**

| Phase | KPI | Benchmark |
|-------|-----|-----------|
| Validation | Signup-to-activation rate | Target: 20-40% (best: 60%+) |
| Validation | Time-to-value | < 5 min consumer, < 30 min SMB, < 1 day team |
| Traction | Free-to-paid conversion (freemium) | Target: 2-5% (best: 7-10%) |
| Traction | Trial-to-paid conversion (trial) | Target: 10-25% (best: 40%+) |
| Scale | Net revenue retention | Target: > 100% |
| Scale | Viral coefficient (if applicable) | K > 0.3 to matter, > 1.0 for true virality |

**Sales-Led KPIs:**

| Phase | KPI | Benchmark |
|-------|-----|-----------|
| Validation | Outbound response rate | Problem-first: 8-15%; pitch-first: 1-3% |
| Validation | Founder close rate | Track per segment and deal size |
| Traction | AE quota attainment | Healthy: 55-65% hitting quota |
| Traction | Sales cycle length | 30-90 days mid-market, 90-365 enterprise |
| Scale | SDR-sourced close rate | 10-20% |
| Scale | Customer expansion revenue | 20-40% of new revenue by year 2 |

**Hybrid KPIs:**

| Phase | KPI | Benchmark |
|-------|-----|-----------|
| Validation | Activation rate (self-serve) | 20-40% |
| Validation | PQL identification rate | 5%+ of self-serve users show PQL signals |
| Traction | PQL-to-close rate | Target: 15-30% (if < 10%, PQL definition wrong) |
| Traction | Self-serve to team expansion | > 5% of self-serve expand to team tier |
| Scale | Blended CAC trend | Stable or declining QoQ |

**Network/Marketplace KPIs:**

| Phase | KPI | Benchmark |
|-------|-----|-----------|
| Validation | Supply-side acquisition | Manual recruitment targets |
| Validation | Liquidity rate (marketplace) | > 30% to be a marketplace, not a listing site |
| Traction | Density in target geography/niche | 30-50% of local/niche market |
| Traction | K-factor (network) | > 0.5 to matter; even 0.3 compounds if cycle < 3 days |
| Scale | Organic K-factor | 0.15-0.4 without incentive |

Flag any KPI where the benchmark requires ground-truth data (T3) to
establish a realistic target.

**Gate:** `kpis_defined: bool` -- 3-5 KPIs per phase, each with specific
benchmark and measurement method.
- Pass: Step 5.
- Fail: Replace vanity metrics (pageviews, signups without activation)
  with conversion or retention metrics.

### Step 5: Build Messaging Framework [K-grounded]

**Grounded in:** value proposition (section 4), segment hypothesis
(section 2), competitive analysis.

Translate the value proposition into channel-adapted messaging across
buyer awareness levels.

**5a. Decompose the value proposition into messaging components:**

From the VP claim, extract:
- **Headline:** [Differentiator] for [Target] -- short, specific, no jargon
- **Subhead:** Expand the problem and hint at mechanism
- **Proof points:** 3 maximum. Each specific (numbers, names, timeframes)
- **CTA per awareness level:**

| Awareness Level | Buyer State | Message Lead | CTA |
|----------------|-------------|--------------|-----|
| Unaware | Does not know they have the problem | Cost of status quo | "Learn more" |
| Problem-aware | Knows the problem, not solutions | Problem label | "See how" |
| Solution-aware | Evaluating solutions | Differentiation | "Try free" / "See demo" |
| Product-aware | Knows product, has not converted | Proof and risk reversal | "Start now" |
| Most aware | Ready to buy | Offer | "Get started" / "Talk to sales" |

**5b. Adapt messaging per channel:**

| Channel Type | Messaging Rule |
|-------------|---------------|
| SEO/Content | Write for the problem keyword, not the product category. Problem-aware search volume is typically 3-10x category volume. |
| Paid Search | Bid on high-intent terms only. "[Alternative to competitor]" converts 3-5x vs category terms. |
| Outbound | First message: problem only, no pitch. 5-7 touches over 3-4 weeks. |
| Paid Social | Pattern interrupt required. Lead with surprising data or contrarian take. UGC-style video outperforms polished 1.5-2x. |
| Community | Zero marketing language. 4-8 weeks of pure contribution before any product mention. |

**5c. State what is testable vs assumed:**

Every messaging claim inherits the tier of the hypothesis it derives
from. If the VP clause is T2, the messaging derived from it is T2.
Flag T3-dependent messaging explicitly.

**Gate:** `messaging_built: bool` -- headline, subhead, proof points,
awareness-level CTAs, and per-channel adaptations all produced.
VP clause tracing documented.
- Pass: Step 6.
- Fail: If messaging cannot trace to VP claims, the VP is too vague
  for GTM. Flag as a dependency issue.

### Step 6: Derive Operational Constraints [S]

Extract constraints that limit GTM execution from each hypothesis:

| Source | Constraint Type | Example |
|--------|----------------|---------|
| Problem hypothesis | Urgency/timing | Seasonal problem = launch window constraint |
| Segment hypothesis | Access limitations | Segment does not use LinkedIn = outbound via LinkedIn nonviable |
| Unit Economics | Budget ceiling | Bootstrap mode = < $50K total Phase 1 spend |
| Unit Economics | CAC ceiling | Blended CAC must stay below 1/3 first-year ACV |
| Unit Economics | Payback requirement | Bootstrap: < 6 months; Venture: < 18 months |
| Growth Architecture | Motion constraint | PLG requires activation < 1 day; sales-led requires playbook before SDR hire |
| Pricing | Deal size constraint | ACV < $2K eliminates sales-assisted channels |

Compile constraint list with source hypothesis and blast radius
(HIGH/MEDIUM/LOW) if violated.

**Gate:** `constraints_derived: bool` -- at least one constraint from
each upstream hypothesis documented with blast radius.
- Pass: Step 7.
- Fail: If a hypothesis provides no constraints, re-read it. Every
  hypothesis constrains GTM somehow.

### Step 7: Define Success and Kill Criteria per Phase [R]

For each phase, define:

**Success criteria** (move to next phase):
- The exit gate from Step 3 restated as measurable outcomes
- Minimum data thresholds (not just "positive results" -- specific
  conversion rates, specific pipeline numbers, specific CAC ranges)

**Kill criteria** (stop or pivot):

| Signal | Timeframe | Action |
|--------|-----------|--------|
| Phase 1: Zero repeatable acquisition after 90 days with adequate effort | 90 days | Reassess channel-segment fit. If problem hypothesis holds, test different channels. If no channel works, problem hypothesis may be wrong. |
| Phase 1: CAC > 3x target after optimization | 120 days | Channel economics nonviable at this ACV. Either raise ACV or find cheaper channels. |
| Phase 2: Blended CAC rising > 20% QoQ | 2 consecutive quarters | Market saturating or targeting exhausted. Diversify or narrow. |
| Phase 2: Single channel > 70% of acquisition | Any point | Fragile. Platform change can halve acquisition overnight. Accelerate diversification. |
| Phase 3: Net revenue retention < 100% | Any point | Churn exceeds expansion. Product or CS problem, not GTM. |

Kill criteria must be specific and observable. "Not working" is not
a kill criterion. "< 50% of target pipeline after 90-day test with
$X budget" is a kill criterion.

**Gate:** `criteria_defined: bool` -- every phase has success criteria
with specific numbers and kill criteria with timeframes and actions.
- Pass: Step 8.
- Fail: Replace qualitative criteria ("good traction") with quantitative
  thresholds.

### Step 8: Apply Diagnostic Framework [R]

Before writing, run the diagnostic sequence against the designed plan
to catch structural issues:

```
1. Is there demand? (Does the segment search for this problem? Do
   they respond to outbound?)
   -> If NO from research: flag as T3 gap. Problem hypothesis may need
      revisiting.

2. Can the funnel convert? (Is the messaging-market fit plausible given
   awareness-level mapping?)
   -> If messaging depends on T3 claims: flag messaging as hypothesis,
      not plan.

3. Can users activate? (Is time-to-value compatible with the growth
   architecture?)
   -> If PLG and time-to-value > 1 day: flag activation risk.

4. Is CAC sustainable? (Does the channel mix produce blended CAC within
   constraints?)
   -> If blended CAC > 1/3 first-year ACV: flag economics risk.

5. Is the plan survivable? (Can the team execute Phase 1 channels given
   founder-channel fit?)
   -> If required channels do not match team capabilities: flag
      execution risk.
```

Document findings from this diagnostic as GTM risks in the plan.

**Gate:** `diagnostic_passed: bool` -- all 5 diagnostic checks run,
findings documented.
- Pass: Step 9.
- Fail: Findings are information, not blockers. Document and proceed.
  Structural issues (demand nonexistent, CAC impossible) should be
  flagged prominently but do not prevent writing the plan.

### Step 9: Write GTM Plan Section [S]

Write register section 7 matching the register format:

```
## 7. GTM Plan (Proposed)

**Support State:** PROPOSED
**Last Updated:** {date}

### GTM Architecture
- Pattern: {PLG / Sales-Led / Network / Hybrid / Marketplace}
- Rationale: {why this pattern for this architecture and ACV}

### Channel Sequence

**Phase 1: Validation ({timeline})**
- Channels: {channel 1 (budget %), channel 2 (budget %)}
- Total budget: {estimate}
- Target KPIs: {3-5 specific KPIs with benchmarks}
- Exit gate: {specific measurable criteria}
- Kill criteria: {specific triggers with timeframes}

**Phase 2: Traction ({timeline})**
- Channels: {existing + additions (budget %)}
- Target KPIs: {3-5 specific KPIs with benchmarks}
- Exit gate: {specific measurable criteria}
- Kill criteria: {specific triggers with timeframes}

**Phase 3: Scale ({timeline})**
- Channels: {full mix (budget %)}
- Target KPIs: {3-5 specific KPIs with benchmarks}
- Kill criteria: {specific triggers with timeframes}

### Messaging Framework
- Headline: {from VP}
- Subhead: {problem expansion}
- Proof points: {3 max, specific}
- Awareness-level CTAs: {table}
- Channel adaptations: {per active channel}

### Operational Constraints
{constraint list with source hypothesis and blast radius}

### GTM Risks
{diagnostic findings from Step 8}

### Constraints from Hypotheses
- From Problem: {constraint}
- From Segment: {constraint}
- From Unit Economics: {constraint}
- From Growth Architecture: {constraint}
```

Set support state to PROPOSED. Gap Definer validates or blocks.

**Gate:** `section_written: bool` -- all subsections populated, support
state = PROPOSED, every KPI has a benchmark, every phase has exit/kill
criteria with specific numbers.
- Pass: Done.
- Fail: Fix missing subsections. Every field must be populated.

## Quality Criteria

- Growth architecture consumed from section 5 (not re-derived)
- Channel strategy consumed from section 3 (not re-derived)
- Value proposition consumed from section 4 (not re-derived)
- Messaging traces to VP claims with tier inheritance
- Phase gates have specific measurable criteria (not qualitative)
- KPIs include benchmarks from domain knowledge (not invented)
- Kill criteria have timeframes and specific actions
- Operational constraints cite source hypothesis
- Budget splits sum to 100% per phase
- No channel-architecture mismatch present without flagged risk
- Diagnostic framework run and findings documented
- All CAC benchmarks and conversion benchmarks cite domain basis

## Failure Modes

| Mode | Signal | Recovery |
|------|--------|----------|
| Generic messaging | "Great solution for modern teams" | Trace every message clause to a specific VP claim and segment characteristic |
| Vanity KPIs | Pageviews, impressions, signups-without-activation | Replace with conversion, retention, or revenue metrics with benchmarks |
| Missing phase gates | "Move to Phase 2 when ready" | Define specific measurable exit criteria with thresholds |
| Architecture-GTM mismatch | PLG plan for $50K ACV product | Check ACV against GTM pattern constraints; flag if mismatched |
| CAC denial | "$0 CAC" or no founder time accounting | Every channel has a real cost including founder time at opportunity cost |
| All channels simultaneously | No phasing, no prioritization | Phase 1 must focus on 1-2 channels. Concentration before diversification. |
| Messaging without tier tracing | Confident messaging from T2/T3 claims | Every message inherits the tier of its source hypothesis clause |
| Kill criteria too vague | "Revisit if not working" | Specific: "< X% conversion after Y days with $Z spend" |
| Scope creep into execution | Content calendars, outreach templates, campaign designs | This skill designs the GTM plan. Execution is downstream. |
| Premature scaling assumption | Phase 2 assumes working channel before Phase 1 validates | Each phase depends on prior phase exit gate being met |

## Boundaries

**In scope:** GTM architecture selection, phase-gated channel sequencing,
target KPIs with benchmarks, messaging framework derived from VP, operational
constraint derivation, success/kill criteria per phase, diagnostic check.

**Out of scope:** Channel identification and per-channel CAC estimation
(stg-designing-channels), pricing design and tier architecture
(stg-designing-pricing), LTV/CAC/payback calculation and cost structure
(stg-calculating-economics), growth architecture selection and rationale
(stg-designing-solutions), competitive landscape mapping
(stg-analyzing-competition), GTM execution: content production, outreach
cadences, campaign management, nurture flows (downstream execution systems).
