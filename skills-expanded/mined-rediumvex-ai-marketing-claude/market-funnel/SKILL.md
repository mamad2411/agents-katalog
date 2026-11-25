---
name: market-funnel
description: End-to-end funnel analysis from awareness to retention with leak diagnosis and a GA4 event spec. Invoke whenever the user says "funnel", "where are we leaking", "conversion drop", "activation rate", or runs `/market funnel <url>`. Produces FUNNEL-ANALYSIS.md with stage-by-stage scores and an implementable analytics event map.
---

# Market Funnel — Full Journey Diagnosis

Model the full funnel, identify where prospects drop off, and hand back an analytics spec the client's engineer can implement directly.

## The 6 Funnel Stages

| Stage | Goal | Key metric |
|---|---|---|
| **1. Awareness** | Get in front of the right audience | Impressions, reach, branded search |
| **2. Acquisition** | Earn the click | CTR, referral traffic, CAC |
| **3. Activation** | First value moment | Signup rate, first-action rate |
| **4. Revenue** | First purchase or trial conversion | Trial→paid, ARPU |
| **5. Retention** | Continued use | DAU/MAU, churn, repeat rate |
| **6. Referral** | Organic growth | NPS, referral rate, virality coefficient |

Pirate metrics (AARRR) plus Awareness, adapted for 2025 realities.

## Workflow

1. **Map the existing funnel** based on what's visible: the home page, the pricing page, the signup flow, the app/experience.
2. **Score each stage 0–10** using the rubrics below.
3. **Name the leak** — the stage with the steepest drop-off relative to benchmark.
4. **Propose fixes** per stage with expected impact.
5. **Write the GA4 event spec** — every event name, params, when it fires.

## Stage Rubrics

### 1. Awareness (0–10)
- Channels in use (organic, paid, social, referral, partnerships)
- Branded vs non-branded traffic mix
- Share of voice vs competitors (ballpark from search data)
- Content cadence

### 2. Acquisition (0–10)
- Landing page → form view rate
- Page load speed
- Hero-to-CTA distance
- Ad / organic message match

### 3. Activation (0–10)
- Signup friction (fields, steps, time)
- First value moment — is there a "wow" before the user has to commit?
- Empty state quality
- Onboarding sequence present?

### 4. Revenue (0–10)
- Trial length and gating
- Pricing page clarity
- Checkout friction
- Payment options
- Refund/cancel policy transparency

### 5. Retention (0–10)
- Product usage signal (if visible)
- Lifecycle emails
- Re-engagement paths
- Churn recovery

### 6. Referral (0–10)
- Explicit referral program
- Shareable moments built in
- Testimonial capture
- UGC encouragement

## Benchmarks (use these, state they're rough)

| Stage | SaaS | E-com | Agency |
|---|---|---|---|
| Visitor → signup | 2–5% | — | — |
| Visitor → purchase | — | 1.5–3.5% | — |
| Visitor → booked call | — | — | 2–5% |
| Trial → paid | 15–25% | — | — |
| Cart → checkout | — | 40–70% | — |
| Checkout → purchase | — | 65–85% | — |
| Month 1 retention | 70%+ | 15–25% (repeat) | — |

## GA4 Event Spec (deliverable)

Produce a table the client's engineer can implement in one sitting:

| Event name | When it fires | Params | Stage |
|---|---|---|---|
| `page_view` | Every page load | `page_location`, `page_title`, `page_referrer` | Awareness |
| `scroll_50` | Scroll depth 50% | `page_location` | Awareness |
| `cta_click` | Any primary CTA click | `cta_text`, `cta_location`, `destination` | Acquisition |
| `sign_up` | Account creation success | `method`, `plan` | Activation |
| `onboarding_step` | Each onboarding step | `step_number`, `step_name` | Activation |
| `first_value` | Key activation moment (client-specific) | `feature` | Activation |
| `begin_checkout` | Checkout loaded | `value`, `currency`, `items` | Revenue |
| `purchase` | Payment success | `transaction_id`, `value`, `currency`, `items` | Revenue |
| `subscription_started` | First recurring charge | `plan`, `value`, `billing_period` | Revenue |
| `feature_used` | Core feature event (client-specific) | `feature`, `count` | Retention |
| `churn_risk` | Inactivity 14d+ | `last_active` | Retention |
| `referral_sent` | Share action | `channel` | Referral |

Adjust events to the specific product. Always include the stage mapping so the client can build funnel reports in GA4 directly.

## Output: FUNNEL-ANALYSIS.md

```markdown
# Funnel Analysis — [Brand]
**URL:** [url]  |  **Date:** [YYYY-MM-DD]

## Funnel Score: [X]/100

[1-paragraph diagnosis: where the funnel leaks worst and why.]

## Stage Scores
| Stage | Score | Status | Top Issue |
|---|---|---|---|

## Stage-by-Stage Analysis
### 1. Awareness — X/10
[Findings, evidence, fixes]

... repeat for all 6 stages ...

## The Leak
[Name the #1 drop-off point. Estimate its cost. Explain why.]

## Fixes by Stage
### Quick wins (this week)
### High-leverage (this month)
### Strategic (this quarter)

## GA4 Event Spec
[Full table as above]

## Reporting
[3 GA4 exploration reports the client should build: funnel exploration, path exploration, retention.]
```

## Quality Bar

- Be honest about what you can and can't see. The homepage shows you stages 1–3 clearly; 4–6 require the client's analytics data. If you can't see it, flag it.
- The GA4 spec is the most actionable part — it should be copy-paste-ready for a developer.
- Don't invent conversion rates. If you don't know actual CR, say "assume 3% baseline" and compute impact from there.
