---
name: pinterest-analytics
description: Analyze Pinterest data from any source — CSV exports, PDF reports, dashboard screenshots, and trend reports like Pinterest Predicts or Pinterest Trends — to find top-performing pins, rank trending search demand, track performance over time, and produce polished client-ready reports. Use this skill whenever the user mentions Pinterest data, pins, boards, Pinterest Analytics, Pinterest Predicts, trend reports, impressions/saves/outbound clicks, or uploads files that look like Pinterest exports, dashboard screenshots, or Pinterest trend forecasts, even if they just say "analyze this" or "make a report from this" without naming Pinterest explicitly. Also use it for month-over-month Pinterest comparisons, content strategy or content calendar recommendations based on pin performance or search trends, and combining multiple Pinterest files into one report.
---

# Pinterest Analytics

Turn raw Pinterest data (CSVs, PDFs, dashboard screenshots) into insight and client-ready reports.

## Why this skill exists

Pinterest data arrives messy and in mixed formats. Clients forward PDF summaries, marketers screenshot the dashboard, and Pinterest's own CSV exports vary in structure depending on which page they were exported from. The goal is always the same: figure out what content is working, how performance is moving over time, and communicate it clearly to someone who won't look at a spreadsheet. Keep that end goal in mind at every step — the deliverable is insight, not a data dump.

## Workflow overview

1. **Ingest** every file the user provides (see "Reading each input type")
2. **Normalize** into one tidy dataset (see "Normalizing the data")
3. **Analyze** — top performers, trends, and anything the user specifically asked for
4. **Report** — pick the right deliverable format and build it

## Step 1: Reading each input type

Inventory all uploaded files first. Users often upload a mix (e.g., a CSV plus screenshots of charts the CSV doesn't cover). Every file is a data source; don't ignore any.

**CSV exports.** Read with pandas. Pinterest exports vary; common shapes include:
- *Pin-level export*: one row per pin with columns like `Pin ID`, `Pin title`, `Impressions`, `Engagements`, `Pin clicks`, `Outbound clicks`, `Saves`, sometimes `Created date` and `Board name`
- *Time-series export*: one row per day with aggregate metrics (`Date`, `Impressions`, `Engagements`, ...)
- *Ads exports*: campaign/ad group rows with `Spend`, `CPC`, `CTR`, conversion columns

Column names shift over time and by locale. Match columns by meaning, not exact name (e.g., "Link clicks" ≈ "Outbound clicks" in older exports). Check for thousands separators, percent signs, and currency symbols stored as text — strip and convert to numeric before doing math.

**PDF reports.** Consult the pdf-reading skill if available. Extract tables and stated metrics. PDFs from Pinterest or agency tools usually contain summary numbers (period totals, top pins) — capture the reporting period from headers or page text, since the numbers are meaningless without it.

**Images / screenshots.** Read the image directly (it will be visible in context). Transcribe every legible number, label, and date range into a small table before analyzing. Note the metric and period each screenshot covers. If a chart has no readable axis values, describe the shape of the trend qualitatively and say so — never invent numbers a screenshot doesn't show.

If any file is unreadable or a critical piece (like the date range) is missing, tell the user what's missing and what you assumed, rather than silently guessing.

## Step 2: Normalizing the data

Build one tidy dataset (or two: pin-level and time-series) before analyzing. Record for each data point: source file, metric, value, date or period, and pin/board identifiers when present.

Watch for these Pinterest-specific traps:

- **Overlapping periods.** Two files covering "last 30 days" exported a week apart overlap. Deduplicate by date, and flag the overlap to the user.
- **Impressions ≠ success.** Pinterest inflates impressions relative to meaningful actions. Never rank "top pins" by impressions alone.
- **Fresh-pin bias.** Pins accumulate metrics over their lifetime, so recently created pins look weak in lifetime exports. When `Created date` exists, normalize (e.g., engagements per day live) or segment by pin age before comparing.
- **Mixed granularity.** Don't sum a time-series file with a lifetime pin export — they measure different windows. Keep them as separate views.

## Step 3: Analysis

Pinterest data comes in two fundamentally different kinds, and they must not be blended: **performance data** (how the user's own pins/account did: impressions, saves, clicks) and **demand data** (what Pinterest users are searching for: Pinterest Predicts reports, Pinterest Trends exports, search growth percentages). Identify which kind each file is before analyzing. Performance data answers "what's working for us"; demand data answers "what the audience wants next." The most valuable reports combine both, but each gets its own analysis below.

### Key metrics and how to derive them

Compute these when the underlying columns exist (skip silently when they don't):

- **Engagement rate** = Engagements / Impressions
- **Save rate** = Saves / Impressions — the strongest signal of content resonance; saves drive long-term distribution on Pinterest
- **Outbound click rate** = Outbound clicks / Impressions — the traffic signal; what most clients ultimately pay for
- **Clicks per save** — indicates whether content inspires action or just collection

### Finding top performers

Rank pins on the metric that matches the user's goal: outbound clicks for traffic goals, saves for reach/brand goals, engagement rate for content-quality questions. Present a top-10 style view with each pin's key metrics side by side, and explicitly note *why* each pin likely performed (format, topic, seasonality) when the data supports it. Also surface the underperformers quietly — clients ask.

### Trends over time

- Aggregate daily data to weekly for anything over ~6 weeks; daily Pinterest data is noisy.
- Pinterest is strongly seasonal and *forward-looking*: users search 2–3 months ahead of holidays and seasons. A spike in October food content is often Thanksgiving/Christmas planning, not October demand. Read trends with this lead time in mind and say so in recommendations (e.g., "publish holiday content by early October").
- Compare like periods (this month vs. same month last year when data allows) before month-over-month, to avoid mistaking seasonality for growth or decline.
- Call out inflection points and tie them to known causes when the user has mentioned any (new posting cadence, campaign launches).

### Trend and search-demand data (Pinterest Predicts, Pinterest Trends)

Trend reports contain search growth data, not account metrics — analyze them accordingly:

- **Normalize into a tidy table**: trend name, category, driving generations, search term, YoY growth %. Every trend page in Pinterest Predicts lists 5–6 search terms with growth figures; capture all of them, not just the headline.
- **Always record the analysis period and methodology** from the fine print (e.g., "normalized global English searches, Sep 2024–Aug 2025 vs. prior year"). Growth percentages are meaningless without their comparison window, and clients will ask.
- **Rank trends by average search growth across their terms**, and separately surface breakout terms (single terms with extreme growth, like +400%+) — these are low-competition content openings. Compute rankings programmatically; never sort by eye.
- **Translate demand into a content calendar.** Because users plan 2–3 months ahead, recommendations should state *when* to publish for each trend, not just what. A 2026 trend report read mid-2026 means "publish now," not "wait for the peak."
- **Never present forecast data as performance data.** Note in the deliverable that these are demand signals, and recommend pairing with the account's own pin-level analytics to pick which trends fit the existing audience.

### Recommendations

Every analysis should end with 3–5 specific, actionable recommendations grounded in the data ("your video pins earn 2.4× the save rate of static pins — shift toward video"), not generic Pinterest advice. If the data is too thin to support a recommendation, say what additional export would unlock it (and name the exact Pinterest Analytics page to export from, if known).

## Step 4: The deliverable

Choose format by audience, and confirm with the user only if genuinely ambiguous:

- **Client or team report** → Excel workbook (consult the xlsx skill): a Summary sheet with headline numbers and takeaways, a Top Pins sheet, a Trends sheet with charts, and a clean Data sheet with the normalized dataset. Charts belong on the sheets they explain.
- **Formal written deliverable** → Word document (consult the docx skill) with an executive summary first, then findings with embedded charts, then recommendations.
- **Quick look for the user themselves** → answer directly in conversation with a compact table and the key findings; offer to build the full report after.

Report structure to follow in any format:

```
1. Executive summary — 3-5 sentences: period covered, headline movement, single biggest insight
2. Performance overview — totals and rates for the period, vs. prior period when available
3. Top content — ranked pins with the metrics that matter for the stated goal
4. Trends — time-series view with seasonality context
5. Recommendations — specific and data-grounded
6. Appendix / data notes — sources used, periods covered, any gaps or assumptions
```

The data notes section is not optional when inputs were mixed (screenshots + CSV): state which numbers came from where, so the client can trust the report.

## Reference

For Pinterest metric definitions and how the platform's distribution works (useful when explaining results to clients), read `references/pinterest-metrics.md`.
