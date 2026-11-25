---
name: hr-people-report
version: 1.0.0
description: Build headcount, attrition, diversity, and org-health reports — every metric defined, small-n protected, insight before data dump.
author: matrixx0070
tags: [people-analytics, attrition, diversity, headcount, reporting, org-health]
capabilities: []
---

## When to use

Reach for this when preparing a monthly/quarterly people review, answering a leadership question about the workforce, or tracking a metric like regretted attrition. Report numbers accurately, define every metric, and lead with insight.

**Not for:** forward-looking hiring plans (use hr-org-planning), pricing a role (use hr-comp-analysis), or live pipeline status (use hr-recruiting-pipeline).

## Method

1. **Scope the report** — audience, period, and org cut (company/function/team). State the as-of date and data source.
2. **Headcount** — starting/ending headcount, hires, exits, net change, open reqs; break down by function and level.
3. **Attrition** — annualized attrition = exits ÷ average headcount. Split voluntary vs. involuntary and regretted vs. non-regretted; show trend vs. prior periods.
4. **Diversity** — representation by relevant dimensions at overall, leadership, and hiring-funnel stages, with period delta. Decision point: for any small-n group, suppress or aggregate to protect privacy rather than publishing an identifiable count.
5. **Org health** — spans/layers, tenure distribution, internal mobility, and engagement/eNPS if available.
6. **Interpret** — call out the 3-5 signals that matter, likely drivers, and recommended actions. Decision point: distinguish correlation from cause and flag any data-quality caveat before it misleads a decision.

## Example

Q2, Engineering, as-of 2026-06-30, source Workday. Headcount 210 → 218 (+12 hires, -4 exits). Annualized attrition 7.5% (3 voluntary / 1 involuntary; 2 of the 3 voluntary flagged regretted) vs. 6.1% in Q1 — trending up. Regretted exits both cite comp; two open competing offers matched market 60th. Women in eng 26% overall but 14% at manager+ — a leadership-pipeline gap. Insight + action: launch a mid-level promotion review to widen the manager funnel; revisit senior-eng bands after the comp signal.

## Pitfalls

- Publishing a raw number for a group of 2-3 people, making individuals identifiable.
- Quoting an attrition rate without stating the formula or the denominator (average vs. ending headcount).
- Reporting diversity at company level only, hiding the leadership-tier gap.
- Dumping every chart with no ranked insight, so leadership can't tell what matters.

## Output format

```
Executive summary: top 3-5 insights + recommended actions
Headcount: table + net-change waterfall (start, hires, exits, end)
Attrition: rate (formula), voluntary/involuntary, regretted split, trend
Diversity: representation by level + funnel, period delta (small-n suppressed)
Org health: spans, layers, tenure, mobility, eNPS
Metric definitions + data caveats
```

## Reference

### Metric definitions — get the denominator right

The most common reporting error is an undefined or wrong denominator. State the formula every time.

```
average headcount   = (beginning HC + ending HC) ÷ 2
attrition (ann'l)   = (exits in period ÷ average HC) × (12 ÷ months in period)
turnover rate       = total separations ÷ average HC            # some use total exits incl. involuntary
voluntary attrition = voluntary exits ÷ average HC
regretted attrition = regretted exits ÷ average HC              # the one leadership cares about
retention rate      = (employees present start & end) ÷ start HC
net change          = hires − exits
new-hire attrition  = exits within 90/180d ÷ hires in that window   # onboarding/quality-of-hire signal
internal mobility   = internal moves ÷ average HC
```

Annualize short periods (a monthly rate ×12; a quarterly rate ×4) and say you did. Use **average** headcount as the denominator, not ending — ending understates attrition in a growing org and overstates it in a shrinking one.

### Attrition splits that matter

Raw attrition hides the story. Always decompose:

- **Voluntary vs. involuntary** — the employee chose to leave vs. the company did. Involuntary spikes may be planned (perf, RIF); voluntary spikes are the warning signal.
- **Regretted vs. non-regretted** — would you rehire this person? Regretted voluntary attrition is the single most important retention metric; a company can have "healthy" 10% total attrition that is all regretted (crisis) or all non-regretted (healthy pruning).
- **By cohort** — attrition by tenure band (0–90d, 3–12mo, 1–2yr, 2yr+), by level, by function, by manager. Early attrition points at hiring/onboarding; senior attrition at growth/comp.

**Reference ranges:** overall annual voluntary attrition of ~10% is common/healthy for many industries; sustained regretted attrition above ~10%, or a sharp quarter-over-quarter rise, warrants investigation. Tech and high-demand functions run higher. Compare to *your own* trend and industry benchmark, not a universal number.

### Small-n privacy protection

Any breakdown that makes an individual identifiable is a privacy and legal risk. Standard practice:

- Suppress or aggregate any group with **fewer than ~5** people (some orgs use n<10 for sensitive dimensions like disability, ethnicity, or health).
- When you suppress one cell, suppress a complementary cell too — otherwise the reader back-calculates it (if total and all-but-one groups show, the hidden one is trivially derived).
- Never publish a raw count for a 2–3 person demographic slice. Report a range, aggregate up a level, or omit with a "n too small to report" note.
- Apply the same threshold consistently so suppression itself doesn't leak information.

### Diversity reporting

Report representation at three cuts, each with a period delta:

1. **Overall** — the headline number.
2. **Leadership** (manager+ / director+) — where pipeline gaps hide; company-wide parity often masks a thin leadership tier.
3. **Hiring funnel** — representation at applied → screen → onsite → offer → hire, to find the stage where representation drops (a bias signal to investigate, not to conclude cause).

Show the delta vs. prior period so trend is visible. Always pair diversity numbers with the small-n rules above. Do not attribute a gap to a single cause from the data alone — flag it for investigation.

### Org-health metrics

- **Spans & layers** — avg span, count of managers with span <3 (layering) or >10 (overload); number of management layers.
- **Tenure distribution** — median tenure and the shape; a bulge at 0–1yr with thin 2yr+ signals a retention cliff.
- **Internal mobility** — % of roles filled internally; healthy orgs promote/transfer meaningfully rather than always hiring out.
- **Manager quality / eNPS** — engagement or eNPS by team if survey data exists; segment by manager and tenure.
- **Time-to-productivity / new-hire attrition** — links people-analytics back to hiring quality.

### Insight before data dump — the reporting discipline

Lead every report with the **3–5 signals that actually matter** and a recommended action for each, before any table. Leadership should be able to read the executive summary and know what to do. Then:

- Attach the formula/denominator to every rate.
- Distinguish **correlation from cause** — "regretted exits both cite comp" is a signal to investigate, not proof comp is the driver.
- Flag data-quality caveats *before* the number, not in a footnote — a stale source or missing field can flip a conclusion.
- Show trend, not just a point-in-time snapshot; one quarter is noise, three is a pattern.

### Executive-summary template

```
Period | org cut | as-of date | data source

Top signals (ranked):
  1. <metric moved> — <likely driver, flagged as hypothesis> → <recommended action, owner>
  2. ...
Then: headcount waterfall → attrition (with splits) → diversity (small-n suppressed) → org health → definitions & caveats
```

### Common pitfalls (numeric)

- Quoting attrition without the denominator (ending vs. average) — can misstate the rate by 10–20% in a fast-growing org.
- Not annualizing a monthly/quarterly figure, then comparing it to an annual benchmark.
- Publishing an identifiable small-n cell.
- Reporting only company-level diversity, hiding the leadership-tier gap.
- Presenting a snapshot with no trend, so a normal fluctuation reads as a crisis (or vice versa).
- Dumping every chart with no ranked insight — leadership can't tell signal from noise.
