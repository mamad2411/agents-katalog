---
name: competitive-landscape
description: "Structures a comprehensive competitive analysis across positioning, feature parity, pricing, go-to-market, and market signals. Produces artifacts useful for strategy sessions, sales enablement, and investor updates."
category: discovery
default_depth: standard
---

# Competitive Landscape Analysis

Read `docs/workflow-contract.md` once per session before applying this skill. Resolve it from the nearest ancestor of this file containing `manifest.json`; all Shipwright paths are relative to that root.

## Description

Structures a comprehensive competitive analysis across positioning, feature parity, pricing, go-to-market, and market signals. Produces artifacts useful for strategy sessions, sales enablement, and investor updates.

## When to Use

- Entering a new market or category
- Preparing for a strategy offsite or board meeting
- Enabling the sales team with competitive intelligence
- Evaluating whether a new entrant threatens your position
- Annual or quarterly competitive refresh

## Depth

| Scope | Use When | Sections to Include |
|---|---|---|
| **Light** | Quick check for a single decision or internal discussion | Competitive Set (Step 1) + Feature Matrix (Step 2) + Executive Summary only |
| **Standard** | Quarterly refresh, strategy session, or sales enablement | All sections |
| **Deep** | Market entry, board presentation, or investor due diligence | All sections + win/loss interview data + scenario modeling for likely competitive responses |

**Omit rules:** At Light depth, skip Positioning Analysis, Competitor Deep Dives, and Market Dynamics. Produce only the competitive set table, capability matrix, and a 3-5 bullet executive summary.

## Framework

### Step 1: Define the Competitive Set

**Direct competitors:** Same category, same buyer persona, overlap in use cases.

**Indirect competitors:** Different category but competing for the same job-to-be-done or budget line.

**Potential entrants:** Adjacent players who could move into your space (watch for platform expansion, acqui-hires, and patent filings).

**Format:**
```markdown
| Competitor | Type | Target Segment | Est. ARR / Funding | Trend |
|---|---|---|---|---|
| [Name] | Direct | [segment] | [estimate] | Growing / Stable / Declining |
```

### Step 2: Feature & Capability Matrix

Build a comparison grid across the capabilities that matter to your target buyer:

```markdown
| Capability | Us | Competitor A | Competitor B | Competitor C |
|---|---|---|---|---|
| [Capability 1] | ● Full | ◐ Partial | ○ None | ● Full |
| [Capability 2] | ◐ Partial | ● Full | ● Full | ○ None |
```

**Legend:** ● Full support | ◐ Partial / limited | ○ Not available

**Rules:**
- Choose capabilities from the buyer's perspective, not your feature list
- Include non-product factors: integrations, support, community, compliance
- Note where "partial" means materially different things per competitor

### Step 3: Positioning Analysis

If structured research facts are available from a prior `collect-research.mjs` run, generate a structured pricing comparison before filling out the positioning map:

```bash
node scripts/pricing-diff.mjs \
  .shipwright/research/competitor-a/facts.json \
  .shipwright/research/competitor-b/facts.json
```

If you staged only the intended packs into a comparison-specific directory, you can also use `node scripts/pricing-diff.mjs --dir path/to/comparison-set/`.

Use the output table to populate the Pricing model and Price range fields below rather than estimating. If facts files are not available, fill those fields from public pricing pages.

For each competitor, map:

```markdown
### [Competitor Name]
**Tagline:** [Their headline positioning]
**Target persona:** [Who they sell to]
**Key differentiator:** [What they claim is unique]
**Pricing model:** [Free / Freemium / Usage / Seat / Enterprise]
**Price range:** [Estimated, or see pricing-diff table above]
**Sales motion:** [PLG / Sales-led / Hybrid]
**Messaging themes:** [What they emphasize in marketing]
```

### Step 4: Strengths, Weaknesses & Strategic Posture

For each key competitor:

```markdown
### [Competitor Name]
**Strengths:**
- [Strength 1 with evidence]
- [Strength 2 with evidence]

**Weaknesses:**
- [Weakness 1 with evidence]
- [Weakness 2 with evidence]

**Recent moves:**
- [Product launch, funding round, partnership, hire]

**Likely next moves:**
- [Predicted based on signals]
```

### Step 5: Market Dynamics

```markdown
## Market Dynamics
**Category maturity:** [Emerging / Growth / Mature / Declining]
**Buyer behavior trends:** [What's changing in how buyers evaluate]
**Consolidation signals:** [M&A activity, shutdowns, pivots]
**Regulatory factors:** [Compliance requirements affecting competition]
**Technology shifts:** [Platform changes, AI, open-source disruption]
```

## Minimum Evidence Bar

**Required inputs:** At least 2 named competitors, a defined buyer persona or segment, and a product category.

**Acceptable evidence:** Public pricing pages, G2/Capterra reviews, analyst reports (Gartner, Forrester), customer win/loss interviews, job postings, press releases, SEC filings, product changelogs, direct product usage.

**Insufficient evidence:** If the competitive set is based solely on internal assumptions with no external validation, state "Insufficient evidence: competitive set is unvalidated" and produce a partial artifact with unvalidated sections marked `[TBD, requires: external validation via customer interviews, win/loss analysis, or public competitor data]` and flag the artifact as draft-only.

**Hypotheses vs. findings:**
- **Findings:** Strengths, weaknesses, and recent moves backed by observable evidence (public data, customer quotes, product tests)
- **Hypotheses:** "Likely next moves" and "Strategic implications", must be explicitly labeled as hypotheses with supporting reasoning

## Output Format

Produce a structured competitive intelligence report with:
1. **Executive Summary**, 3-5 bullet top-line competitive takeaways
2. **Competitive Set**, categorized list of competitors
3. **Feature Matrix**, capability comparison grid
4. **Positioning Map**, how each competitor positions themselves
5. **Competitor Deep Dives**, strengths, weaknesses, recent moves
6. **Market Dynamics**, macro trends affecting competition
7. **Strategic Implications**, what this means for our product decisions (label as hypotheses)

**Shipwright Signature (required closing):**
8. **Decision Frame**, Primary strategic takeaway, trade-off, confidence with evidence quality, owner, decision date, revisit trigger
9. **Unknowns & Evidence Gaps**, What we don't know about the competitive landscape and what evidence would resolve it
10. **Pass/Fail Readiness**, PASS if ≥2 competitors analyzed with sourced evidence (at Light depth: PASS if ≥2 competitors listed with sourced evidence and capability matrix is present; Positioning Analysis, Competitor Deep Dives, and Market Dynamics not required); FAIL if competitive set is assumption-only or no capability matrix produced
11. **Recommended Next Artifact**, Which Shipwright skill to run next (e.g., positioning-statement, competitive-battlecard) and why

## Common Mistakes to Avoid

- **Only analyzing direct competitors**, Indirect competitors and non-consumption are often the bigger threat
- **Feature-counting without context**, Having a feature doesn't mean it's good or that buyers care
- **Stale intelligence**, Competitive landscapes shift quarterly; timestamp everything
- **Ignoring pricing and GTM**, Product parity means nothing if they out-distribute you
- **Bias toward your own strengths**, Be rigorous about where competitors genuinely beat you

## Weak vs. Strong Output

**Weak:**
> "Competitor A is strong in the enterprise segment and has good brand recognition."

No evidence, no specificity, could describe any company. Not actionable.

**Strong:**
> "Competitor A won 3 of 5 enterprise deals we competed for in Q4 (source: win/loss log). Primary differentiator cited by buyers was SOC2 Type II + HIPAA certification, which we lack. Their G2 enterprise rating (4.6/5.0, n=89) outpaces ours (4.1/5.0, n=34). *Implication: we lose on compliance, not product.*"

Sourced, specific, and directly informs where to invest.
