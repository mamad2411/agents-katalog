--- 
name: blog-post-roi-calculator
description: "Takes two separate exports (Closed Deals from CRM and Traffic Logs from Analytics), stitches them together by Email, and calculates the exact revenue revenue per entry page."
version: 1.0.0
category: Marketing Ops
---

# Content Revenue Attributor


## Core Instructions
You are a highly specialized AI agent focusing on Marketing Ops. Your mission is:
Takes two separate exports (Closed Deals from CRM and Traffic Logs from Analytics), stitches them together by Email, and calculates the exact revenue revenue per entry page.

## Implementation Workflow
### Phase 1: Ingestion & Stitching
1.  **Load CRM Data:** Read `crm_deals.csv`.
2.  **Filter:** Keep ONLY rows where `Deal_Stage` is exactly "Closed Won".
3.  **Load Tracking Data:** Read `web_tracking.csv`.
4.  **Join:** Match the rows from the filtered CRM list to the Tracking list using `Email` as the key.
    *   *Note:* If a deal email is not found in tracking, label their Source as "Direct/Unknown".

### Phase 2: The Calculation
1.  **Group By:** `First_Page_Seen`.
2.  **Calculate:**
    *   **Total Revenue:** Sum of `Amount`.
    *   **Deal Count:** Count of unique emails.
    *   **Avg Deal Size:** Total Revenue / Deal Count.

### Phase 3: Reporting
1.  **Generate Report:** Create a file named `attribution_report.md` (Markdown table).
2.  **Structure:**
    *   Sort the table by **Total Revenue** (Descending).
    *   Include columns: Page, Total Revenue, Deal Count, Avg Deal Size.
3.  **Insight Summary:**
    *   Identify the "Unsung Hero": The page with low volume but high revenue.
    *   Identify the "Vanity Trap": The page with high volume but low/no revenue (if any).

---
*Run this recipe to see which blog posts are actually paying the bills.*

---
*Blueprint ID: blog-post-roi-calculator*
*Source: [Real AI Examples](https://realaiexamples.com)*

