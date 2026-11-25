---
name: monthly-business-review-prep
description: Prepare the FinOps section of the monthly business review. Triggers on phrases like "MBR prep", "monthly business review", "monthly cost review", "I need to put together my MBR". Pulls last month's spend by service and team, computes trends vs the prior 3 months, drafts the narrative that goes in the deck, and surfaces the anomalies leadership will ask about.
---

# Monthly Business Review Prep

When invoked, do the data pull and write the narrative section of the FinOps MBR slide(s). The goal is that the practitioner shows up to the review with a draft that's 80% there, leaving them to add color and field questions instead of formatting numbers at midnight.

## Inputs to confirm before starting

- The month being reviewed (default: most recently closed month)
- The audience (default: VP+ leadership; adjust tone if it's a different group)
- Any major events from the month the practitioner wants called out
- Whether the deck uses a specific template — if so, ask for a sample slide

## Steps

1. **Pull the month's spend.** Total spend, broken down by:
   - Service (top 10 only; bucket the rest as "Other")
   - Team / cost center (every team that's >1% of total)
   - Environment (prod / non-prod / shared)

2. **Compute trends.** For each cut above, show:
   - Month-over-month change ($, %)
   - Three-month rolling average comparison (this month vs. avg of prior 3)
   - Year-over-year if data is available

3. **Surface anomalies.** Anything that moved more than 15% MoM or 25% vs. 3-month average. List with one-line explanation each. Use `anomaly-triage` outputs if any incidents from the month were already triaged.

4. **Draft the narrative.** See template below.

5. **Build the "questions leadership will ask" list.** For each major movement, anticipate the question and have the answer ready.

## Narrative template

The narrative section is three paragraphs, in this order:

**Paragraph 1: The headline.** Total spend, change vs. last month, change vs. forecast. One sentence on whether we're tracking to budget for the quarter.

**Paragraph 2: What drove the change.** The 2–3 movements that explain most of the delta. Each gets one sentence: *what moved, by how much, why*. Tie to business activity where possible (product launches, customer growth, infrastructure changes).

**Paragraph 3: What's coming.** Forward-looking. Known events that will affect next month's spend. Any commitment renewals, contract milestones, or migrations. One sentence on whether the current trajectory needs intervention.

## House rules

- Lead with totals, then percentages, never the reverse. ("$2.4M, up 8% MoM" not "Up 8% MoM, to $2.4M.")
- Round to the nearest hundred dollars under $10K, nearest thousand above. Never present sub-cent precision.
- Connect spend changes to business activity where you can. Spend that grew with revenue is a different story than spend that grew without it.
- No service-name jargon in the narrative paragraphs. ("Our analytics platform" not "BigQuery", unless you've established the term earlier.)

## Output format

```
## Headline numbers
[Total | MoM | vs forecast | budget tracking]

## Top movements
[Bulleted list, biggest first, dollar amounts with brief why]

## Anomalies flagged this month
[Any item over 15% MoM or 25% vs 3-month avg, with one-line explanation]

## Narrative (paste into deck)
[Three paragraphs as templated above]

## Questions to be ready for
[5–8 questions leadership is likely to ask, with the answer for each]
```

## Customization notes

- The 15% / 25% anomaly thresholds are starting defaults. Tune them to your org's noise level.
- If your org has specific reporting taxonomy (e.g., "Compute" rolls up GKE + GCE + serverless), encode that in this skill rather than re-explaining it every month.
- Add MBR-specific framings your leadership uses ("unit economics", "$ per active user", whatever maps to your business) here so the AI uses your vocabulary.
