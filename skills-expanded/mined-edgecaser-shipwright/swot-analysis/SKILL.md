---
name: swot-analysis
description: "Produces a structured Strengths, Weaknesses, Opportunities, and Threats analysis for a product, feature, or business unit. Goes beyond listing items by cross-referencing quadrants to generate strategic options (SO, WO, ST, WT strategies)."
category: strategy
default_depth: standard
---

# SWOT Analysis

Read `docs/workflow-contract.md` once per session before applying this skill. Resolve it from the nearest ancestor of this file containing `manifest.json`; all Shipwright paths are relative to that root.

## Description

Produces a structured Strengths, Weaknesses, Opportunities, and Threats analysis for a product, feature, or business unit. Goes beyond listing items by cross-referencing quadrants to generate strategic options (SO, WO, ST, WT strategies).

## When to Use

- Evaluating a new market entry or product expansion
- Preparing for strategic planning sessions
- Assessing a product's competitive position before roadmap planning
- Briefing leadership on where a product stands
- Comparing multiple strategic options side-by-side

## Depth

| Scope | Use When | Sections to Include |
|---|---|---|
| **Light** | Quick competitive position check or meeting prep | Define the Subject, Fill the Four Quadrants (top 2-3 per quadrant) |
| **Standard** | Strategic planning input or product review | All sections |
| **Deep** | Market entry decision, M&A evaluation, or board presentation | All sections + PESTEL overlay per threat/opportunity, competitive SWOT comparison, quantified impact estimates per item |

**Omit rules:** At Light depth, skip Cross-Reference for Strategic Options and Prioritize. Produce only the four-quadrant grid with evidence. Watch for symmetrical outputs, if every quadrant has exactly the same number of items with equal weight, the analysis is likely superficial.

## Framework

### Step 1: Define the Subject

Be specific about what you're analyzing. "Our product" is too broad. "Our onboarding flow for enterprise customers" is actionable.

### Step 2: Fill the Four Quadrants

```markdown
# SWOT Analysis: [Subject]

**Date:** [date]
**Scope:** [what exactly is being analyzed]

## Strengths (Internal, Positive)
What do we do well? What advantages do we have? What do customers cite as reasons they chose us?

| Strength | Evidence | Relative to Competitors |
|---|---|---|
| [e.g., "Fastest time-to-value in category"] | [e.g., "Avg onboarding: 3 days vs industry 14 days"] | [Ahead / Parity / Unique] |
| | | |
| | | |

## Weaknesses (Internal, Negative)
Where do we underperform? What do customers complain about? What do competitors do better?

| Weakness | Evidence | Impact |
|---|---|---|
| [e.g., "No mobile app"] | [e.g., "35% of support tickets mention mobile"] | [High / Medium / Low] |
| | | |
| | | |

## Opportunities (External, Positive)
What market trends favor us? What unmet needs exist? What changes (regulatory, technological, behavioral) could we exploit?

| Opportunity | Source | Time Horizon |
|---|---|---|
| [e.g., "New EU regulation requires audit trails"] | [e.g., "EU Digital Services Act, effective Q3 2026"] | [Near / Medium / Long] |
| | | |
| | | |

## Threats (External, Negative)
What competitors or market shifts could hurt us? What trends work against our model? What dependencies are at risk?

| Threat | Likelihood | Severity | Mitigation |
|---|---|---|---|
| [e.g., "Incumbent launches free tier"] | [High / Med / Low] | [High / Med / Low] | [Initial mitigation idea] |
| | | | |
| | | | |
```

### Step 3: Cross-Reference for Strategic Options

This is where SWOT becomes useful instead of just a list. Combine quadrants:

```markdown
## Strategic Options

### SO Strategies (Strengths + Opportunities)
Use strengths to capture opportunities:
- [e.g., "Leverage our fast onboarding to win enterprise deals before the new regulation deadline"]

### WO Strategies (Weaknesses + Opportunities)
Fix weaknesses to unlock opportunities:
- [e.g., "Build mobile app to capture the growing mobile-first buyer segment"]

### ST Strategies (Strengths + Threats)
Use strengths to defend against threats:
- [e.g., "Emphasize our depth of integrations as a moat against the incumbent's free tier"]

### WT Strategies (Weaknesses + Threats)
Mitigate worst-case scenarios:
- [e.g., "If we can't ship mobile before the incumbent launches free, partner with a mobile-first vendor"]
```

### Step 4: Prioritize

Rank the strategic options by impact and feasibility. Identify which belong on the roadmap now vs. later.

## Minimum Evidence Bar

**Required inputs:** A clearly scoped subject (product, feature, business unit, not "our company"), and at least one source of internal data and one source of external/market data.

**Acceptable evidence:** Customer feedback, usage metrics, competitive analysis, market reports, win/loss data, support ticket themes, industry benchmarks.

**Insufficient evidence:** If no competitive or market context is available for the external quadrants (Opportunities/Threats), produce a partial artifact with external quadrants marked `[TBD, requires: competitive research or market analysis data]` and flag the artifact as draft-only.

**Hypotheses vs. findings:**
- **Findings:** Strengths and Weaknesses backed by internal data (metrics, customer quotes, support volumes)
- **Hypotheses:** Opportunities and Threats based on market projections or competitor speculation, must be labeled with source and confidence

## Output Format

Produce:
1. **SWOT Grid** with evidence for each item (not just assertions)
2. **Strategic Options Matrix** (SO, WO, ST, WT) with at least 2 options per quadrant
3. **Top 3 Actions** ranked by urgency and impact

**Shipwright Signature (required closing):**
4. **Decision Frame**, Top strategic action from cross-reference analysis with trade-off (offensive vs. defensive posture), confidence with evidence quality, owner, decision date, revisit trigger
5. **Unknowns & Evidence Gaps**, Quadrant items based on assumption rather than data, missing competitive intel, unverified market trends
6. **Pass/Fail Readiness**, PASS if every quadrant item cites evidence and at least one SO/WT strategy is actionable (at Light depth: PASS if every quadrant item cites evidence, cross-reference strategies are deferred); FAIL if quadrants contain unsourced assertions
7. **Recommended Next Artifact**, Which Shipwright skill to run next and why

## Common Mistakes to Avoid

- **Listing without evidence** - "Great team" is not a strength. "3 engineers with 10+ years in payments infrastructure" is.
- **Confusing internal and external** - Strengths/Weaknesses are things you control. Opportunities/Threats are things happening to you.
- **Stopping at the grid** - The four lists are inputs, not outputs. The strategic options are the actual deliverable.
- **Ignoring the WT quadrant** - It's uncomfortable but it's where your biggest risks live.
- **Doing SWOT in isolation** - Combine with competitive landscape, PESTEL, or customer feedback for grounded inputs.

## Weak vs. Strong Output

**Weak:**
> "Strength: Great product. Weakness: Could be better. Opportunity: Market is growing. Threat: Competition."

Symmetrical, unsourced, and interchangeable with any company, this SWOT does zero analytical work.

**Strong:**
> "Strength: 3-day avg onboarding vs. 14-day industry benchmark (Source: internal telemetry, Jan 2026). Threat: Incumbent announced free tier at $0/seat targeting our SMB segment (Source: competitor press release, Feb 2026). ST Strategy: Accelerate enterprise onboarding as moat, free-tier competitors can't match our white-glove setup."

Each item cites a source, and the cross-reference generates an actionable strategy rather than restating the inputs.
