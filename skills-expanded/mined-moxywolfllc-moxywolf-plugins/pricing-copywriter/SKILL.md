---
name: pricing-copywriter
description: >
  This skill should be used when the user says "write pricing page copy",
  "create a pricing page", "pricing page design", "write tier descriptions",
  "pricing FAQ", "how should I present my pricing", "pricing page conversion",
  "pricing comparison table", "feature comparison copy", "pricing CTA copy",
  "upgrade prompt copy", "downgrade prevention copy", "annual vs monthly copy",
  "pricing announcement email", "price increase communication", or any request
  to write the customer-facing copy, page structure, or communication
  materials for a pricing page or pricing change. This skill turns a pricing
  model into persuasive, conversion-optimized customer-facing content. Use
  this after pricing-modeler has produced the tier definitions and price points.
version: 0.1.0
---

# Pricing Copywriter

Transform a pricing model into conversion-optimized, customer-facing pricing content — page copy, comparison tables, FAQs, upgrade prompts, and pricing change communications.

## Prerequisites

This skill works best with output from pricing-modeler (tier definitions, price points, feature gates). If none exists, gather the basics: what tiers exist, what each costs, and what's in each.

## Pricing Page Architecture

### The Conversion-Optimized Page Structure

Build the pricing page in this order:

#### 1. Headline + Subheadline
The headline should answer "why should I pay?" not "how much does it cost?"

**Good**: "Compliance confidence at every scale"
**Bad**: "Our pricing plans"

The subheadline addresses the primary pricing objection for your audience.

**Good**: "Start free. Upgrade when your team grows. No surprises."
**Bad**: "Choose the plan that's right for you."

#### 2. Billing Toggle
Annual vs. monthly toggle. Always default to annual (it's what you want them to pick).

Copy for annual savings badge:
- "Save 20%" (clear, simple)
- "2 months free" (feels like a gift)
- "Best value" (if discount is significant)

Never show just the annual price without context. Show the monthly equivalent.

#### 3. Tier Cards
Each tier card follows this structure:

```
[TIER NAME]
[One-line description of who this tier is for]
[$XX/mo] billed annually (or $XX/mo billed monthly)

[Primary CTA button]

[3-5 key features with benefit framing]
- [Feature] — [why it matters]
- [Feature] — [why it matters]
- Everything in [Previous Tier], plus:
- [Differentiating feature]
```

#### 4. The "Recommended" Signal
The middle/primary tier should be visually differentiated:
- Larger card or highlighted border
- "Most Popular" or "Recommended" badge
- Different CTA color (higher contrast)
- Positioned in the center

#### 5. Feature Comparison Table
Below the tier cards, a detailed comparison for evaluators who need specifics.

Design principles:
- Group features by category (Core, Collaboration, Security, Support)
- Use checkmarks, X marks, and specific limits (not just Y/N)
- Highlight the row that most differentiates tiers
- Make it scannable — use consistent formatting

#### 6. Social Proof Section
Positioned between pricing and FAQ:
- Customer logos (sorted by recognizability)
- Testimonials that specifically mention value/ROI
- "Trusted by X,000 teams" or equivalent
- Case study snippets with concrete numbers

#### 7. FAQ Section
Address the top objections and questions. Typical sections:

Read `references/pricing-faq-templates.md` for a library of proven FAQ copy.

#### 8. Final CTA
Repeat the primary CTA after the FAQ. For B2B SaaS:
- "Start your free trial" (if free trial exists)
- "Get started for free" (if freemium)
- "Talk to sales" (if enterprise-focused)

## Tier Description Copy

### Writing Principles

**Lead with the buyer, not the feature.**
- Good: "For growing teams that need compliance automation"
- Bad: "Includes automated scanning and team management"

**Use specifics, not superlatives.**
- Good: "Manage up to 500 assets with priority support"
- Bad: "Our best plan for serious businesses"

**Frame limits as capability, not restriction.**
- Good: "5 team members included"
- Bad: "Limited to 5 team members"

**The upgrade trigger should be implicit in the tier description.**
- Starter: "For individuals and small teams getting started with compliance"
- Pro: "For teams scaling compliance across multiple frameworks"
- Enterprise: "For organizations with complex compliance requirements and dedicated support needs"

### CTA Button Copy by Tier

| Tier | Primary CTA | Alternative |
|------|------------|-------------|
| Free | "Get started free" | "Create free account" |
| Starter | "Start free trial" | "Try Starter free" |
| Pro | "Start free trial" | "Upgrade to Pro" |
| Enterprise | "Contact sales" | "Request a demo" |

Avoid:
- "Buy now" (too aggressive for SaaS)
- "Subscribe" (too transactional)
- "Learn more" (too passive — save for secondary CTA)

## Pricing Communication Templates

### Price Increase Announcement

When raising prices, communicate with transparency and respect:

```
Subject: Changes to [Product] pricing — effective [date]

[Name],

We're writing to let you know about upcoming changes to [Product] pricing,
effective [date].

[What's changing]
Your [Tier] plan will move from $X/mo to $Y/mo (a [Z]% increase).

[Why]
Over the past [period], we've [invested in / shipped / improved]:
- [Concrete improvement 1]
- [Concrete improvement 2]
- [Concrete improvement 3]

This investment allows us to [outcome that matters to them].

[What's NOT changing]
- Your current features and limits remain the same
- [Any grandfathering or grace period]
- [Lock-in option if available: "Lock in your current rate for 12 months by switching to annual billing before [date]"]

[Support]
If you have questions, reply to this email or [reach out to support].
We're committed to making [Product] worth every dollar.

[Name]
[Title]
```

### New Feature Justifying Price

When a major feature launch accompanies a price change:

```
Subject: [Feature] is here — and [Plan] just got better

[Name],

Big news: [Feature] is now live in [Product].

[What it does — one sentence, benefit-framed]

[Feature] is included in your [Tier] plan at no additional cost.

Starting [date], [Tier] pricing moves to $X/mo (from $Y/mo) to reflect
the expanded capabilities. As a current customer, you'll keep your
current rate until [date].

[CTA to try the feature]
```

## Upgrade & Expansion Copy

### In-App Upgrade Prompts

When a user hits a tier limit:

```
You've reached your plan's [limit type] limit.

Upgrade to [Next Tier] to:
- [Primary benefit of upgrading]
- [Secondary benefit]
- [Quantified improvement: "Manage up to X assets"]

[Upgrade now] [View plans]
```

### Downgrade Prevention

When a user initiates a downgrade:

```
Before you switch to [Lower Tier], here's what you'll lose:

- [Feature they actively use] (used X times this month)
- [Feature they actively use] (X team members rely on this)
- [Limit change] (your current usage: X, [Lower Tier] limit: Y)

[Keep current plan] [Continue downgrade]
```

Use actual usage data when available — "You used API access 47 times this month" is more persuasive than "You'll lose API access."

## Compliance/Defense Vertical Copy Considerations

For STIGViewer and defense-adjacent products:

**Tone adjustments:**
- More formal than typical SaaS (avoid "awesome," "supercharge," "game-changing")
- Emphasize reliability, accuracy, and compliance over speed and convenience
- Use procurement-friendly language ("annual subscription," "volume licensing")
- Reference standards and certifications explicitly

**Trust signals that matter in this vertical:**
- FedRAMP status
- IL4/IL5 authorization
- SOC 2 Type II
- CMMC certification level
- GSA Schedule listing
- Existing defense contractor customers (with permission to name)

**Pricing page additions for gov/defense:**
- "Government pricing available" link
- Volume/site licensing information
- Procurement-friendly terms (NET30/60, PO acceptance)
- "Schedule a compliance briefing" CTA alongside standard demo CTA

Read `references/compliance-copy-patterns.md` for defense-vertical-specific language patterns.
