---
name: positioning-statement
description: "Generates and critiques product positioning using April Dunford's \"Obviously Awesome\" methodology and Geoffrey Moore's classic positioning template. Helps PMs articulate who the product is for, what category it competes in, and why it wins."
category: strategy
default_depth: standard
---

# Positioning Statement

Read `docs/workflow-contract.md` once per session before applying this skill. Resolve it from the nearest ancestor of this file containing `manifest.json`; all Shipwright paths are relative to that root.

## Description

Generates and critiques product positioning using April Dunford's "Obviously Awesome" methodology and Geoffrey Moore's classic positioning template. Helps PMs articulate who the product is for, what category it competes in, and why it wins.

## When to Use

- Launching a new product or entering a new market
- Repositioning an existing product after a pivot
- Aligning marketing, sales, and product on messaging
- Preparing for competitive displacement campaigns

## Depth

| Scope | Use When | Sections to Include |
|---|---|---|
| **Light** | Internal alignment on messaging or quick positioning check | Competitive Alternatives, Unique Attributes, Value (UVP), Target Customer only |
| **Standard** | Product launch or repositioning effort | All 7 steps: Competitive Alternatives through Stress Test |
| **Deep** | Competitive displacement campaign or category creation | All steps + segment-specific positioning variants, message testing plan, sales enablement talk track |

**Omit rules:** At Light depth, skip Value Map, Market Category, and Stress Test. Produce only Competitive Alternatives, Unique Attributes, a one-line Value (UVP), and the target customer profile.

## Framework

### Step 1: Competitive Alternatives

Before positioning, understand what you're positioning *against*.

**Question:** If your product didn't exist, what would customers do instead?

```markdown
## Competitive Alternatives
| Alternative | Type | What it does well | Where it falls short |
|---|---|---|---|
| [Product A] | Direct competitor | [strength] | [weakness] |
| [Manual process] | Status quo | [it's free/familiar] | [slow, error-prone] |
| [Spreadsheet] | Workaround | [flexible] | [doesn't scale] |
```

### Step 2: Unique Attributes

What does your product have or do that alternatives don't?

**Rules:**
- Must be objectively true (not aspirational)
- Must be difficult for competitors to copy quickly
- Focus on capabilities, not features, what does it *enable*?

```markdown
## Unique Attributes
1. [Attribute 1], e.g., "Real-time collaboration with version history"
2. [Attribute 2], e.g., "Native integration with [ecosystem]"
3. [Attribute 3], e.g., "AI-powered [capability]"
```

### Step 3: Value (So What?)

Translate each unique attribute into customer value:

```markdown
## Attribute-to-Value Map
| Unique Attribute | Value to Customer |
|---|---|
| [Attribute 1] | [What this means for their workflow/outcome] |
| [Attribute 2] | [How this saves time/money/risk] |
```

### Step 4: Target Customer

Who cares the most about this value? Be specific.

```markdown
## Best-Fit Customer
**Characteristics:**
- [Company size / type]
- [Role / seniority]
- [Situation / trigger]

**Why they care more than others:**
- [Reason, e.g., "They face this problem daily, not monthly"]

**Who is NOT a good fit (right now):**
- [Segment], because [reason]
```

### Step 5: Market Category

What frame of reference helps the customer understand what you are?

**Three category strategies:**
1. **Existing category**, Compete head-to-head (e.g., "CRM")
2. **Subcategory**, Niche of an existing category (e.g., "CRM for real estate teams")
3. **New category**, Create a category (e.g., "Revenue Intelligence Platform")

```markdown
## Market Category
**Category:** [Name]
**Strategy:** [Existing / Subcategory / New]
**Rationale:** [Why this frame helps the customer understand us]
**Risk:** [What could go wrong with this framing]
```

### Step 6: Assemble the Positioning Statement

**Moore's Template:**
```
For [target customer]
who [statement of need or opportunity],
[product name] is a [market category]
that [key benefit / reason to believe].
Unlike [competitive alternative],
our product [primary differentiation].
```

**Dunford's Positioning Canvas:**
```markdown
| Element | Our Position |
|---|---|
| Competitive alternatives | [What customers would use instead] |
| Unique attributes | [What we have that they don't] |
| Value | [What our attributes enable for customers] |
| Target customers | [Who cares the most] |
| Market category | [Frame of reference] |
```

### Step 7: Stress-Test the Positioning

Evaluate the positioning against these questions:
- Does a target customer immediately understand what this is?
- Is the differentiation true, provable, and hard to copy?
- Does it pass the "so what?" test, is the value meaningful?
- Can sales use this in a cold outreach email?
- Would a customer describe us this way to a peer?

## Minimum Evidence Bar

**Required inputs:** Product name, at least two competitive alternatives (or status quo workarounds), and a described target customer.

**Acceptable evidence:** Customer interviews or win/loss data, competitor product pages or G2/Gartner reviews, sales call recordings, usage analytics showing differentiation, published analyst comparisons.

**Insufficient evidence:** If differentiation claims have no customer or market validation, stop and recommend running win/loss interviews or competitive teardowns before attempting this skill. Do not produce positioning with unvalidated differentiation claims.

**Hypotheses vs. findings:**
- **Findings:** Competitive Alternatives, Unique Attributes, and Target Customer characteristics must be grounded in observable market data or direct customer input.
- **Hypotheses:** Market Category choice and Stress Test predictions may be directional, must be labeled as positioning bets to validate.

## Output Format

Produce a positioning document with:
1. **Competitive Alternatives**, what exists today
2. **Unique Attributes**, what sets us apart
3. **Value Map**, attributes translated to customer outcomes
4. **Target Customer**, best-fit profile
5. **Market Category**, frame of reference
6. **Positioning Statement**, assembled statement
7. **Stress Test**, evaluation and refinements

**Shipwright Signature (required closing):**
8. **Decision Frame**, Recommended positioning to commit to, category strategy trade-off, confidence with evidence quality, owner, decision date, revisit trigger
9. **Unknowns & Evidence Gaps**, Unvalidated differentiation claims, untested category framing with buyers, assumed competitive weaknesses
10. **Pass/Fail Readiness**, PASS if positioning is grounded in multiple validated unique attributes and tested against real competitive alternatives (at Light depth: PASS if competitive context is established and Value (UVP) is grounded in at least one differentiator, full attribute validation is deferred); FAIL if differentiation is aspirational with no customer or market evidence
11. **Recommended Next Artifact**, Which Shipwright skill to run next and why

## Common Mistakes to Avoid

- **Positioning on aspirations**, Position on what's true today, not what you hope to build
- **Everyone is the target**, If your target is "all businesses," you have no positioning
- **Category is too broad**, "Software" is not a useful category; narrow until it's meaningful
- **Feature-led differentiation**, "We have feature X" is weak; "We enable outcome Y" is strong
- **Ignoring the competitive alternative**, You don't position in a vacuum; you position *against something*

## Weak vs. Strong Output

**Weak:**
> For businesses who need better data, DataCo is an innovative platform that uses AI to provide insights. Unlike competitors, we are faster and more accurate.

No named segment, no specific value, "innovative" and "AI" are filler, "faster and more accurate" is unverifiable.

**Strong:**
> For mid-market e-commerce teams (50-500 SKUs) who lose 8-12% of revenue to stockouts during promotions, PlanCast is a demand forecasting tool that predicts promotional lift within 5% accuracy using historical POS data. Unlike manual spreadsheet planning, PlanCast updates forecasts daily and flags reorder points 72 hours before stockout risk.

Named segment with a quantified pain, specific mechanism, measurable differentiation, and a concrete competitive alternative.
