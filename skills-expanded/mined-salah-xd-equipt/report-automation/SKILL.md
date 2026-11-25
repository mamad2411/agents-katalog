---
name: report-automation
description: "Designs automated reporting workflows with data sources, schedules, distribution lists, and template standardization. Use when eliminating manual reporting work."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Report Automation

## When to Use This Skill

Use this skill when you need to:
- Automate recurring business reports that are currently manual
- Design a reporting workflow with scheduled delivery
- Standardize report templates across the business
- Reduce hours spent compiling data into presentations or spreadsheets

**DO NOT** use this skill for one-time analyses, dashboard design, or building automation scripts. This is for planning the automation workflow and template design.

---

## Core Principle

AUTOMATE THE REPORT, NOT THE THINKING — AUTOMATED DATA DELIVERY FREES TIME FOR ANALYSIS AND DECISIONS INSTEAD OF COPY-PASTING NUMBERS.

---

## Phase 1: Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Reports to automate** | "Which recurring reports take the most time?" | Must be provided |
| **Current process** | "How are these reports created now? (manual spreadsheet, copy-paste, tool export)" | Manual spreadsheet |
| **Frequency** | "How often is each report needed? (daily, weekly, monthly)" | Weekly |
| **Audience** | "Who receives each report? (founder, team, clients, investors)" | Founder and team leads |
| **Data sources** | "Where does the report data come from? (GA4, Stripe, CRM, spreadsheets)" | Multiple sources |
| **Tools available** | "What tools do you use or would consider? (Google Sheets, Zapier, Looker, Databox)" | Google Sheets + Zapier |

**GATE: Confirm brief before proceeding.**

---

## Phase 2: Design

### Automation Assessment

For each report, evaluate:
- **Data collection:** Can data be pulled automatically? (API, integration, export)
- **Transformation:** Does data need calculations or reformatting?
- **Presentation:** Can the template be standardized?
- **Distribution:** Can delivery be automated? (email, Slack, dashboard link)

### Automation Levels

| Level | Description | Tools |
|-------|------------|-------|
| **Manual with template** | Standardized template, manual data entry | Google Sheets |
| **Semi-automated** | Data pulls automated, human reviews before sending | Zapier + Sheets |
| **Fully automated** | Data to delivery with no human touch | Looker, Databox, custom |

**GATE: Present the automation plan with recommended level per report.**

---

## Phase 3: Build

### Deliverables

**1. Report Automation Specification**
- Each report mapped: data source → transformation → template → delivery
- Automation level and tools per report
- Schedule and trigger definitions
- Distribution list per report

**2. Standardized Report Templates**
- Template for each report type with placeholder sections
- Consistent formatting: header, date range, key metrics, charts, commentary section
- Brand-consistent styling guidelines

**3. Implementation Guide**
- Step-by-step setup for each automation
- Integration configuration instructions
- Testing procedures (verify data accuracy before automating delivery)
- Error handling: what happens when a data source fails?

**4. Maintenance Checklist**
- Monthly: verify all automations are running and data is accurate
- Quarterly: review whether reports are still needed and useful
- Annually: audit the full reporting stack for redundancies

---

## Phase 4: Polish

### Time Savings Calculation

Document for each report:
- Time spent before automation (hours/week)
- Time spent after automation (hours/week)
- Annual time saved
- Dollar value of recovered time

### Iteration Recommendations

After 1 month of automated reports, gather feedback: Is anything missing? Is anything ignored? Adjust templates and frequency based on actual usage.

---

## Example 1: Weekly Business Metrics Report

**Before:** 2 hours every Monday pulling numbers from GA4, Stripe, and Mailchimp into a Google Doc.
**After:** Google Sheets with Supermetrics auto-pulling data, summary auto-generated, Slack notification sent Monday 8am. Human reviews and adds commentary (20 minutes).

## Example 2: Monthly Client Report (Agency)

**Before:** 4 hours per client assembling analytics, ad performance, and deliverable summaries.
**After:** Looker Studio dashboard with auto-refreshing data, PDF auto-generated and emailed to clients on the 1st. Human adds strategic commentary (30 minutes per client).

---

## Anti-Patterns

- **Automating bad reports** — if nobody reads the report, automating it just sends garbage faster. Validate usefulness first.
- **Over-engineering the first version** — start semi-automated. Prove the template works, then add full automation.
- **No human review layer** — fully automated reports without periodic accuracy checks will eventually send wrong numbers. Build in spot-checks.
- **Too many reports** — automation makes it easy to create reports. Fight the urge. Fewer, better reports beat more reports.
- **Ignoring data freshness** — a "daily" report pulling from a source that updates weekly is misleading. Match report frequency to data availability.

---

## Recovery

- **Data sources do not have APIs:** Use scheduled CSV exports + Google Sheets IMPORTDATA or Zapier file triggers as a bridge.
- **Reports serve different audiences:** Create one data source with multiple views — executive summary for leadership, detailed breakdown for operators.
- **Automation breaks frequently:** Simplify. Complex chains break more often. Reduce integration points or use more robust tools.
- **User does not trust automated numbers:** Run automated and manual reports in parallel for 2 weeks. Compare and resolve discrepancies before retiring the manual process.
