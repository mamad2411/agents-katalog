---
name: swot-analysis
description: Evidence-grounded SWOT analysis engine -- takes persona extraction output, signal scan data, format research, and market hypothesis, then produces a brutally honest Strengths/Weaknesses/Opportunities/Threats analysis with verdict (proceed/pivot/kill), risk registry, and moat assessment. Use when stress-testing a product hypothesis before committing to a build spec.
license: MIT
metadata:
  context: fork
  openclaw:
    emoji: "\U0001F50D"
---

# SWOT Analysis

Transform upstream pipeline data into an evidence-grounded SWOT analysis that stress-tests a product hypothesis before you invest build time. Produces a structured JSON spec and a human-readable markdown summary with cited evidence for every point, a clear verdict, a risk registry with monitoring thresholds, and a realistic moat assessment.

## Step 0: Load Conventions

Before doing ANYTHING, read the shared conventions file:

```
Read ${SKILLS_DIR}/_conventions.md
```

This file defines: canonical vault path, folder-to-type mapping, frontmatter contract, valid statuses, tag hierarchy, cross-reference syntax, and the PipelineEnvelope schema. All output from this skill MUST conform to those conventions. If there is a conflict between this SKILL.md and `_conventions.md`, the conventions file wins.

## Pipeline Position

```
signal-scan -> decision-log -> persona-extract -> **swot-analysis** -> offer-scope -> pitch -> hunter-log
```

This skill consumes the output of `persona-extract`, `signal-scan`, and `decision-log`, and feeds into `offer-scope` for build spec generation. The verdict determines whether the hypothesis proceeds to offer-scope at all.

## When to Use

- Stress-testing a product hypothesis before committing to a build spec
- Validating whether a market opportunity has fatal weaknesses before investing time
- Grounding a go/no-go decision in external evidence rather than gut feeling
- Identifying specific risks to monitor during build and launch
- Assessing whether a moat is buildable for a given product/market combination
- Deciding between proceed, pivot, or kill before offer-scope

## Trigger Phrases

- "Run a SWOT on this hypothesis"
- "Stress-test this product idea"
- "Should I actually build this?"
- "What are the real risks here?"
- "Is this hypothesis viable?"
- "/swot-analysis [hypothesis]"

---

## Prerequisites

Before starting, the following must be available:

1. **Persona extraction output** -- A completed persona-extract result containing: persona archetypes, pain stories, decision triggers, objections, willingness-to-pay data, and channel behavior
2. **Signal scan data** -- A completed signal-scan with PAIN, SPEND, COMPETITIVE, SENTIMENT, DEMAND, BEHAVIOR, and AUDIENCE signals
3. **Decision log** -- The decision record for the chosen opportunity, including rationale and constraints
4. **Market hypothesis** -- A specific, testable hypothesis statement including: product, format, price, audience, distribution channel, and brand thesis
5. **Format research findings** (optional) -- Any research on the specific format being considered (e.g., Skool community research, PDF market data, course platform analysis)

If the market hypothesis is not explicitly stated, synthesize one from the upstream data before proceeding. The hypothesis must be concrete enough to test -- "DevOps education" is not a hypothesis; "A $29 decision-framework PDF for mid-level DevOps engineers, distributed through GitHub and r/devops, feeding into a $49/mo Skool community" is a hypothesis.

---

## Input

The skill expects the following input structure (assembled from upstream skill outputs):

```typescript
interface SwotAnalysisInput {
  hypothesis: {
    product: string          // what you are building
    format: string           // PDF, course, community, tool, etc.
    price: string            // specific price or price range
    audience: string         // who this is for (from persona)
    distribution_channel: string  // how they find it
    brand_thesis: string     // the core positioning statement
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
    decision_triggers: { trigger: string, urgency: string, channel: string }[]
    objections: { objection: string, counter: string }[]
    willingness_to_pay: { range: string, evidence: string, anchor_products: string[] }
    channels: { platform: string, behavior: string }[]
  }
  signal_scan: {
    domain: string
    opportunity: string
    pain_signals: { signal: string, intensity: number, source: string }[]
    spend_signals: { signal: string, price_range: string, platform: string }[]
    competitive_signals: { signal: string, type: string, source: string }[]
    sentiment_signals: { signal: string, valence: string, source: string }[]
    audience_signals: { signal: string, reach: string, source: string }[]
  }
  format_research?: {
    findings: string[]
    sources: string[]
  }
  decision_ref: string       // slug of the decision-log entry
  persona_ref: string        // slug of the persona-extract entry
  signal_scan_ref: string    // slug of the signal-scan entry
}
```

---

## Workflow

```
Hypothesis + Persona + Signal Scan + Format Research (from upstream)
    |
Phase 1: Hypothesis Framing (crystallize what we are testing)
    |
Phase 2: Strengths Research (web search for internal advantages)
    |
Phase 3: Weaknesses Research (web search for internal vulnerabilities)
    |
Phase 4: Opportunities Research (web search for external tailwinds)
    |
Phase 5: Threats Research (web search for external headwinds)
    |
Phase 6: Synthesis (verdict: proceed / proceed-with-modifications / pivot / kill)
    |
Phase 7: Risk Registry (specific, measurable risks with monitoring methods)
    |
Phase 8: Moat Assessment (what could become defensible, on what timeline)
    |
Output: JSON spec + Markdown summary -> vault
```

---

## Phase 1: Hypothesis Framing

Before analyzing anything, state the hypothesis in one paragraph. This is the specific claim being tested. It must include ALL of the following:

- **Product**: What you are building (name and brief description)
- **Format**: The delivery mechanism (PDF, course, community, tool, etc.)
- **Price**: The specific price point or pricing model
- **Audience**: Who this is for (referencing the persona)
- **Distribution channel**: How they will find it
- **Brand thesis**: The core positioning statement -- the one sentence that makes the audience say "that's exactly my problem"

**Rules**:
- The hypothesis must be falsifiable. "This could work" is not a hypothesis. "Mid-level DevOps engineers will pay $29 for a decision-framework PDF because no practitioner-grade decision guide exists in the market" is a hypothesis.
- If the hypothesis is vague, push the operator to sharpen it before proceeding.

**Output**: A single, concrete hypothesis paragraph.

---

## Phase 2: Strengths Research (Internal, Positive)

Identify internal advantages that support the hypothesis. These are things the operator controls or possesses.

### What to research (via web search):

- **Operator credentials validation**: Search for evidence that the operator's background is rare or valued in the target market. How does the community evaluate credibility?
- **Format-market fit**: Search for evidence that the chosen format resonates with the audience. Do people in this niche buy this type of product?
- **White space validation**: Search for whether the specific positioning (not just the topic) is unoccupied. Is anyone selling this exact angle?
- **Price architecture fit**: Search for the pricing landscape. Does the chosen price sit in a viable tier?
- **Pedagogical advantage**: Search for what the audience values in educators. Does the operator's teaching background match?
- **Distribution channel viability**: Search for whether the chosen channel actually reaches the target audience.

### Rules

- Minimum 4 strengths, each with a specific source, data point, or finding.
- Every strength must cite evidence from web research, upstream signals, or persona data. No vibes.
- Each strength must explain WHY it is a strength for THIS hypothesis, not just a nice thing to have.
- Score each strength as high/medium/low impact on the hypothesis succeeding.

---

## Phase 3: Weaknesses Research (Internal, Negative)

Identify internal vulnerabilities that threaten the hypothesis. These are things the operator lacks or that are structurally fragile.

### What to research (via web search):

- **Cold-start problem**: Search for data on how hard it is to launch this type of product with zero audience. What do zero-audience success stories look like? What is the typical failure mode?
- **Churn and retention**: Search for churn rates, retention benchmarks, and LTV data for the specific format/platform being used.
- **Audience skepticism**: Search for how the target audience feels about paid content in this space. What is the "free content floor"?
- **Conversion benchmarks**: Search for lead-to-sale conversion rates for the specific funnel being proposed.
- **Platform limitations**: Search for known limitations of the chosen distribution platform that could hurt the target audience experience.
- **Skill gaps**: Identify operator skill gaps (e.g., marketing, sales, community management) that are critical to the hypothesis succeeding.

### Rules

- Minimum 4 weaknesses, each with specific evidence.
- Do NOT soften weaknesses. If the cold-start problem is severe, say so. If the operator has no audience, that is a critical weakness, not a "challenge to overcome."
- Each weakness must explain the specific impact on the hypothesis.
- Score each as high/medium/low impact.

---

## Phase 4: Opportunities Research (External, Positive)

Identify external tailwinds that could accelerate the hypothesis. These are market forces the operator does not control but can ride.

### What to research (via web search):

- **Competitive landscape gaps**: Search for what competitors are doing RIGHT NOW. Where are the gaps? Who is NOT serving this audience?
- **Market growth data**: Search for market size, growth rates, salary data, and hiring trends in the target domain.
- **Platform changes**: Search for recent platform updates, pricing changes, or policy shifts that create openings.
- **Industry shifts**: Search for emerging trends, certification launches, technology transitions, or regulatory changes that create demand.
- **Distribution opportunities**: Search for channels, communities, or platforms with growing audiences that match the target persona.
- **AI and technology tailwinds**: Search for how AI or other technology shifts are creating new needs or elevating existing ones.

### Rules

- Minimum 4 opportunities, each with specific evidence.
- Each opportunity must be external (not something the operator can create, but something they can exploit).
- Cite specific data: market growth percentages, competitor pricing, platform statistics, community sizes.
- Score each as high/medium/low impact.

---

## Phase 5: Threats Research (External, Negative)

Identify external headwinds that could kill the hypothesis. These are market forces that work against success.

### What to research (via web search):

- **Established player moves**: Search for what the biggest competitors are doing right now. Could they easily ship a competing product? What is their current trajectory?
- **AI displacement**: Search for whether AI tools are already solving or could soon solve the problem the product addresses. How good are free AI alternatives?
- **Free content floor**: Search for the quality and quantity of free alternatives. How high is the floor the product must clear?
- **Economic conditions**: Search for L&D budget trends, individual spending patterns, and economic conditions affecting the target audience's willingness to spend.
- **Platform risk**: Search for platform stability, pricing changes, reputation issues, and vendor lock-in risks for the chosen distribution channel.
- **Cold-start death spiral**: Search for failure patterns specific to the product type, format, and distribution model. What is the most common way this type of product dies?

### Rules

- Minimum 4 threats, each with specific evidence.
- At least one threat must address the "what kills most products like this" scenario.
- Do NOT be optimistic. Threats are threats. If a well-funded competitor could ship a better version in two weeks, say so.
- Score each as high/medium/low impact.

---

## Phase 6: Synthesis

The synthesis is the verdict. It must be one of four outcomes:

| Verdict | Meaning | Next Step |
|---------|---------|-----------|
| `proceed` | Hypothesis is strong. Ship it as specified. | Go directly to `offer-scope` |
| `proceed-with-modifications` | Hypothesis is sound but needs specific changes. | Apply modifications, then go to `offer-scope` |
| `pivot` | Core insight is valid but the hypothesis as stated will fail. | Reformulate hypothesis, re-run SWOT |
| `kill` | Hypothesis has fatal weaknesses. Do not invest build time. | Return to `persona-extract` or `signal-scan` |

### Synthesis Rules

- State clearly WHAT IS RIGHT about the hypothesis (which strengths and opportunities are real).
- State clearly WHAT IS WRONG about the hypothesis (which weaknesses and threats are fatal or near-fatal).
- If the verdict is `proceed-with-modifications`, list specific, actionable modifications. Not "improve marketing" but "Launch on Skool Hobby plan ($9/mo) instead of Pro ($99/mo) to validate community demand with minimal burn."
- If the verdict is `pivot`, explain what the pivot looks like. What changes and what stays the same?
- If the verdict is `kill`, explain why plainly. "The free content floor is too high for this format at this price" is a valid kill reason.
- The synthesis must weigh WEAKNESSES and THREATS heavily. Optimism bias is the enemy. If 3 of 4 strengths are valid but 2 threats are existential, the existential threats dominate.

---

## Phase 7: Risk Registry

For each identified risk (drawn from weaknesses and threats), create a monitoring entry:

| Field | Description |
|-------|-------------|
| risk | What could go wrong (one sentence) |
| metric | What number or signal to watch |
| threshold | At what value does this become a problem |
| timeframe | When to check (e.g., "0-90 days", "Month 2+") |
| monitoring_method | How to measure (specific tool, platform, or method) |

### Risk Registry Rules

- Minimum 4 risks, maximum 8.
- Every risk must be specific and measurable. "Market conditions change" is not a risk. "GitHub repo fails to reach 500 stars within 90 days" is a risk.
- Include at least one risk per SWOT quadrant (weakness-derived and threat-derived).
- Each risk must have a concrete monitoring method -- not "keep an eye on it" but "check GitHub Insights weekly for star velocity."

---

## Phase 8: Moat Assessment

Evaluate what could become defensible and on what timeline.

### Assessment Structure

**Current moat strength**: One of `none`, `thin`, `emerging`, `moderate`, `strong`.

**What is NOT a moat**: List things the operator might think are defensible but are not (e.g., "the content itself", "the GitHub templates", "being first").

**What COULD become a moat**: List potential moat sources with realistic timelines:
- What specific power (from Helmer's 7 Powers) could emerge?
- What would need to happen for it to emerge?
- How long would it take?

**Moat timeline**:
- **Months 0-6**: What is the moat situation? (Usually: none. Competing on positioning and content quality.)
- **Months 6-12**: What could emerge? (Usually: brand recognition, early community network effects.)
- **Months 12-24**: What becomes real? (Usually: moderate moat if community reaches critical mass.)
- **Months 24+**: What is the endgame? (What does strong defensibility look like for this specific product?)

### Moat Assessment Rules

- Be realistic. Most indie products have NO moat in months 0-6. Say so.
- Do not confuse "hard to build" with "defensible." A product that took you 6 months to build but can be replicated in 2 weeks is not a moat.
- The moat assessment must connect to Helmer's 7 Powers. Which power(s) are plausible, and which are not?

---

## Output

The SWOT analysis produces two files:

### 1. JSON Spec

**Vault path**: `Admin/Product-Discovery/SWOT/{domain-slug}-{YYYY-MM-DD}.json`

Structured data following the schema in [references/output-schema.json](references/output-schema.json). Must validate against that schema.

### 2. Markdown Summary

**Vault path**: `Admin/Product-Discovery/SWOT/{domain-slug}-{YYYY-MM-DD}.md`

Human-readable SWOT report with the following structure:

```markdown
---
type: swot-analysis
date: YYYY-MM-DD
status: complete
tags:
  - hunter/swot
  - hunter/domain/{domain-slug}
  - hunter/opportunity/{opportunity-slug}
persona_ref: "{persona-slug}"
decision_ref: "{decision-slug}"
signal_scan_ref: "{signal-scan-slug}"
---

# SWOT Analysis: [Product Name]

**Date**: [date]
**Domain**: [domain]
**Opportunity**: [opportunity]
**Hypothesis**: "[full hypothesis statement]"
**Brand Thesis**: "[brand thesis]"

---

## STRENGTHS (Internal, Positive)

### S1: [Strength Title]
[Evidence-backed description with citations]
[...minimum 4 total, each with evidence + impact rating]

## WEAKNESSES (Internal, Negative)

### W1: [Weakness Title]
[Evidence-backed description with citations]
[...minimum 4 total, each with evidence + impact rating]

## OPPORTUNITIES (External, Positive)

### O1: [Opportunity Title]
[Evidence-backed description with citations]
[...minimum 4 total, each with evidence + impact rating]

## THREATS (External, Negative)

### T1: [Threat Title]
[Evidence-backed description with citations]
[...minimum 4 total, each with evidence + impact rating]

---

## SWOT Synthesis: Should We Proceed, Pivot, or Kill?

### Verdict: [PROCEED | PROCEED WITH MODIFICATIONS | PIVOT | KILL]

**What is right about this hypothesis:**
- [point 1]
- [point 2]

**What is wrong about this hypothesis:**
- [point 1]
- [point 2]

### Recommended Modifications (if applicable)

1. [Specific modification with reasoning]
2. [Specific modification with reasoning]

---

## Risk Registry

### Risk 1: [Risk Name] ([Timeframe])
**Metric**: [what to watch]
**Threshold**: [at what value to act]
**Monitoring**: [how to measure]

### Risk 2: [Risk Name] ([Timeframe])
[...]

---

## Moat Assessment

**Current moat strength**: [none/thin/emerging/moderate/strong]

### What Is NOT a Moat
- [item 1]
- [item 2]

### What COULD Become a Moat
- [potential moat source + timeline]
- [potential moat source + timeline]

### Moat Timeline
- **Months 0-6**: [assessment]
- **Months 6-12**: [assessment]
- **Months 12-24**: [assessment]
- **Months 24+**: [assessment]

### Bottom Line
[1-2 paragraph honest assessment of the hypothesis viability and timeline]

---

## Sources

- [All sources cited in the analysis, with URLs]

## References

- **Persona**: [[Admin/Product-Discovery/Personas/{persona-slug}]]
- **Decision Log**: [[Admin/Product-Discovery/Decisions/{decision-slug}]]
- **Signal Scan**: [[Admin/Product-Discovery/Signal-Scans/{signal-scan-slug}]]
```

---

## Vault Output Contract

Both output files are written to the Obsidian vault (iCloud-synced):

```
${VAULT}/Admin/Product-Discovery/SWOT/
```

- Filename format: `{domain-slug}-{YYYY-MM-DD}.md` and `{domain-slug}-{YYYY-MM-DD}.json`
- If a file already exists at the target path: APPEND under `## Update: {ISO timestamp}`, do NOT overwrite
- Frontmatter MUST include: `type: swot-analysis`, `date`, `status: complete`, `tags` (minimum: `hunter/swot`)

---

## Resources

### references/

- `output-schema.json` -- JSON Schema for the structured SWOT analysis output. Load when producing the JSON file to validate against.

### README.md

- The full Hypothesis Stress Test (HST) framework reference, including intellectual lineage (Humphrey, Porter, Horowitz, Helmer, Grove, Ries, Klein), detailed methodology, anti-patterns, and calibration examples. Consult for deep framework questions during a SWOT session.

---

## Quality Checklist

Run this checklist before delivering the SWOT:

- [ ] Hypothesis is concrete and falsifiable (product, format, price, audience, distribution, brand thesis all stated)
- [ ] Minimum 4 strengths, each with specific cited evidence (not vibes)
- [ ] Minimum 4 weaknesses, each with specific cited evidence (not softened)
- [ ] Minimum 4 opportunities, each with specific cited evidence (external forces only)
- [ ] Minimum 4 threats, each with specific cited evidence (not minimized)
- [ ] Web search was performed for EACH quadrant -- no quadrant relies solely on prior knowledge
- [ ] Every SWOT point has an impact rating (high/medium/low)
- [ ] Synthesis verdict is one of: proceed, proceed-with-modifications, pivot, kill
- [ ] If proceed-with-modifications, specific actionable modifications are listed
- [ ] Synthesis weighs weaknesses and threats honestly -- optimism bias is checked
- [ ] Risk registry has 4-8 specific, measurable risks with thresholds and monitoring methods
- [ ] Moat assessment is realistic (most indie products have no moat in months 0-6)
- [ ] Moat assessment references Helmer's 7 Powers by name
- [ ] JSON output validates against `references/output-schema.json`
- [ ] Markdown output has correct frontmatter (type, date, status, tags, persona_ref, decision_ref, signal_scan_ref)
- [ ] Both files are saved to vault `Admin/Product-Discovery/SWOT/`
- [ ] All upstream references (persona_ref, decision_ref, signal_scan_ref) are linked
- [ ] Next-step hint is populated for offer-scope with validated strengths, key risks, and recommended modifications
