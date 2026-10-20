---
name: impact-framework
description: "Generate a quarterly impact summary for overlay specialists. Maps engagements to Wiseman's 4-domain model (Account Outcomes, Engagement Quality, Strategic Influence, Knowledge Multiplication), cross-references with STRIDE profile goals, and pulls live data from the Strategist Impact Dashboard. Triggers on 'impact summary', 'quarterly summary', 'what did I work on', 'document impact', 'impact report', 'quarterly review', 'Q1 summary', 'Q2 summary'."
user-invocable: true
default-model: opus
---

# Impact Framework

Generate a crisp, data-driven quarterly impact summary for overlay specialists. Uses Wiseman's *Impact Players* 4-domain model mapped to the Strategist Impact Dashboard.

**Strongly recommended:** Create a Strategist Profile first via `/strategist-profile`. The impact summary maps directly to your goals, KPIs, and named accounts. Without a profile, the skill will still generate a summary from engagement data but cannot score goal attainment.

---

## Databricks Fiscal Year Calendar

| Quarter | Months | Example |
|---------|--------|---------|
| Q1 | Feb - Apr | FY27Q1 = Feb 2026 - Apr 2026 |
| Q2 | May - Jul | FY27Q2 = May 2026 - Jul 2026 |
| Q3 | Aug - Oct | FY27Q3 = Aug 2026 - Oct 2026 |
| Q4 | Nov - Jan | FY27Q4 = Nov 2026 - Jan 2027 |

FY starts in February. To determine the current FY quarter: if the current month is January, it's Q4 of the *previous* FY. Otherwise, FY = calendar year + 1 for Feb-Jan, and quarter = ceil((month - 1) / 3) where month 2=Q1 start.

---

## Step 1 — Context Gathering

### Read the Strategist Profile
Check if `~/.vibe/stride-profile.yaml` exists. If yes, read it and extract:
- **Named goals** with targets (e.g., "2 C-level doors, 3 high-value use cases")
- **Focus areas/themes** (e.g., "Agentic AI", "Process Intelligence")
- **Named accounts** (e.g., Stroeer, BSH, Viessmann)
- **KPIs** with targets
- **Time allocation model**

If no profile exists, inform the user:
> "I can generate an impact summary from your engagement data, but it'll be much richer with a Strategist Profile. Run `/strategist-profile` to set one up — or continue and I'll work with what I find."

### Determine the Quarter
Ask the user which quarter to summarize, or default to the current quarter. Convert to FY notation (e.g., "FY27Q1").

---

## Step 2 — Pull Engagement Data

Query the Strategist Impact Dashboard source data using the `fe-databricks-tools:databricks-query` skill. Use the `logfood` profile.

### Core Query: Engagement Portfolio for the Quarter
```sql
SELECT
  e.customer,
  e.account_id,
  e.engagement_type,
  e.engagement_format,
  e.engagement_status,
  e.engagement_title,
  e.ae,
  e.fy,
  e.quarter,
  e.territory_area,
  e.next_steps,
  COALESCE(e.total_dbu_dollars, 0) AS total_dbu_dollars
FROM home_felix_mutzl.strategist_canvas.v_engagements_unified e
WHERE e.fy = '{fy}'
  AND e.strategist_email = '{strategist_email}'
ORDER BY e.engagement_type, e.customer
```

### Revenue Impact Query: Focus Account Growth
```sql
SELECT
  e.customer,
  c.usage_date_string,
  c.fiscal_year,
  ROUND(SUM(c.dbu_dollars)) AS dbu_dollars,
  ROUND(AVG(c.growth_rate), 4) AS growth_rate
FROM home_felix_mutzl.strategist_canvas.v_engagements_unified e
LEFT JOIN main.gtm_gold.rpt_c360_overview_unpivoted c
  ON e.account_id = c.account_id
WHERE e.engagement_type = 'Focus'
  AND e.strategist_email = '{strategist_email}'
  AND c.date_grain = 'quarterly'
  AND c.fiscal_year BETWEEN 2024 AND 2027
  AND c.bu1 = 'Central'
GROUP BY e.customer, c.usage_date_string, c.fiscal_year
ORDER BY e.customer, c.usage_date_string
```

### KPI Summary Query
```sql
SELECT
  COUNT(DISTINCT e.account_id) AS total_accounts,
  COUNT(DISTINCT CASE WHEN e.engagement_type = 'Focus' THEN e.account_id END) AS focus_accounts,
  COUNT(DISTINCT CASE WHEN e.engagement_type = 'One-off' THEN e.account_id END) AS oneoff_accounts,
  COUNT(*) AS total_engagements,
  COUNT(DISTINCT e.territory_area) AS territories_covered,
  COUNT(DISTINCT e.ae) AS ae_partners
FROM home_felix_mutzl.strategist_canvas.v_engagements_unified e
WHERE e.fy = '{fy}'
  AND e.strategist_email = '{strategist_email}'
```

If the user's `strategist_email` is not known (no profile), **ask them directly** — do not assume or default to any email. If the `~/.vibe/profile` file exists, check it for the user's Databricks email as a fallback.

---

## Step 3 — Enrich with Additional Sources (Optional)

If additional context is available, pull from:

1. **Salesforce ASQs** — via `fe-salesforce-tools:salesforce-actions` — specialist requests created/completed this quarter
2. **Calendar** — via `fe-google-tools:google-calendar` — count of customer meetings, internal strategy sessions
3. **Gmail** — via `fe-google-tools:gmail` — count of customer-facing emails in the quarter
4. **Slack** — notable threads, shout-outs, or recognition mentions

Only pull these if the user asks for a comprehensive summary or if the engagement data alone is thin.

---

## Step 4 — Score Against the 4-Domain Model

Map all findings to Wiseman's Impact Players framework:

### Domain 1: Account Outcomes
*Revenue growth in strategist-engaged accounts — the before/after.*

- Focus account revenue trajectory (QoQ and YoY)
- Advisor portfolio growth vs. regional benchmark (Central)
- Specific wins: new use cases launched, commit expansions, competitive displacements
- Map to profile KPIs: "$ revenue influenced", "consumption growth in engaged accounts"

### Domain 2: Engagement Quality
*Depth and format of engagements — Focus (deep, multi-quarter) vs. One-off (targeted).*

- Breakdown: # Focus vs. # One-off engagements
- Format mix: Advisory, Keynote, Point of View, Workshop, Strategy Session
- Engagement status: Active, Completed, Pipeline
- Map to profile KPIs: "# data & AI programs", "# customer events", "# high-value use cases"

### Domain 3: Strategic Influence
*Breadth of reach — territories, AE partnerships, C-level access.*

- Territories covered (out of assigned territories)
- AE partners engaged (count + names)
- C-level doors opened (from engagement data + Salesforce)
- Map to profile KPIs: "C-level doors opened", "public events spoken at"

### Domain 4: Knowledge Multiplication
*Reusable value created — assets, frameworks, publications, coaching.*

This domain is NOT yet tracked in the dashboard. Pull from:
- Profile's `outcomes.reusable_value` — what assets were created this quarter?
- Ask the user directly: "What reusable assets, frameworks, or publications did you create this quarter?"
- Check for: internal decks, external publications, LinkedIn posts, speaking engagements, open-source contributions, skill/plugin creation

Map to profile KPIs: "# reusable assets", "# publications"

---

## Step 5 — Generate the Impact Summary

Produce a crisp, structured summary. Keep it tight — this is for leadership review, not a diary.

```markdown
# Quarterly Impact Summary: [FY Quarter]
**Strategist:** [Name] | **Period:** [Month range] | **Generated:** [Date]

## Headlines
- [1-3 bullet points: the most important things that happened]

## Account Outcomes (Domain 1)
| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Focus portfolio revenue | — | $XXX | [trend] |
| YoY growth (advisor vs. region) | — | XX% vs. XX% | [above/below] |
| Notable wins | — | [list] | — |

## Engagement Quality (Domain 2)
| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Total engagements | — | XX | — |
| Focus / One-off split | — | X / X | — |
| Data & AI programs launched | [from profile] | X | [on/off track] |
| Customer events delivered | [from profile] | X | [on/off track] |

## Strategic Influence (Domain 3)
| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| C-level doors opened | [from profile] | X | [on/off track] |
| Territories covered | X | X | — |
| AE partners | — | X | — |
| Public events | [from profile] | X | [on/off track] |

## Knowledge Multiplication (Domain 4)
| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Reusable assets | [from profile] | X | [on/off track] |
| Publications | [from profile] | X | [on/off track] |
| [Specific items: frameworks, decks, plugins, posts] |

## Engagement Detail
[Table of all engagements this quarter: Customer | Type | Format | AE | Status]

## Goal Attainment (from STRIDE Profile)
[For each named_goal in the profile, show target vs. actual with a traffic light]

## Dashboard Link
[Strategist Impact Dashboard](https://adb-2548836972759138.18.azuredatabricks.net/dashboardsv3/01f0f51a424b1cc0bc6f5feba0c33948/published?o=2548836972759138)
```

---

## Step 6 — Output Options

After generating the summary, offer:
1. **View here** — display in the terminal (default)
2. **Google Doc** — create a formatted Google Doc using `fe-google-tools:google-docs`
3. **Google Slides** — create a slide deck version for leadership review
4. **Update dashboard** — remind the user to classify unclassified engagements in the source data

---

## Key Principles

1. **Data first, narrative second.** Pull numbers before writing prose.
2. **Map everything to the profile.** Every metric should connect to a KPI or named goal.
3. **Be honest about gaps.** If Knowledge Multiplication is thin, say so — don't pad.
4. **Before/After is the gold standard.** Show trajectories, not snapshots.
5. **Keep it tight.** This is a leadership artifact, not a journal. One page of signal, not three pages of activity.
6. **Link to the dashboard.** The summary complements the dashboard, not replaces it.
