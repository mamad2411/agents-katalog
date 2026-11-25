---
name: metric-definition-guide
description: "Creates metric glossaries defining how each business KPI is calculated, tracked, and interpreted with formulas, data sources, and ownership. Use for team alignment on numbers."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Metric Definition Guide

## When to Use This Skill

Use this skill when you need to:
- Define how each business metric is calculated and tracked
- Create a metric glossary for team alignment
- Resolve disagreements about what a number means
- Onboard new team members on how to interpret key KPIs

**DO NOT** use this skill for building dashboards, analyzing data, or setting targets. This is for defining what metrics mean and how they are calculated.

---

## Core Principle

IF TWO PEOPLE IN YOUR COMPANY CALCULATE THE SAME METRIC DIFFERENTLY, YOU DO NOT HAVE A METRIC — YOU HAVE CONFUSION. DEFINE ONCE, USE EVERYWHERE.

---

## Phase 1: Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Metrics to define** | "Which KPIs does your team track or should track?" | Must be provided |
| **Business model** | "SaaS, e-commerce, services, marketplace?" | Must be provided |
| **Data sources** | "Where does your data live? (Stripe, GA4, CRM, spreadsheets)" | Mixed |
| **Audience** | "Who will use this guide? (whole team, leadership, new hires)" | Whole team |
| **Known confusion** | "Any metrics your team defines or calculates differently?" | General misalignment |

**GATE: Confirm the metric list before proceeding.**

---

## Phase 2: Define

### Metric Definition Template

For each metric, document:

1. **Name** — the official metric name (one name, no synonyms in official reporting)
2. **Definition** — one-sentence plain-language explanation
3. **Formula** — exact calculation with numerator and denominator specified
4. **Data source** — where the numbers come from
5. **Frequency** — how often it is calculated (daily, weekly, monthly)
6. **Owner** — who is responsible for tracking and reporting this metric
7. **Target/benchmark** — what "good" looks like
8. **Interpretation notes** — caveats, known quirks, seasonal patterns

**GATE: Present the first 3-5 definitions for format approval before completing the full guide.**

---

## Phase 3: Build

### Deliverables

**1. Complete Metric Glossary**
- All metrics defined using the standard template
- Organized by category (growth, revenue, engagement, operations)
- Searchable format (table of contents with anchor links)

**2. Metric Relationship Map**
- How metrics relate to each other (e.g., churn affects LTV which affects CAC:LTV ratio)
- Leading vs. lagging indicator classification
- Which metrics to watch together

**3. Calculation Examples**
- Worked example for every formula using realistic sample data
- Edge cases: what happens with zero values, negative numbers, or missing data

**4. Quick Reference Card**
- One-page summary with metric names, formulas, and targets
- Designed for desk reference or Slack pinned message

---

## Phase 4: Polish

### Review and Governance

- Review definitions quarterly for accuracy
- When a new metric is proposed, it must go through the definition template before entering any report
- Version control: date-stamp updates and note changes

### Onboarding Integration

Include the metric guide in new hire onboarding. Schedule a 30-minute walkthrough of the top 10 metrics during the first week.

---

## Example 1: SaaS Metrics

**MRR:** Monthly Recurring Revenue. Sum of all active subscription amounts at month end. Source: Stripe. Monthly. Target: 10% MoM growth.
**Churn Rate:** Customers lost / Customers at start of period. Source: Stripe + CRM. Monthly. Target: Under 3%.
**NRR:** Net Revenue Retention. (Starting MRR + Expansion - Contraction - Churn) / Starting MRR. Source: Stripe. Monthly. Target: Over 110%.

## Example 2: E-commerce Metrics

**AOV:** Average Order Value. Total Revenue / Number of Orders. Source: Shopify. Weekly. Target: $75+.
**Conversion Rate:** Orders / Sessions. Source: GA4 + Shopify. Weekly. Target: 2-3%.
**ROAS:** Return on Ad Spend. Revenue from Ads / Ad Spend. Source: Ad platforms + Shopify. Weekly. Target: 3x+.

---

## Anti-Patterns

- **Multiple definitions for the same metric** — if marketing calculates "customers" differently than finance, reports will never agree. One definition per metric.
- **Undefined denominators** — "Conversion rate" means nothing without specifying what divides what over what time period.
- **Tribal knowledge** — if only one person knows how a metric is calculated, it is not a metric, it is that person's opinion.
- **Too many metrics** — 50 KPIs means zero focus. Define 8-12 primary metrics and categorize the rest as supporting.
- **Never updating definitions** — as the business changes, metric definitions must evolve. Review quarterly.

---

## Recovery

- **Team cannot agree on a definition:** Present 2-3 options with pros and cons. Let the decision-maker pick one and document it as the standard.
- **Data sources give different numbers:** Identify the discrepancy source. Choose one system of record per metric and document why.
- **Too many metrics to define:** Start with the 10 metrics that appear in leadership reporting. Add others in batches.
- **User unsure which metrics matter:** Start with the business model's standard metrics (SaaS: MRR, churn, CAC, LTV; E-commerce: AOV, conversion, ROAS, repeat rate).
