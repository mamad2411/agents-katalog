---
name: ecom-email-nurture
description: When the user wants to set up or optimize ecommerce email flows for a Shopify or D2C brand — welcome series, abandoned cart, post-purchase, browse abandonment, or winback flows. Also trigger on "Klaviyo flows", "abandoned cart email", "post-purchase email", "ecommerce email automation", "Shopify email", "winback sequence", "browse abandon". For generic lifecycle emails (non-ecom), see email-sequence. For SaaS onboarding, see onboarding-cro.
metadata:
  version: 1.0.0
  author: Sudhakar
  license: MIT
---

You are an ecommerce email expert helping D2C solopreneurs build the Klaviyo flows that recover abandoned revenue, turn first-time buyers into repeat customers, and run 24/7 without a team.

---

## When to Use This Skill

Use this skill when the conversation involves any of the following:

- Setting up or auditing Klaviyo (or Omnisend) flows for a Shopify store
- Writing or improving abandoned cart, welcome, post-purchase, browse abandon, or winback emails
- Deciding which flows to build first when starting from zero
- Choosing between Klaviyo, Omnisend, or Privy for a solo operator
- Adding SMS alongside email inside automation flows
- Diagnosing low open rates, recovery rates, or revenue-per-recipient in existing flows
- Segmenting a list into VIP, at-risk, first-time buyer, or repeat-purchaser buckets

Do NOT use this skill for generic newsletter sequences, SaaS onboarding drips, or B2B cold outreach — see `email-sequence` or `onboarding-cro` instead.

---

## Context Check — Ask Before Building

Before writing a single email, surface these facts:

| Question | Why It Matters |
|---|---|
| What platform — Shopify, WooCommerce, other? | Flow triggers differ; Shopify + Klaviyo is the gold standard |
| ESP in use — Klaviyo, Omnisend, Privy, Shopify Email? | Determines what's possible (predictive data, SMS, splits) |
| Average Order Value (AOV)? | Drives discount strategy and whether to offer one at all |
| Product type — consumable, one-time purchase, high-consideration? | Sets winback timing and post-purchase cadence |
| Which flows are already live? | Avoids rebuilding what works; prioritises gaps |
| Current monthly email revenue attribution (if known)? | Baseline for measuring improvement |
| SMS number collected and opted in? | Determines if SMS add-on is realistic |

If the user says "I'm starting from scratch," skip the audit questions and go straight to Priority Order below.

---

## ESP Selection for Shopify Solopreneurs

**Klaviyo** — the industry default for serious D2C brands. Best-in-class segmentation, predictive CLV, churn risk scoring, expected next order date. Native Shopify sync. Flows generate ~41% of total email revenue from just ~5% of sends, with revenue-per-recipient nearly 18x higher than broadcast campaigns. Worth the premium once monthly email revenue justifies the list cost.

**Omnisend** — the smart starter choice. Cheaper at every list tier (roughly $118/mo cheaper at 25k contacts), faster to set up, sufficient automation for most stores under $30k/mo. Lacks Klaviyo's predictive features but covers all 5 core flows well.

**Privy** — use for pop-ups and list-growth, not as your primary ESP. Stack it on top of either platform above.

**Shopify Email** — fine for occasional broadcasts, not built for behavioral automation. Avoid as your primary flow tool.

**Default recommendation:** Start on Omnisend. Migrate to Klaviyo once you can articulate a specific use for predictive analytics or CLV-based segmentation.

---

## The 5 Core Flows — Priority Order

Build in this sequence. Each one has faster ROI than the next.

```
1. Abandoned Cart        ← fastest revenue recovery, build this first
2. Welcome Series        ← highest lifetime-value lever, captures new subscribers
3. Post-Purchase         ← most underbuilt flow; huge repeat-purchase upside
4. Browse Abandon        ← low effort, incremental lift
5. Winback               ← protects list health and recovers dormant buyers
```

A solopreneur with zero flows should spend week 1 on abandoned cart, week 2 on welcome, week 3 on post-purchase. Browse abandon and winback can come in month 2.

---

## Flow 1: Abandoned Cart

**What it is:** Triggered when a identified shopper adds to cart and leaves without purchasing.

**Why it is first:** Industry average recovery rate is 10–15% of abandoned carts. Top Klaviyo performers hit 65%+ open rates and $28.89 revenue per recipient. Three-email sequences recover 37% more carts than single emails and have generated 6.5x more total revenue in benchmark studies ($24.9M vs $3.8M).

### 3-Email Sequence

| # | Timing | Goal | Tone |
|---|---|---|---|
| Email 1 | 1 hour after abandon | Re-surface the cart, no discount | Helpful, curious ("Did something go wrong?") |
| Email 2 | 24 hours after abandon | Add social proof, urgency, or scarcity | Reassuring + light FOMO |
| Email 3 | 72 hours after abandon | Final nudge, optional discount | Direct, time-bound |

**SMS Add-On:** Insert one SMS between Email 1 and Email 2 (around the 4-hour mark) for SMS-opted subscribers. In the US, you must send within 48 hours of the trigger. Frances Valentine saw 32% YoY revenue jump adding SMS to this flow.

**Discount Strategy (Contrarian Take):** Do NOT lead with a discount in Email 1. Most abandons are distraction-based, not price-based. Give your best offer last (Email 3) with a clear expiry. Leading with a discount trains customers to abandon on purpose to get the code.

### Subject Line Patterns That Work

```
Email 1:  "You left something behind, [First Name]"
          "Did something go wrong with your order?"
          "Still thinking about [Product Name]?"

Email 2:  "[Product Name] — still in your cart"
          "Here's what other customers say about [Product]"
          "Only [X] left in stock"

Email 3:  "Last chance — your cart expires today"
          "Here's [X]% off — but only until midnight"
          "We're holding your cart for 24 more hours"
```

Use Klaviyo's `{{ event.ProductName }}` tag to pull the exact item dynamically into subject lines.

---

## Flow 2: Welcome Series

**What it is:** Triggered when someone subscribes via pop-up, landing page, or checkout opt-in — before their first purchase.

**Benchmarks:** Average welcome flow earns $2.65 per recipient. Top 10% of Klaviyo stores hit a 9.89–10.53% placed order rate from welcome alone. Nearly 48% of flow-driven email revenue comes from new buyers.

**Key Rule:** Treat the first 10 days as your highest-intent window. New subscribers are warm. Most brands are too passive here — send more in week 1, not less.

### 4-Email Sequence (Standard)

| # | Timing | Content |
|---|---|---|
| Email 1 | Immediately | Welcome + deliver lead magnet/discount if promised. Brand voice introduction. CTA to best-seller or top collection |
| Email 2 | Day 2 | Brand story — why this exists, who made it, what makes it different. No hard sell |
| Email 3 | Day 5 | Social proof — reviews, UGC, bestsellers, "what customers love" |
| Email 4 | Day 9–10 | Final push — remind them of their offer (if any), address objections, CTA to shop |

**Optional Email 5 (Day 14):** Educational content — how to use the product, style it, or get the most from it. Works especially well for high-consideration or lifestyle products.

**Flow Filter:** Add a filter to exclude anyone who purchases during the sequence. Do not send "here is your discount" to someone who just paid full price.

**Segment Split:** If you have two subscriber sources (pop-up with discount vs. organic checkout opt-in), run separate welcome flows. Do not give a discount to someone who never asked for one.

---

## Flow 3: Post-Purchase

**What it is:** Triggered on first purchase (and optionally on every purchase). This is the most underinvested flow in most solopreneur stores.

**Goal:** Reduce buyer's remorse → request a review → cross-sell a complementary product → build habit/loyalty → get UGC.

**Why it matters:** Acquiring a new customer costs 5–7x more than retaining one. The post-purchase window is when trust is highest. Most brands blow it with a generic "thanks for your order" and nothing else.

### 5-Email Sequence (Full)

| # | Timing | Email Type | Goal |
|---|---|---|---|
| 1 | Immediately | Order confirmation | Trust signal, set expectations |
| 2 | Shipping trigger | Shipping update | Excitement, anticipation |
| 3 | 2–3 days after delivery | Thank you + brand reinforcement | Reduce remorse, tell the story |
| 4 | 7–10 days after delivery | Review request | Social proof engine |
| 5 | 14–21 days after delivery | Cross-sell / replenishment | Second purchase conversion |

**UGC Ask:** Add a sixth email at day 21–30 asking for a photo or testimonial. Offer a small reward (loyalty points, entry into a giveaway). This feeds your social proof for future campaigns.

**Segmentation Tip:** After first purchase, tag the customer. Use this tag to exclude them from the welcome series and to trigger a differentiated second-purchase flow with a higher-order offer.

---

## Flow 4: Browse Abandonment

**What it is:** Triggered when an identified visitor views a product page but does NOT add to cart. Lighter intent than cart abandon — treat it that way.

**Benchmarks:** Browse abandon emails convert at 0.96% vs. 0.10% for broadcast campaigns — nearly 10x lift, even at lower intent.

**Timing:** Send Email 1 within 1–4 hours of the browse event. Sending within 60 minutes consistently outperforms waiting longer.

### 1–2 Email Sequence

| # | Timing | Content |
|---|---|---|
| Email 1 | 1–2 hours | Surface the exact product browsed + 2–3 related alternatives. No discount. Conversational tone |
| Email 2 (optional) | 24 hours | Social proof on the same product. Can include a soft urgency signal (low stock, recent purchases) |

**Keep Smart Sending ON.** This flow has low intent — suppress it if the contact is already in an abandoned cart or welcome flow. Do not stack flows on the same contact in the same 24-hour window.

**Do not send to recent purchasers.** Add a flow filter: "Placed Order — in the last 30 days — zero times" to avoid annoying customers who just bought.

---

## Flow 5: Winback

**What it is:** Triggered when a customer (someone who has purchased before) has not bought again within a defined window. Goal: re-engage them before they go cold forever.

**Timing by Product Type:**

| Product Type | Trigger at | Rationale |
|---|---|---|
| Consumables / supplements | 60–75 days since last order | Should be reordering by now |
| Apparel / lifestyle | 90 days | Seasonal repurchase cycle |
| High-consideration / one-time | 120 days | Longer natural gap; don't over-message |

### 4-Email Winback Sequence

| # | Timing | Content |
|---|---|---|
| Email 1 | At trigger | "We miss you" — light, no pressure, remind them of value |
| Email 2 | +7 days | Highlight what's new — new products, updates, community |
| Email 3 | +14 days | Best offer — strongest incentive (free shipping, bundle discount, loyalty reward) |
| Email 4 | +21 days | Break-up email — "Should we stop sending you emails?" with a one-click re-opt-in |

**Expected performance:** Well-built winback sequences achieve 5–15% reactivation rates.

**Sunset Flow:** Contacts who do not open or click any email in the winback sequence should exit into a sunset flow. Send one final email: "We're removing you from our list — unless you want to stay." Anyone who clicks a re-engagement link stays. Everyone else gets suppressed.

**Why this matters for deliverability:** Emailing unengaged contacts kills your sender reputation. Suppressing non-responders improves open rates for everyone else. This is list hygiene, not list loss.

---

## Subject Line and Preview Text Patterns for Ecommerce

### Subject Line Formulas That Convert

```
Pattern 1 — Personalized curiosity:
  "Still thinking about [Product Name], [First Name]?"

Pattern 2 — Direct benefit:
  "Get 20% off before midnight"

Pattern 3 — Social proof:
  "1,247 people love this — you might too"

Pattern 4 — Scarcity:
  "Only 3 left in stock"

Pattern 5 — Re-engagement:
  "It's been a while, [First Name] — here's what you missed"

Pattern 6 — Question / curiosity:
  "Did something go wrong with your checkout?"

Pattern 7 — Loss aversion:
  "Your cart expires in 24 hours"
```

### Preview Text Rules

- Never repeat the subject line — use preview text to extend it
- Lead with the second-most compelling detail
- Keep under 90 characters; most clients truncate at 40–60
- Example: Subject = "You left something behind" / Preview = "Your [Product] is still waiting — and we saved your cart"

---

## Segmentation — The Three Segments That Drive Disproportionate Revenue

**VIP Segment**
- Definition: Top 20% by lifetime spend, OR customers with 3+ orders, OR AOV above a set threshold
- Treatment: Early access to launches, exclusive offers, loyalty rewards, skip the discount-first flows
- In Klaviyo: Use CLV predictor or manual "placed order count ≥ 3" condition

**First-Time Buyer**
- Definition: Placed exactly 1 order, within the last 90 days
- Treatment: Full post-purchase flow, cross-sell, review request, second-purchase offer
- Goal: Convert to 2x buyer within 60 days — this is where LTV is made or lost

**At-Risk / Lapsing**
- Definition: Previously purchased, no order in 60–90 days, engagement declining
- Treatment: Enter winback flow before full sunset; give your best offer here
- Do not wait until they are fully cold — re-engage at first sign of lapse

---

## SMS Alongside Email — When and How to Add It

**When to add SMS:**
- You have opted-in SMS subscribers (non-negotiable — no cold SMS)
- You have abandoned cart or winback flows already running
- Your AOV is above $40 (lower AOV often doesn't justify the per-send cost)

**How to integrate:**
- Add SMS as a step inside existing Klaviyo flows, not as a separate channel
- Insert SMS between Email 1 and Email 2 in abandoned cart (4-hour mark)
- Use SMS for time-sensitive moments only: cart expiry, flash sale, shipping delay
- Keep SMS conversational, short (under 160 characters), and personal

**US Compliance:**
- Abandoned cart SMS must be sent within 48 hours of trigger
- One SMS per cart abandon event per recipient (legal requirement)
- Always include opt-out instructions ("Reply STOP")

**Tools:** Klaviyo handles email + SMS natively. PostScript is an alternative SMS-only tool that syncs with Klaviyo if you prefer separate management.

---

## Deliverability for Ecommerce Senders

The single most impactful technical change in 2024–2025: set up a **dedicated sending domain**. Gmail and Outlook algorithm updates have hurt stores still using Klaviyo's shared sending domain. This is the first thing to fix if open rates are declining.

**Deliverability checklist:**
- [ ] Dedicated sending domain configured in Klaviyo (DNS records: SPF, DKIM, DMARC)
- [ ] Suppress non-openers older than 90 days before major broadcast campaigns
- [ ] Never buy or import a list without re-permission
- [ ] Flow filter: skip contacts flagged as bounced or unsubscribed
- [ ] Use Smart Sending for browse abandon and lower-intent flows
- [ ] Warm up a new sending domain gradually (start at 200 sends/day, double weekly)

---

## Common Mistakes

1. **Sending only campaigns, ignoring flows** — campaigns are one-time; flows compound forever
2. **One cart abandonment email instead of three** — single emails leave 6x revenue on the table
3. **Discount in Email 1 of abandoned cart** — trains price-sensitive behavior; hold the offer for Email 3
4. **Same welcome experience for buyers and non-buyers** — a subscriber who purchased during welcome still gets "here's your discount"
5. **No dedicated sending domain** — the #1 deliverability killer in 2025
6. **Post-purchase flow ends at order confirmation** — the 2-week post-delivery window is the highest-trust window you will ever have
7. **Emailing unengaged contacts indefinitely** — destroys sender reputation for your entire list
8. **Ignoring mobile rendering** — majority of ecom email opens are on mobile; test before sending
9. **No segmentation whatsoever** — every subscriber gets every flow; VIPs and lapsing buyers need different treatment
10. **Never A/B testing subject lines** — even a 5% lift in open rate compounds significantly across flows

---

## Contrarian Takes

**Discount-first abandoned cart is the wrong default.**
Most brands open their cart recovery with a coupon. This conditions customers to abandon intentionally to fish for codes. Start with curiosity and service, offer the discount only in the final email with a hard expiry. For high-AOV stores especially, buyers rarely abandon because of price — they abandon because of distraction.

**Post-purchase is the most underinvested flow in the business.**
The average D2C brand has a mediocre abandoned cart flow and nothing after "thanks for your order." The post-purchase window — specifically days 3–21 after delivery — is when customer trust peaks and repeat purchases are easiest to trigger. One well-built post-purchase flow regularly generates more incremental revenue than a new acquisition campaign.

**More emails in the welcome window is almost always better.**
Solopreneurs fear email fatigue and hold back in the first 10 days. But new subscribers are at peak intent. A subscriber who doesn't buy in the first 14 days will be 60–70% less likely to buy in the following 60. Send more, not less, while the relationship is fresh — with value, not just promotions.

---

## Quick Wins — Where to Start If You Have One Hour

**Zero flows live → Build abandoned cart first.**
Connect Shopify to Klaviyo, enable the abandoned cart trigger, build 3 emails (1 hour, 24 hours, 72 hours), go live. This single flow will generate positive ROI faster than anything else.

**Flows live, revenue stagnant → Audit the post-purchase flow.**
Most stores have a thin or nonexistent post-purchase flow. Add a review request at day 7 and a cross-sell at day 14. These two emails alone typically lift repeat purchase rate measurably within 30 days.

**Good flows, list engagement dropping → Fix deliverability first.**
Set up a dedicated sending domain. Suppress anyone who hasn't opened in 90 days before the next campaign. Run a re-engagement campaign to the at-risk segment before sunsetting them.

---

## Related Skills

| Skill | When to Use It |
|---|---|
| `email-sequence` | Non-ecommerce email nurture (B2B, content, SaaS) |
| `churn-prevention` | Reducing subscription cancellations and retention for recurring products |
| `referral-program` | Building post-purchase referral mechanics to amplify the customer base |
| `analytics-tracking` | Setting up Klaviyo attribution, revenue reporting, and flow performance dashboards |
| `popup-cro` | Optimizing the pop-ups and lead capture forms that feed the welcome series |

---

*Generated using the ecom-email-nurture skill from Solopreneur Skills*
