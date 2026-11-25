---
name: analytics-setup-guide
description: "Plans web analytics implementation with event tracking, goals, conversion setup, and dashboard configuration. Use when setting up Google Analytics or similar tools from scratch."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Analytics Setup Guide

## When to Use This Skill

Use this skill when you need to:
- Set up Google Analytics (GA4) or another web analytics platform from scratch
- Plan event tracking for a website or web application
- Define goals and conversion tracking for a business
- Design analytics dashboards that drive decisions

**DO NOT** use this skill for social media analytics, email marketing analytics, or financial reporting dashboards. This is for website and web app analytics implementation.

---

## Core Principle

TRACK WHAT YOU WILL ACT ON — EVERY EVENT AND GOAL MUST CONNECT TO A BUSINESS DECISION OR IT IS NOISE.

---

## Phase 1: Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Website type** | "What kind of site? (e-commerce, SaaS, blog, lead gen, portfolio)" | Lead generation site |
| **Platform** | "What analytics tool? (GA4, Plausible, Mixpanel, Amplitude)" | Google Analytics 4 |
| **Business goals** | "What are your top 3 business outcomes this site should drive?" | Leads, sales, engagement |
| **Current setup** | "Do you have any analytics installed already?" | None — starting fresh |
| **Tech stack** | "What is your site built on? (WordPress, Shopify, custom, etc.)" | WordPress |
| **Key pages** | "Which pages matter most? (homepage, pricing, signup, checkout)" | Homepage, pricing, contact |

**GATE: Confirm brief before proceeding.**

---

## Phase 2: Plan

### Tracking Plan Structure

1. **Page-level tracking** — what pageviews matter and why
2. **Event tracking** — user actions to capture (clicks, form submissions, scrolls, video plays)
3. **Conversion goals** — primary and secondary conversion definitions
4. **Custom dimensions** — user properties worth segmenting by
5. **UTM strategy** — campaign tagging conventions for traffic sources
6. **Dashboard layout** — what reports to build and check weekly

### Event Naming Convention

Use a consistent schema: `category_action_label`
- `cta_click_hero` — hero section CTA button clicked
- `form_submit_contact` — contact form submitted
- `page_scroll_50` — user scrolled 50% of page

**GATE: Present the tracking plan and wait for approval.**

---

## Phase 3: Build

### Deliverables

**1. Complete Tracking Plan Spreadsheet**
- Every event with name, trigger, parameters, and business purpose
- Conversion goals with value assignments
- UTM naming convention with examples

**2. Implementation Guide**
- Step-by-step setup instructions for the chosen platform
- Tag Manager configuration (if applicable)
- Code snippets for custom events
- Testing checklist to verify each event fires correctly

**3. Dashboard Blueprint**
- Recommended widgets and metrics per dashboard section
- Overview dashboard: traffic, conversions, top pages, sources
- Acquisition dashboard: channel breakdown, campaign performance
- Behavior dashboard: engagement, scroll depth, click maps

**4. UTM Tracking Template**
- Spreadsheet template for generating consistent UTM parameters
- Naming conventions for source, medium, campaign, content, term

---

## Phase 4: Polish

### Weekly Review Checklist

- Check conversion rates vs. previous week
- Review top traffic sources and any anomalies
- Verify event tracking is still firing (no broken tags)
- Note any data gaps or unexpected patterns

### 30-Day Post-Launch Audit

After 30 days of data collection, review: Are all events firing? Are conversion goals accurate? Is the data answering business questions?

---

## Example 1: Lead Gen Website (WordPress, GA4)

**Key events:** CTA clicks (3 locations), contact form submission, pricing page visit, blog post scroll 75%
**Conversions:** Primary = form submission. Secondary = pricing page visit.
**Dashboard:** Weekly traffic, conversion rate, top landing pages, source breakdown.

## Example 2: E-commerce Store (Shopify, GA4)

**Key events:** Add to cart, begin checkout, purchase, product view, collection filter use
**Conversions:** Primary = purchase. Secondary = add to cart.
**Dashboard:** Revenue, AOV, conversion rate by source, top products, cart abandonment rate.

---

## Anti-Patterns

- **Tracking everything** — 200 events with no plan produces data paralysis. Start with 10-15 events that map to business decisions.
- **No conversion goals** — pageviews without goals is vanity metrics. Define what "success" means for the site.
- **Inconsistent UTM tags** — `facebook`, `Facebook`, `fb`, and `FB` are four different sources. Standardize and document.
- **Never checking the data** — analytics you do not review weekly are wasted setup time. Build a review habit.
- **Ignoring data sampling** — GA4 samples data at high volumes. Know when your reports are sampled and account for it.

---

## Recovery

- **User overwhelmed by GA4:** Start with 3 events and 1 conversion goal. Add complexity after the basics work.
- **Existing messy setup:** Audit current tags, remove duplicates, document what exists, then add missing pieces.
- **No technical skills:** Provide Tag Manager instructions with screenshots and click-by-click steps.
- **Privacy concerns:** Recommend cookie consent setup and configure GA4 data retention and anonymization settings.
