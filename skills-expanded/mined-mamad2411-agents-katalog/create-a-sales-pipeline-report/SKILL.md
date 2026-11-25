---
name: create-a-sales-pipeline-report
domain: business
locale: [generic]
interface: web
difficulty: intermediate
est_time: 20min
risk: low
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Create a CRM report that shows open sales pipeline by stage, owner, amount, and expected close date.

## Preconditions

- CRM reporting access.
- A defined pipeline, stage field, amount field, owner field, and close-date field.
- The reporting period and audience for the report.

## Steps

1. **Open the report builder.** [BRANCH: Salesforce | HubSpot | generic] choose Reports and New Report in Salesforce; open Reports or Custom Report Builder in HubSpot; in another CRM, open analytics or reporting. → *Expect:* a report configuration screen is visible.
2. **Select the deal object.** Choose Opportunities, Deals, or the equivalent pipeline object. → *Expect:* the report is based on sales deals.
3. **Filter to open pipeline.** Exclude closed-won, closed-lost, deleted, test, and duplicate records; set close-date range if needed. → *Expect:* only active pipeline rows remain.
4. **Add key columns.** Include deal name, account, owner, stage, amount, probability, close date, and next step. → *Expect:* the table contains fields needed for inspection.
5. **Group and summarize.** Group by stage and owner, then summarize amount and weighted amount if available. → *Expect:* totals show pipeline value by stage and rep.
6. **Add visual output.** Create a funnel, bar chart, or table summary appropriate for the audience. → *Expect:* the report is readable without exporting data.
7. **Save and share.** Name the report, save it in the approved folder, and set access for the intended users. → *Expect:* authorized users can open the report.

## Decision points

- If leadership needs forecast rather than raw pipeline → include forecast category and weighted amount.
- If reps need hygiene review → include next step, last activity date, and stale deal flags.
- If data contains restricted accounts → limit report sharing to approved roles.

## Failure modes & recovery

- **F1 Closed deals included:** detect closed-won or closed-lost records in rows → tighten status or stage filters.
- **F2 Inflated totals:** detect duplicates, test deals, or multi-currency issues → filter or group according to reporting policy.
- **F3 Access denied:** detect users cannot open the report → move it to an accessible folder or adjust sharing permissions.

## Verification

The saved report shows only open pipeline, grouped by stage or owner, with correct amount totals and access limited to the intended audience.

## Variations

- Weekly sales meeting: add stale next-step and close-date slippage fields.
- Executive report: use summarized visuals and forecast categories.
- Territory report: filter by region, segment, or account owner.

## Safety & privacy

Pipeline reports can expose customer names, revenue, and rep performance. Share only with authorized audiences and avoid exporting sensitive sales data unnecessarily.
