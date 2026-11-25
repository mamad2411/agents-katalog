---
name: leaddocket-reports
description: >
  Understand and use the built-in Reports and Analytics in LeadDocket.
  Covers the available report types, how to access and filter them, and how to
  use the API to supplement reporting with raw data exports. Use when the user
  asks about lead pipeline performance, referral ROI, user activity, settlement
  totals, or conversion rates.
---

# LeadDocket — Reports & Analytics

LeadDocket includes built-in reporting tools accessible from the UI. There is no dedicated reporting API — reports are UI-only features that can be supplemented with API data pulls.

> Support section: [Reports](https://support.leaddocket.com/hc/en-us/sections/360009498811-Reports)

---

## Accessing Reports (in the LeadDocket UI)

Navigate to the **Reports** section in the top navigation bar.

---

## Available Report Types

### Lead Pipeline Reports

| Report | What it shows |
|--------|--------------|
| **Leads by Status** | Count and list of leads in each pipeline status |
| **Lead Conversion Rate** | % of opportunities converted to leads |
| **Status History** | Timeline of status changes for a lead or group |
| **Leads by Source** | Lead volume attributed to each marketing source |
| **Lead Volume Over Time** | Lead creation trends by day/week/month |

### Financial Reports

| Report | What it shows |
|--------|--------------|
| **Settlements** | Gross settlements, attorney fees, net client recovery |
| **Expenses** | Case expenses by date range and type |
| **Revenue by Referral Source** | Settlement value attributed to each referral |

### Referral Reports

| Report | What it shows |
|--------|--------------|
| **Referral Source Activity** | Volume of leads per referral source |
| **Referral ROI** | Settlement totals grouped by referral source |
| **Top Referrers** | Ranked list by lead volume or settlement value |

### User Activity Reports

| Report | What it shows |
|--------|--------------|
| **User Performance** | Leads handled, conversion rates by user |
| **Task Completion** | Tasks created vs. completed by user |

---

## Exporting Report Data via API

While UI reports aren't available via API, you can reconstruct most reports using API data:

```
Lead volume by source:
GET /api/leads/lastupdatedsince?date=2026-01-01 → aggregate by LeadSourceId

Settlement totals:
GET /api/settlements/getbyleadid/{id} → sum per lead

Referral activity:
GET /api/referrals/list → cross-reference with leads

Expense totals by date:
GET /api/expenses/getlist?startDate=2026-01-01&endDate=2026-06-30
```

---

## Best Practices

- **Date range filters**: Most reports support custom date ranges. Use fiscal quarters or month-over-month for consistent comparisons.
- **Export to CSV**: Reports in the UI support CSV export for use in Excel or Google Sheets.
- **Supplement with API**: For custom dashboards or BI tools (Tableau, Looker), pull raw data via the API's `lastupdatedsince` endpoints and aggregate in your BI layer.
- **Referral ROI**: The referral + settlement reports together are the core business development metric for law firms. Review monthly.
