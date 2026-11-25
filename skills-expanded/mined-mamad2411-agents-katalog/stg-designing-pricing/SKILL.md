---
name: stg-designing-pricing
description: Develops pricing hypothesis using value-based methodology, tier architecture, and mode-specific constraints. Use when constructing unit economics during BUILD phase 2.
serves: strategist
domain: pricing-strategy
affects: unit-economics-hypothesis
depends-on: none
produces: pricing inputs for unit economics hypothesis
---

# Pricing Design

Develop pricing hypothesis using value-based methodology. All WTP estimates are T3 (always). Prices are ranges, not points. Channel economics integrated.

## Procedure

### Step 1: Calculate Value Anchor [S]

Read: problem hypothesis (quantified cost of the problem).

Value = problem cost x percentage resolved by solution.
Price ceiling = value x capture rate (10-25% for SaaS).

Present as range. Label T2 (derived from problem cost estimate which may itself be T2).

Produce: value anchor range [T2].

**Gate:** `value_anchor_calculated: bool` -- derived from quantified problem cost, not asserted.
- Pass: Step 2.
- Fail: If problem cost is not quantified, estimate from severity score and segment characteristics. Note increased uncertainty (T2-T3).

### Step 2: Analyze Competitive Pricing [S]

Read: competitor profiles from stg-analyzing-competition.

Map competitor pricing:
- Tiers and price points (from pricing pages)
- Packaging model (per-seat, usage, flat)
- Free tier availability and limits

Identify price gaps (underserved price ranges).

Produce: competitive pricing map [T1] + gap analysis [T2].

**Gate:** `competitive_pricing_mapped: bool` -- at least 2 competitors' pricing documented with source URLs.
- Pass: Step 3.
- Fail: If competitor pricing is hidden (enterprise "contact us"), note as data gap. Use available benchmarks for the category.

### Step 3: Select Revenue Model [R]

Match revenue model to growth architecture:

| Growth Architecture | Revenue Model | Rationale |
|--------------------|---------------|-----------|
| PLG | Freemium or usage-based with paid conversion | Users must experience value before paying |
| Network | Free tier with network-gated premium | Network value increases with users; premium unlocks at density |
| Traditional | Subscription (monthly/annual) | Sales-assisted, predictable revenue |
| Hybrid | Base subscription + usage overage | Predictable base with upside from usage |

Mode overlay:
- BOOTSTRAP: biases toward immediate revenue (no extended free tiers)
- VENTURE: can sustain longer free periods if growth loop is strong

Produce: revenue model selection with rationale.

**Gate:** `model_selected: bool` -- revenue model matches growth architecture with documented rationale.
- Pass: Step 4.
- Fail: If growth architecture not yet selected, flag dependency. Use segment ACV range to infer likely model.

### Step 4: Design Tier Architecture [K-grounded]

**Grounded in:** revenue model, value anchor, competitive pricing, segment characteristics.

Apply Good-Better-Best framework:
- **Good** = entry point (free or low friction)
- **Better** = main revenue driver (2-3x Good price). 60-70% of customers should land here.
- **Best** = price anchor (3-5x Better price). Anchors perception; captures high-value users.

For PLG: define free tier value + natural upgrade pressure points. Free must deliver value but not full value.

**Channel constraint check:**

| ACV Range | Viable Channels | Implication |
|-----------|----------------|-------------|
| < $1K | Near-zero-touch only (self-serve, content, SEO) | Cannot afford sales; product must sell itself |
| $1K-$10K | Light-touch (inside sales, webinars, trials) | Limited sales capacity; product-led assists |
| > $10K | Sales-assisted viable (demos, pilots, account executives) | Can invest in sales process |

Produce: tier structure with price ranges [T2 for tiers, T3 for conversion rates].

**Gate:** `tiers_designed: bool` -- tiers follow Good-Better-Best with rationale, channel constraint check completed.
- Pass: Step 5.
- Fail: If tiers do not follow framework, justify the deviation. If channel constraint check reveals ACV-channel mismatch, flag for resolution.

### Step 5: Define Upgrade Triggers [K-grounded]

**Grounded in:** tier structure, growth architecture.

For each tier boundary, define what triggers upgrade:
- Usage limits (API calls, storage, users)
- Feature gates (advanced features, integrations)
- Team expansion (per-seat triggers)
- Time limits (trial expiry)

Each trigger is a hypothesis -- conversion rate estimates are T3.

Produce: upgrade trigger list [T3 for effectiveness].

**Gate:** `triggers_defined: bool` -- at least 1 trigger per tier boundary, each labeled T3 for conversion predictions.
- Pass: Step 6.
- Fail: Triggers that are purely time-based without value connection are weak. Add at least one usage-based trigger.

### Step 6: Validate Pricing-Economics Coherence [R]

Check: does the price range support required LTV:CAC?

| Mode | LTV:CAC Required | Payback Required |
|------|-----------------|-----------------|
| VENTURE | > 3x | < 18 months |
| BOOTSTRAP | > 5x | < 6 months |

If pricing cannot meet thresholds, flag conflict: "At [price range], achieving [required LTV:CAC] requires CAC below [$X]. This constrains channel strategy to [channels]."

Produce: coherence check result.

**Gate:** `coherence_validated: bool` -- threshold check completed with explicit pass/fail.
- Pass: Done. Pricing inputs ready for unit economics.
- Fail: If coherence fails, report as finding. Do not adjust pricing to make numbers work without justification.

## Quality Criteria

- Value anchor derived from quantified problem cost (not asserted)
- Competitive pricing cites specific competitor price points with sources
- Revenue model aligned with growth architecture (not arbitrary)
- All WTP estimates labeled T3 with explicit note: "requires customer validation"
- Price ranges, not point prices
- Channel viability check performed (ACV vs channel type)
- Mode-specific thresholds checked

## Failure Modes

| Mode | Signal | Recovery |
|------|--------|----------|
| Pricing by competitor mimicry | Price set at competitor average without value-based justification | Calculate value anchor first. Competitor pricing is context, not methodology |
| WTP presented as known | Price stated without T3 label or "customers will pay" language | All WTP is T3 until sales data exists. Reframe as hypothesis |
| Free tier too generous | Free tier delivers full core value with no natural upgrade pressure | Identify the specific usage limit or feature gate that creates upgrade motivation. Free must deliver value but not full value |

## Boundaries

**In scope:** Value-based pricing methodology, tier architecture (Good-Better-Best), revenue model selection, upgrade trigger definition, channel-ACV constraint check, mode-specific threshold validation, competitive pricing analysis.

**Out of scope:** LTV/CAC calculation (stg-calculating-economics), market sizing (stg-sizing-markets), solution design (stg-designing-solutions), customer willingness-to-pay validation.
