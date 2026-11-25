---
name: subscription-management
description: Track, analyze, and optimize all SaaS subscriptions — renewals, usage analysis, cost optimization, vendor consolidation, and cancellation workflows.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [cfo, finance, subscriptions, saas, cost-optimization, renewals, vendor-management]
related_skills:
  - transaction-processing
  - accounts-payable-management
  - cost-optimization
  - budget-creation-management
  - ledger-management
inputs_required:
  - subscription-inventory
  - usage-data
  - contract-terms
deliverables:
  - subscription-inventory-table
  - optimization-hit-list
  - renewal-calendar
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Subscription Management

## Purpose

Every SaaS subscription the company pays for must be tracked — who uses it, when it renews, what it costs, and whether it's still worth it. This skill eliminates zombie subscriptions, right-sizes plans, times renewals strategically, and keeps the SaaS stack lean. Without it, companies waste 30% or more of their SaaS spend on unused or underused tools.

## When to Use

- "Audit our SaaS subscriptions"
- "What subscriptions do we have / when do they renew?"
- "Optimize our tool stack / find unused subscriptions"
- "Review this renewal / negotiate this contract"
- "Consolidate overlapping tools"

## Inputs Required

1. **Subscription inventory** — source from: accounting system (QuickBooks/Xero), corporate card exports, bank statements, email invoices, SSO/procurement tools (Vendr, Tropic, Zylo).
2. **Usage data** — login frequency per user, seat utilization, feature adoption. Either from the vendor's admin panel or from SSO logs.
3. **Contract terms** — renewal date, term length, auto-renewal clause, cancellation window, price lock.

## Quick Reference

| Metric / Action | Definition | Why It Matters |
|----------------|-----------|---------------|
| Seat Utilization | Active users / Paid seats. < 70% → flag for downsizing | Paying for seats nobody uses is the #1 SaaS waste |
| Cost per Seat | Annual subscription cost / Total seats | Compare against industry benchmarks for the tool category |
| Zombie Subscription | No active users in 60+ days, no critical dependency | Immediate cancellation candidate |
| Renewal Calendar | 12-month forward view of all renewals with action deadlines | Prevents auto-renewal surprises and missed negotiation windows |
| 80/20 Rule | 20% of subscriptions drive 80% of spend | Focus optimization energy on the expensive tools |
| Annual vs Monthly | Annual billing saves 15-20% on average | Switch to annual for tools you'll definitely use for a year |

## Procedure

### 1. Build the Subscription Inventory

Compile into a unified register:

| Vendor | Product | Plan/Tier | Monthly Cost | Annual Cost | Users/Seats | Billing Owner | Renewal Date | Auto-Renew? | Cancel Window |
|---|---|---|---|---|---|---|---|---|---|
| HubSpot | CRM | Pro | $890 | $10,680 | 8/10 | Sales | 2026-07-15 | Yes | 30 days |
| Figma | Design | Enterprise | $540 | $6,480 | 4/15 | Design | 2026-09-01 | Yes | 30 days |

Add: annualized total, cost per seat, cost as % of total SaaS spend.

### 2. Usage Analysis

For each subscription, assess:

- **Seat utilization**: active users / paid seats. < 70% → flag for downsizing.
- **Login frequency**: users who haven't logged in > 30 days.
- **Feature overlap**: if two tools serve the same function, flag for consolidation.
- **Cost trend**: is the cost growing faster than the company?
- **Contract terms**: is the price locked or variable? Any upcoming price increases?

### 3. Optimization Recommendations

Categorize every subscription:

| Action | Criteria | Example |
|---|---|---|
| **Cancel immediately** | No active users in 60+ days, no critical dependency | That SEO tool nobody uses |
| **Downsize** | < 50% seat utilization, can reduce tier | Enterprise plan for a team of 5 |
| **Renegotiate** | Renewal within 90 days, > $5k/yr, no price lock | Request volume discount, annual commit |
| **Consolidate** | Functional overlap with another tool | Notion vs Confluence vs Google Docs |
| **Keep as-is** | High utilization, mission-critical, fair price | AWS, GitHub |
| **Replace with free/OSS** | Light usage of expensive tool, OSS alternative exists | Figma → Penpot for basic work |

### 4. Renewal Calendar

Produce a 12-month forward view:

```
May 2026:    HubSpot ($10,680) — 30-day cancel window: ACT NOW
Jun 2026:    —
Jul 2026:    Datadog ($18,000) — negotiate by Jun 01
Aug 2026:    —
Sep 2026:    Figma ($6,480)
Oct 2026:    Salesforce ($24,000) — start negotiation Aug 01
...
```

Flag any renewal > $10k/yr that is within 90 days but hasn't been reviewed.

### 5. Quarterly Audit

Run this skill at least quarterly, at budget review time. Compare the inventory against:
- Budget line items (`budget-creation-management`)
- Actual bank charges (`transaction-processing`, `bank-reconciliation`)
- New tools that appear without a corresponding procurement record (shadow IT)

## Output Format

- **Subscription inventory** (Markdown table, sorted by annual cost descending)
- **Optimization hit list** — ranked by savings impact
- **Renewal calendar** — next 12 months with action deadlines
- **Executive summary** — total monthly/annual SaaS spend, change from last quarter, projected annual savings from optimization

## Done Criteria

The skill is complete when:
1. All SaaS subscriptions are compiled into a unified inventory with costs, seats, and renewal dates
2. Usage analysis is performed for each subscription (seat utilization, login frequency, feature overlap)
3. Optimization recommendations are made for every subscription (cancel, downsize, renegotiate, consolidate, keep)
4. Renewal calendar is produced covering the next 12 months with action deadlines
5. Total SaaS spend is calculated with quarter-over-quarter trend
6. Shadow IT (tools without procurement records) is flagged

## Pitfalls

- **Missing founder-purchased tools**: Tools bought on the founder's personal card won't show up in corporate card exports or accounting systems. Hunt for these manually
- **Ignoring usage-based pricing**: AWS, Datadog, and Twilio are harder to cap than fixed-price subs. Treat usage-based pricing separately and set up usage alerts
- **Assuming annual contracts with monthly payment are cancellable**: They're still a 12-month commitment even if billed monthly. Don't assume cancellation is easy
- **Overlooking per-seat pricing that scales with customers**: Tools like Intercom and HubSpot scale cost with customer count. Model the cost curve, not just current spend
- **Skipping the quarterly audit cadence**: A one-time audit catches the obvious waste, but without a regular cadence, new subscriptions accumulate and sprawl returns

## Verification

Is every subscription in the inventory linked to a specific billing owner and renewal date? Is seat utilization calculated and compared against the 70% threshold? Are optimization recommendations prioritized by savings impact? Does the renewal calendar flag all renewals within 90 days that need action? Are usage-based pricing subscriptions separated from fixed-price subs?

## Example

**Example 1: Full SaaS Audit**
> User: "Audit all our SaaS subscriptions — I think we're wasting money"

→ You compile an inventory from the corporate card export, bank statements, and email invoices — 37 subscriptions totaling $184,000/yr. Usage analysis reveals: 12 subscriptions with < 50% seat utilization, 3 tools with zero active users in 60+ days (zombies), 2 pairs of overlapping tools (Notion/Confluence, Zoom/Whereby). You recommend: cancel 3 zombies ($8,400/yr savings), downsize 5 plans ($14,200/yr), consolidate Notion/Confluence into one ($6,000/yr), renegotiate HubSpot ($10,680 renewal in 60 days — 30-day cancel window is ACT NOW). Total projected savings: $31,600/yr (17% of current spend).

**Example 2: Renewal Negotiation Prep**
> User: "Our Datadog renewal is coming up — help me prepare"

→ You pull the Datadog inventory: $18,000/yr, 12 seats, 8 active users (67% utilization), usage-based infrastructure monitoring costs adding ~$2,000/mo. Last year's price was $16,000 — a 12.5% increase. You prepare: competitive quotes from Grafana Cloud ($12,000/yr) and New Relic ($14,000/yr), a usage optimization recommendation (reduce data retention from 15 to 7 days to cut variable costs by ~30%), and a negotiation target of $15,000/yr with an annual commit.
