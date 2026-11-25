---
name: data-collection-plan
description: "Plans data collection strategies with tracking requirements, privacy compliance, storage recommendations, and implementation steps. Use when building your business data infrastructure."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Data Collection Plan

## When to Use This Skill

Use this skill when you need to:
- Plan what data to collect across your business operations
- Design tracking implementations for web, product, or marketing
- Ensure data collection complies with privacy regulations
- Create a data architecture plan for a growing business

**DO NOT** use this skill for data analysis, dashboard building, or database engineering. This is for planning what to collect, why, and how.

---

## Core Principle

COLLECT DATA WITH PURPOSE — EVERY DATA POINT MUST ANSWER A BUSINESS QUESTION OR DRIVE A DECISION. COLLECTING "JUST IN CASE" CREATES LIABILITY WITHOUT VALUE.

---

## Phase 1: Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Business type** | "What does your business do?" | Must be provided |
| **Key decisions** | "What decisions do you wish you had better data for?" | Must be provided |
| **Current data** | "What data do you already collect? Where does it live?" | Minimal — starting fresh |
| **Channels** | "Where do you interact with customers? (website, app, email, social, in-person)" | Website and email |
| **Privacy requirements** | "Where are your customers? (affects GDPR, CCPA, etc.)" | US-based customers |
| **Technical resources** | "Do you have a developer or will you self-implement?" | Self-implement with no-code tools |

**GATE: Confirm brief before proceeding.**

---

## Phase 2: Design

### Data Collection Framework

Organize by business function:

1. **Marketing data** — traffic sources, campaign performance, ad spend, conversions
2. **Product/website data** — user behavior, feature usage, engagement metrics
3. **Sales data** — leads, pipeline stages, close rates, deal values
4. **Customer data** — profiles, preferences, purchase history, support interactions
5. **Financial data** — revenue, costs, margins, cash flow
6. **Operational data** — fulfillment times, error rates, capacity utilization

### Data Priority Matrix

For each data point, assess:
- **Value:** How much does this data improve decisions? (High/Med/Low)
- **Effort:** How hard is it to collect? (High/Med/Low)
- **Privacy risk:** Does this involve personal data? (Yes/No)

Start with high-value, low-effort, low-risk data.

**GATE: Present the prioritized data collection plan and wait for approval.**

---

## Phase 3: Build

### Deliverables

**1. Data Collection Inventory**
| Data Point | Source | Collection Method | Storage | Frequency | Privacy Level |
|-----------|--------|-------------------|---------|-----------|---------------|
| Page views | Website | GA4 | Google | Real-time | Low |
| Email signups | Forms | Zapier → CRM | CRM | Real-time | Medium |
| Revenue | Stripe | API sync | Spreadsheet | Daily | High |

**2. Implementation Guide**
- Step-by-step setup for each data collection tool
- Integration connections (what feeds into what)
- Testing procedures to verify data is flowing

**3. Privacy Compliance Checklist**
- [ ] Privacy policy updated to reflect data collection
- [ ] Cookie consent banner implemented (if required)
- [ ] Data processing records documented
- [ ] Data retention periods defined
- [ ] User data deletion process established
- [ ] Third-party data sharing disclosed

**4. Data Quality Rules**
- Naming conventions for events and fields
- Validation rules for data entry
- Deduplication strategy for customer records
- Regular audit schedule (monthly data quality check)

---

## Phase 4: Polish

### Data Stack Diagram

Create a simple map showing: data sources → collection tools → storage → reporting tools.

### 90-Day Implementation Roadmap

- Month 1: Core tracking (website analytics, basic CRM)
- Month 2: Marketing attribution (UTMs, conversion tracking)
- Month 3: Customer data enrichment (behavior tracking, segmentation)

---

## Example 1: E-commerce Business

**Priority data:** Traffic sources, conversion events, AOV, cart abandonment rate, customer purchase history, email engagement. Tools: GA4, Shopify analytics, Klaviyo.

## Example 2: Service Business

**Priority data:** Lead sources, consultation bookings, close rate, project profitability, client satisfaction scores. Tools: GA4, CRM (HubSpot free), Google Sheets for financials.

---

## Anti-Patterns

- **Collecting everything** — more data means more privacy risk, more storage cost, and more noise. Be selective.
- **No privacy consideration** — collecting personal data without proper consent and documentation is a legal and financial risk.
- **Data silos** — customer data in 5 tools that do not talk to each other makes analysis impossible. Plan integrations from the start.
- **No naming conventions** — `email_signup`, `EmailSignup`, `email-signup`, and `signup_email` in different tools creates chaos. Standardize.
- **Collecting without reviewing** — data nobody looks at is worse than no data because it creates a false sense of being data-driven.

---

## Recovery

- **User overwhelmed by options:** Start with 3 data points that directly answer their most important business question. Expand later.
- **Privacy concerns paralyze action:** Focus on aggregated, non-personal data first (page views, conversion rates). Add personal data collection only with proper consent mechanisms.
- **No technical ability:** Recommend no-code tools (Zapier, Google Forms, native platform analytics). Most essential data collection requires zero code.
- **Data already scattered:** Begin with an inventory of existing data and create a consolidation plan before adding new collection.
