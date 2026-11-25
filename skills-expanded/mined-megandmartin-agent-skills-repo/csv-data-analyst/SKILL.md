---
name: csv-data-analyst
description: Analyze any CSV with python3 stdlib only — schema sniff, summary stats, outlier detection, group-by breakdowns — delivered as a findings report where every stat carries a "so what" line. Use when the user says "analyze this CSV", "what does this data say", "summarize this export", "find outliers", or hands over any .csv wanting insight. Don't use for clustering open-ended text answers — that's survey-response-synthesizer — or for drawing charts — that's svg-chart-builder.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Research & Analysis, Data, CSV, Statistics]
    related_skills: [svg-chart-builder, survey-response-synthesizer, market-sizing-tam]
---

# CSV Data Analyst

Turns a raw CSV into a decision-ready findings report using nothing but python3's stdlib (`csv`, `statistics`, `collections`). The standard: every number in the report is computed from the file (never estimated), and every stat gets one plain-language "so what" line — a stat without a consequence is trivia, not analysis.

## When to Use

- User hands over a .csv (exports from Stripe, forms, analytics, spreadsheets) and asks what it means.
- User wants outliers, distributions, or "which segment is biggest/best/worst" answers.
- Pre-work before charting or sizing: get the real numbers first.
- **Not for:** clustering free-text answers (`survey-response-synthesizer`) or rendering visuals (`svg-chart-builder` — feed it this skill's output).

## Quick Reference

| Action | Command / Call |
|---|---|
| Precheck | `command -v python3` and `head -3 "$FILE"` |
| Schema sniff | python heredoc below, step 2 — delimiter, columns, types, null counts |
| Summary stats | `statistics.mean/median/stdev/quantiles` per numeric column |
| Outliers | IQR fence: outside `[Q1 - 1.5*IQR, Q3 + 1.5*IQR]` |
| Group-by | `collections.defaultdict(list)` keyed on the category column |
| Row count sanity | `python3 -c "import csv;print(sum(1 for _ in csv.reader(open('$FILE'))))"` |

## Procedure

1. **Precheck** — `command -v python3` and confirm the file path exists (`test -f "$FILE"`). Run `head -3 "$FILE"` to eyeball encoding and delimiter. If the file is missing or binary, stop and ask for a real CSV export.
2. **Schema sniff** — run; expect columns, inferred types, and null counts per column:
   ```bash
   python3 - "$FILE" <<'PY'
   import csv, sys
   f = open(sys.argv[1], newline='', encoding='utf-8-sig')
   dialect = csv.Sniffer().sniff(f.read(8192)); f.seek(0)
   rows = list(csv.reader(f, dialect))
   hdr, data = rows[0], rows[1:]
   print(f"delimiter={dialect.delimiter!r} rows={len(data)}")
   for i, c in enumerate(hdr):
       vals = [r[i].strip() for r in data if len(r) > i]
       filled = [v for v in vals if v]
       num = sum(1 for v in filled if v.replace('.','',1).replace('-','',1).isdigit())
       kind = "numeric" if filled and num/len(filled) > 0.9 else "text"
       print(f"{c}: {kind}, {len(vals)-len(filled)} empty, {len(set(filled))} distinct")
   PY
   ```
3. **Ask the question** — confirm with the user which 1–3 questions the analysis should answer (or infer the obvious ones from column names and say so). Analysis without a question produces a stat dump.
4. **Summary stats** — for each numeric column compute count, mean, median, stdev, min, max via `statistics`. Mean far from median means skew — report median as the headline number and say why.
5. **Outliers** — `q1, q2, q3 = statistics.quantiles(vals, n=4)`; flag values outside `q1 - 1.5*(q3-q1)` to `q3 + 1.5*(q3-q1)`. List the actual outlier rows (identifying column + value), not just the count.
6. **Group-bys** — for each categorical column with 2–20 distinct values, group the key numeric column with `defaultdict(list)` and report per-group count, median, and share of total. Sort by the metric, not alphabetically.
7. **Deliver** — fill the template. Every stat line ends with a "so what" a founder can act on. If a stat has no consequence, cut it.

## Output Template

```
# CSV Findings — <filename> — <date>
Rows: N | Columns: N | Question(s): <what we set out to answer>

## Headline
<The single most decision-relevant finding, one sentence, with its number.>

## Stats that matter
- <metric>: <value> — so what: <consequence in plain language>
- <group-by>: <top/bottom groups with numbers> — so what: <...>
- Outliers: <n> rows outside the IQR fence: <list> — so what: <...>

## Data quality notes
- <empty columns, suspicious duplicates, type mismatches — or "clean">

## Confidence
<high/medium/low> — <why: sample size, nulls, whether data covers the question>
```

## Pitfalls

- **Sniffer misreads the delimiter** — semicolon or tab files parse as one giant column. Recovery: if the sniff reports 1 column, retry with `csv.reader(f, delimiter=';')` then `'\t'`; confirm column count matches the header eyeballed in step 1.
- **Currency and thousands separators break numeric parsing** — `"$1,200"` counts as text and silently drops out of stats. Recovery: strip `$ € £ , %` and whitespace before the numeric test in step 2; report how many values needed cleaning.
- **Mean reported on skewed data** — one whale customer makes the average meaningless. Recovery: always compute median alongside mean; when they diverge >20%, lead with median and name the skew source (usually the outliers from step 5).
- **Empty strings counted as zeros** — nulls treated as 0 crater averages. Recovery: filter empties before math, report the null count per column, and never impute without telling the user.
- **Answering questions the data can't support** — e.g., "why did churn rise" from a file with no time column. Recovery: state the limit explicitly in Confidence and list what extra column/export would answer it.

## Verification

- [ ] Row count in the report matches an independent `sum(1 for _ in reader)` count
- [ ] Every number in the report was computed from the file — nothing estimated
- [ ] Every stat line has a "so what" consequence
- [ ] Nulls and cleaned values disclosed in Data quality notes
- [ ] Confidence label present with a stated reason
