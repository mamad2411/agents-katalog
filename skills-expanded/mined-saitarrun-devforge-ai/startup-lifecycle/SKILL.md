---
name: startup-lifecycle
description: End-to-end founder playbook, product-market fit (PMF) telemetry, SaaS monetization, churn analysis, growth loops, and investor-ready unit economics (CAC, LTV, MRR).
version: 1.0.0
---

# Software Startup Full Lifecycle & Growth Skill

This skill guides founders and engineering teams through building, launching, operating, monetizing, and scaling a high-growth SaaS / AI startup directly from the repository.

---

## 1. The Startup Growth Engine Matrix

```
[Phase 1: 0 to 1 — Problem-Market Fit & MVP]
  ↳ Grill-Me Ideation → Scope Minimization (3 Tracer Slices) → Landing Page Waitlist + Stripe Pre-orders
          ↓
[Phase 2: 1 to 10 — Product-Market Fit (PMF) & Telemetry]
  ↳ PostHog / Mixpanel Event Tracking → North Star Metric → Sean Ellis PMF Survey (>40% "Very Disappointed")
          ↓
[Phase 3: 10 to 100 — SaaS Monetization & Growth Loops]
  ↳ Stripe Billing / Polar / LemonSqueezy (Subscriptions, Metered Tokens, Team Seats) → Referral & SEO Loops
          ↓
[Phase 4: Scale — Unit Economics & Operational Governance]
  ↳ Churn & Retention Cohorts → LTV / CAC Ratio (>3:1) → SOC2 / Compliance → Self-Serve Enterprise Upgrades
```

---

## 2. Startup Engineering Standards

### A. SaaS Monetization & Pricing Architecture
- **Pricing Models**:
  - *Tiered Subscriptions*: Free / Starter / Pro / Enterprise.
  - *Usage-Based (Metered)*: Bill per API call, token consumed, or storage GB.
  - *Per-Seat*: Scaled pricing per team member.
- **Billing Provider Integration**: Stripe Elements, Customer Portal, Webhook Handlers (`invoice.payment_succeeded`, `customer.subscription.deleted`), and dunning email triggers.

### B. Founder Telemetry & Analytics Instrumentation
- **North Star Metric**: Track the one event indicating primary user value (e.g. `query_executed`, `report_exported`, `claim_processed`).
- **Funnel Drop-Off Tracking**:
  - `User Visited Landing Page` → `Signed Up` → `Completed Onboarding` → `Invited Teammate` → `Paid`.
- **Feature Flags & A/B Testing**: PostHog / LaunchDarkly flags to test pricing experiments and checkout flows safely.

### C. Automated Customer Feedback & Churn Mitigation
- **NPS & In-App Surveys**: Automated survey trigger after 7 days of active usage.
- **Cancellation Flow**: Capture exit reason (Too expensive, missing feature, buggy, switched to competitor) and trigger discount/rescue offer.

---

## 3. Investor & Unit Economics Dashboard

Every startup repository should maintain a live metrics tracker in `docs/startup-metrics.md`:

| Metric | Target / Benchmark | Formula / Meaning |
|---|---|---|
| **MRR / ARR** | Growing 15-20% MoM | Monthly / Annual Recurring Revenue |
| **CAC** | Payback < 12 months | Customer Acquisition Cost |
| **LTV** | LTV : CAC > 3.0 | Lifetime Value per Customer |
| **Net Revenue Retention (NRR)** | > 110% for B2B | Expansion revenue outpacing churn |
| **Burn Multiple** | < 1.5 | Net Burn / Net New ARR |
