---
name: superforge-biz
description: >
  Decide whether a market is worth entering, then architect the business model
  on top of it. Opens with a GO/NO-GO gate: TAM/SAM/SOM computed both ways,
  confidence tiers on every input, and the reverse calculation asking how many
  customers this needs and whether you can reach that many. Then monetization
  archetype, price anchoring, paywall placement, growth loops, channel-market
  fit, minimum viable scale per tactic, and quantifying value (time saved, cost
  avoided, revenue captured) as a pitch instead of an adjective. Also covers
  selling capacity rather than a product — revenue ceiling, scope as the
  deliverable, retainers, client concentration — and outreach legality. Use
  when the user says "pricing", "monetization", "paywall", "subscription",
  "business model", "revenue", "GTM", "market size", "TAM", "worth building",
  "customer acquisition", "agency", "retainer", "cold email", "価格", "課金",
  "マネタイズ", "ビジネスモデル", "市場規模", "儲かるのか", "顧客獲得", "受託",
  "見積もり", or runs /superforge-biz.
license: MIT
metadata:
  author: Takao Umehara
  version: "4.1"
compatibility: >
  Standalone.
  Reads docs/product-idea.md and docs/brief.md when present, writes docs/business-model.md.
---

# Superforge Biz — Business Architecture & Monetization Engine

Use this skill whenever defining monetization models, pricing tiers, paywall placements, or business growth loops. This engine turns product ideas into sustainable, high-margin software businesses.

---

## 0. The gate — is this market worth entering at all

Everything below assumes the answer is yes. Check it first, because a perfect
pricing model for a market that cannot support one person is a wasted month.

Three questions, in this order:

1. **How many customers does this actually need?**
   `必要な年間売上 ÷ (価格 × 継続率)`. Run this before any market-size figure —
   a large TAM reliably stops everyone, models included, from asking whether a
   path to those customers exists.
2. **Is the market big enough, computed both ways?** Top-down and bottom-up.
   The gap between them is the finding; if they differ by an order of
   magnitude, one assumption is wrong and you need to know which.
3. **Can you get in, and does getting in protect you?** Every barrier is a cost
   before revenue and a moat after it. A market with no barriers is a warning,
   not an opportunity.

End with a verdict code, never with prose: `GO` / `GO/NARROW` / `NO-GO/TOO-SMALL`
/ `NO-GO/NO-PATH` / `NO-GO/LOCKED` / `WAIT`. A `WAIT` carries the one-sentence
condition that would change it, and that sentence is the same one
`superforge-brain` stores on its Lab shelf.

Full method — the two-directional math, the A/B/C/D confidence tiers on every
input, maturity staging, and which mature markets remain enterable →
**`references/market-sizing.md`**. Run it after `superforge-brain`'s market
pass, never before: sizing a market before the ideas exist collapses the idea
space, which is the exact failure that skill's §8 is built to prevent.

---

## 1. Monetization Archetype Selection

Evaluate the product against 4 core revenue mechanics and select the primary driver:
- **Freemium & Feature Paywall**: Free entry with high-value feature gates (e.g. usage limits, advanced exports, pro automation).
- **Recurring Subscription (SaaS)**: Tiered monthly/annual plans with clear value metrics (per-seat, per-usage, or feature-tier).
- **Usage-Based / Metered**: Pay-as-you-go based on consumed computational or API value.
- **B2B Enterprise / Custom**: High-touch licensing, dedicated support, custom integrations, and SLA guarantees.

---

## 2. Paywall & Value-Gate Engineering

When designing in-app paywalls and conversion triggers:
1. **Value Anchor**: Highlight the single primary ROI/time-saving benefit before showing price.
2. **Frictionless Trial**: Offer zero-friction entry (e.g. 7-day trial with instant value demonstration before hard gate).
3. **Paywall Placement**: Position paywalls at moments of peak user delight or achievement (e.g., right after generating a successful output).
4. **Win-Back & Retention**: Define downgrade/cancellation flows with dynamic discount offers or tier-down options.

What these look like on a concrete screen — smart defaults and 「◯件の結果を表示」,
reciprocity (show the result before the account wall), the trial-timeline
paywall shown in the first session, booking totals on the commit button, and
D2C product pages — each tagged with its evidence tier so a C is tested, not
promised → **`references/conversion-patterns.md`**.

---

## 3. Unit Economics & Growth Engine

Structure the unit economics framework:
- **Core Value Metric**: What single metric scales as the customer gets more value? (e.g. active projects, generated assets, team members).
- **Growth Loops**: Build product-led viral loops (e.g., shared links, branded exports, collaborative invites).
- **Go-To-Market (GTM) Blueprint**: Identify primary launch channels, launch positioning, landing page messaging, and conversion funnel milestones.

**Check every tactic against its minimum viable scale before recommending it.**
A/B testing at 200 sessions a month, win-back campaigns with 12 churned users,
or paid acquisition before the conversion rate is known do not underperform —
they return no interpretable signal at all, while costing the same weeks. The
thresholds, and what to do instead below each one, are in
`references/customer-acquisition.md` §6. Saying 「その規模ではこれは効きません」
is part of the advice, not a failure to give it.

---

## 4. Customer Acquisition — before there's a loop to grow

§3's growth loops assume a customer already exists. Getting the first ones is
a different problem: which channel actually fits this product (price point,
sales cycle, buyer type), what makes a lead magnet convert instead of being
ignored, how to tell a real lead from a vanity one, and the back-of-envelope
CAC/LTV math that stops a channel from quietly losing money. Full framework,
the channel-market-fit matrix, and the first-10-customers playbook (when
there's no case study yet to make a scalable channel credible) →
**`references/customer-acquisition.md`**.

## 4b. When the business sells capacity, not a product

§1–§3 assume a product: build once, sell many times. A service business — 受託,
an agency, a retainer, consulting — inverts that, and it is the most common way
an indie maker funds a product. Its revenue ceiling is **arithmetic**
(稼働可能時間 × 単価 × 稼働率), not a market, and it is lower than it feels.
Compute it before advising a revenue target the equation forbids.

Three things decide whether it works, and none of them are in §1–§3: **the scope
sentence is the product** (artifacts, revision count, exclusions, and an end
condition — a project with no defined end does not end); **scope creep, not
underpricing, is the largest loss driver**, and the fix is to price every
out-of-scope request out loud rather than absorb it; and **one client above 50%
of revenue is an employer, not a customer.** Full model, including project
versus retainer, the three conditions that must all hold before pricing on
outcome instead of time, and the bridge from a service ceiling to a product →
**`references/service-business.md`**.

## 5. The Value Pitch — quantify it, or it's an adjective

"良いオートメーションがあります" is a spec sheet, not a pitch. Every value claim
reduces to one of four levers — time saved, cost avoided, revenue captured,
risk reduced — each with a formula that turns the feature into the
*customer's own number*, stated before the price and paired with the one
specific human moment that number changes. This is the discipline behind
§2's "Value Anchor" step, and the discovery questions that get the real
numbers before the pitch is written → **`references/value-pitch.md`**.

---

## Deeper reference

**`references/market-sizing.md`** — the GO/NO-GO gate: two-directional TAM math
and what their disagreement reveals, A/B/C/D confidence tiers on every input,
the reverse calculation (how many customers this actually needs, and whether
you can reach that many), maturity staging, entry barriers read as both cost
and moat, and the six verdict codes.

The mechanisms behind pricing, anchoring, trials, defaults, and paywall
placement — and the ethical line on each — are in
**`references/behavioral-frameworks.md`**. It also carries the three-part
diagnosis of why nobody acted (理由 / 容易さ / 合図), the symptom index for
picking a mechanism from what is actually going wrong, and the list of widely
recommended tactics this suite deliberately does not use.

**`references/conversion-patterns.md`** — the frameworks applied screen by
screen: six mechanisms as concrete decisions with their honest limits, the
subscription paywall (timeline, not feature list), booking, and e-commerce
patterns, every row tiered A/B/C/D.

**`references/customer-acquisition.md`** — channel-market fit, lead magnets,
fit×intent qualification, CAC/LTV sanity math, minimum viable scale per tactic,
the first-10-customers playbook, and the legality of outreach (§8 — the rule
follows the recipient's location, and scraped lists cost the sending domain
more than they ever return).

**`references/service-business.md`** — the revenue ceiling and the only four
levers that raise it, scope as the actual deliverable, scope creep priced
rather than absorbed, project versus retainer, client concentration thresholds,
and when pricing may move off time.

**`references/value-pitch.md`** — the four value levers and their formulas,
the logic-then-emotion pitch structure, the credibility checklist, and the
discovery questions that fill in the numbers before the pitch is written.

## Artifact

Write `docs/business-model.md`. Read `docs/product-idea.md` first if it
exists; the monetization archetype follows from the product shape, not the
other way round. It must open with a `## Market` section carrying the §0
verdict code (from `references/market-sizing.md`) — a pricing model written
above an unstated NO-GO is the most expensive document in the repository. Then
include an `## Acquisition plan` section (from §4) and a `## Value pitch`
section (from §5): a business model with a price but no way to reach or
convince a customer is only half the artifact. When the business sells capacity
rather than a product, add a `## Service model` section (from §4b) carrying the
ceiling, the scope shape, and the concentration number.

If `superforge-brain` ran, its quadrant travels with the idea. A **Workhorse**
arriving here needs §0 pointed at the win-path code rather than at novelty; a
`WAIT` verdict here goes back to that skill's Lab shelf with its condition
attached, rather than being reported as a dead end.

## Delegate when a sharper skill is installed

`monetization`, `indie-business` (models) · `paywall-generator`,
`subscription-offers`, `offer-codes-setup` (surfaces) ·
`subscription-lifecycle`, `win-back-offers`, `referral-system` (retention) ·
`launch-strategy`, `growth`, `marketing-strategy`, `marketing-psychology` (GTM) ·
the `sales-*` family (B2B) · `app-store`, `product-page-optimization`,
`apple-search-ads`, `keyword-optimizer` (store) · `legal`, `privacy-policy`.
