---
name: monthly-report
description: Client-ready monthly marketing report as one self-contained HTML file (print to PDF) covering Google Ads, GA4 and Search Console, branded from the profile. Use when the user says "monthly report for <account>", "make the September client report", "report for last month", or wants a printable performance summary.
---

# Monthly report

Pull a calendar month from Google Ads, GA4 and Search Console and write one branded HTML file the user can open and
print to PDF.

## When to use

End-of-month client or management reporting. For "what changed and why" use `performance-insights`.

## Inputs

- `account`: profile alias.
- Month: the previous calendar month unless the user names one. Use `dateFrom` / `dateTo` with the first and last day.
- Optional: a one-paragraph summary or plan for next month from the user.

## Steps

1. `account_profile`: currency, timezone, `brand`, and whether `ga4PropertyId` and `gscSiteUrl` are set.
2. **Ads.** `get_account_summary` and `get_campaign_performance` for the month, `get_account_summary` for the month
   before (for the change column), and the top 15 search terms by cost (`get_search_terms` sorts by clicks):
   `run_gaql_query` with `SELECT search_term_view.search_term, metrics.cost_micros, metrics.clicks, metrics.conversions FROM search_term_view WHERE segments.date BETWEEN '<from>' AND '<to>' ORDER BY metrics.cost_micros DESC LIMIT 15`.
3. **Website (only if `ga4PropertyId` is set).** Month totals with `ga4_custom_report`, `dimensions: []`,
   `metrics: ["sessions", "totalUsers", "engagementRate", "keyEvents"]`. Do not sum the daily rows of
   `ga4_traffic_overview`: users and rates don't add up. Then `ga4_traffic_sources`, `ga4_landing_pages` and
   `ga4_conversions` for the tables.
4. **Organic search (only if `gscSiteUrl` is set).** `gsc_top_queries` and `gsc_top_pages` for the month.
5. **Missing products.** When GA4 or Search Console is not configured, or a call fails with a permission error,
   leave that section out and add one line under "Notes": "<product> not connected for this account".
6. **Brand.** From `brand`:
   - `name` goes on the cover; if absent, use the alias.
   - `colors[0]` / `colors[1]` fill `--brand-1` / `--brand-2`; if absent, keep the template's neutral colours.
   - `logo`: read the file and embed it as a base64 data URI (`data:image/png;base64,...`). If the path is missing or
     unreadable, drop the `<img>` and use the neutral cover. Never link to a local path.
7. **Write the file.** Start from `template.html` in this skill's folder and replace every `{{…}}` placeholder:
   - `BRAND_NAME`, `MONTH_LABEL` (e.g. "September 2026"), `ACCOUNT_LABEL` (alias and customer ID),
     `LOGO_DATA_URI`, `SUMMARY`, `NEXT_MONTH`, `NOTES`, `GENERATED_AT` (date and time, profile timezone).
   - KPI values `SPEND`, `CLICKS`, `CONVERSIONS`, `CPA` with `*_DELTA` text ("+12% vs August") and `*_DIR` classes:
     `good` or `bad` by meaning, not direction (spend up is neutral, so use `good` only when the user's goal says so;
     cost per conversion up is `bad`, conversions up is `good`). Leave `*_DIR` empty when there is no comparison.
   - Website KPIs `SESSIONS`, `USERS`, `ENGAGEMENT`, `KEY_EVENTS`; table rows `CAMPAIGN_ROWS`, `SEARCH_TERM_ROWS`,
     `SOURCE_ROWS`, `LANDING_ROWS`, `QUERY_ROWS`, `PAGE_ROWS` (one `<tr>` per row, numbers in `<td class="num">`).
   - HTML-escape every value that comes from the data (`&`, `<`, `>`, `"`): search terms and page titles are user text.
   - Delete sections whose data is missing (step 5). Use the profile currency for money.
   Save to `reports/<alias>-<YYYY-MM>.html` in the current folder (create `reports/` if needed).
8. Read the numbers once more against the tool output before finishing: totals in the KPI cards must match the
   campaign table.

## Output

The file path, plus three bullets with the month's headline numbers. Tell the user to open the file and use the
browser's Print → Save as PDF; the template has A4 print styles.

## Never

- Never invent numbers, targets or commentary. Commentary comes from the data or from the user.
- Never call write tools; this skill only reads.
- Never leave a broken image or an empty section in the file.
