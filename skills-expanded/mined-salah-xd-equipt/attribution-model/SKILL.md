---
name: attribution-model
description: "Designs marketing attribution models with channel mapping, weighting logic, reporting recommendations, and implementation steps. Use when understanding which channels drive conversions."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Attribution Model

## When to Use This Skill

Use this skill when you need to:
- Understand which marketing channels drive the most conversions
- Choose an attribution model for budget allocation decisions
- Design a multi-touch attribution framework
- Report on marketing ROI by channel

**DO NOT** use this skill for setting up tracking pixels, configuring ad platforms, or building attribution software. This is for designing the model and reporting framework.

---

## Core Principle

PERFECT ATTRIBUTION IS IMPOSSIBLE — PICK A MODEL THAT IS GOOD ENOUGH TO MAKE BETTER BUDGET DECISIONS THAN GUESSING, AND BE HONEST ABOUT ITS LIMITATIONS.

---

## Phase 1: Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Channels** | "What marketing channels are you using? (paid ads, SEO, email, social, referral, direct)" | Must be provided |
| **Conversion type** | "What is a conversion? (purchase, signup, demo booking, lead form)" | Lead form submission |
| **Sales cycle** | "How long from first touch to conversion? (same day, days, weeks, months)" | 1-2 weeks |
| **Budget** | "Monthly marketing spend across all channels?" | $1,000-$5,000 |
| **Tracking setup** | "What tracking do you have? (UTMs, GA4, CRM, pixel tracking)" | GA4 + UTMs |
| **Decision need** | "What decision will this help you make? (where to spend more, what to cut)" | Budget allocation |

**GATE: Confirm brief before proceeding.**

---

## Phase 2: Design

### Model Selection

Present the options with pros and cons for the user's context:

| Model | How It Works | Best For |
|-------|-------------|----------|
| **Last touch** | 100% credit to final channel | Short sales cycles, simple setups |
| **First touch** | 100% credit to discovery channel | Understanding awareness drivers |
| **Linear** | Equal credit across all touchpoints | Fair baseline, multi-channel |
| **Time decay** | More credit to recent touches | Longer sales cycles |
| **Position-based** | 40% first, 40% last, 20% middle | Balanced awareness + conversion credit |
| **Data-driven** | Algorithmic based on actual paths | High volume, sophisticated setups |

### Recommended Model Logic

For most solopreneurs and small businesses: start with **position-based** or **last-touch** with a first-touch overlay report. Graduate to data-driven when you have 500+ conversions per month.

**GATE: Present model recommendation and wait for approval.**

---

## Phase 3: Build

### Deliverables

**1. Attribution Model Document**
- Selected model with rationale
- Channel map with all touchpoints and how they are tracked
- Weighting logic explained with examples
- Known blind spots and limitations

**2. Channel-Conversion Path Map**
- Typical customer journeys by channel combination
- Example paths: Social ad → Blog post → Email → Purchase
- Touchpoint definitions: what counts as a "touch" per channel

**3. Reporting Template**
- Monthly attribution report structure
- Metrics per channel: conversions, assisted conversions, cost per acquisition, ROAS
- Comparison: attributed conversions vs. platform-reported conversions (they will differ)

**4. Implementation Checklist**
- [ ] UTM parameters standardized across all channels
- [ ] GA4 conversion events configured
- [ ] CRM tracking connected (if applicable)
- [ ] Attribution window defined (7 days, 30 days, 90 days)
- [ ] First report generated and validated

---

## Phase 4: Polish

### Model Validation

After 30 days, check:
- Do the attribution numbers make intuitive sense given your spend and effort?
- Are any channels getting zero credit despite known activity?
- Does the model change your budget allocation decisions?

### Quarterly Review

Reassess the model fit every quarter as channels, spend, and volume change.

---

## Example 1: Solo Service Business (3 channels, short sales cycle)

**Channels:** Google Ads, Instagram organic, referral
**Model:** Last-touch (simple, decisive, sufficient for 3 channels)
**Report:** Monthly cost per lead by channel, compare to close rate

## Example 2: E-commerce Brand (6 channels, multi-touch)

**Channels:** Meta ads, Google ads, email, SEO, influencer, direct
**Model:** Position-based (40/20/40) with 30-day attribution window
**Report:** Weekly ROAS by channel, assisted conversion count, path analysis

---

## Anti-Patterns

- **Platform-reported only** — every ad platform takes full credit. Facebook and Google will both claim the same conversion. Use independent tracking.
- **Ignoring assisted conversions** — a channel with zero last-touch conversions may be generating all your first touches. Check assisted conversions before cutting.
- **Over-engineering early** — data-driven attribution with 50 monthly conversions is noise, not signal. Match model complexity to data volume.
- **Set and forget** — attribution models need recalibration as your channel mix changes.
- **Treating the model as truth** — all models are wrong. Use them to make *better* decisions, not perfect ones.

---

## Recovery

- **No UTM tracking in place:** Start tagging all links today. You cannot attribute what you do not track. Provide a UTM setup guide.
- **Too few conversions for multi-touch:** Use last-touch attribution and supplement with qualitative data ("How did you hear about us?" survey).
- **Platform numbers do not match GA4:** This is normal. Document the discrepancy and use one source of truth for decisions.
- **User wants to attribute everything perfectly:** Set expectations that 70-80% accuracy is excellent for attribution. Perfect is not achievable.
