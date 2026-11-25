---
name: stock-dashboard
description: "A visual dashboard for a stock or a comparison of stocks: price board, latest quarter, key metrics, verdict — drawn with blocks."
version: 0.1.0
platforms: [linux, macos, windows]
---
# Stock dashboard

Use this when someone asks to analyse a company, show a stock "visually", or compare companies in depth. A quick
"how is X doing" needs only `market_history`, not this recipe.

## Steps

1. **Prices:** call `market_history` with the company (or up to 3, comma separated, to compare) and period `1y`.
   Keep the board id from the tag it returns, e.g. `7f3a09bc`.
2. **Latest quarter:** search the web for the latest reported quarter: revenue and its growth, operating margin,
   net income, EPS against estimates, and guidance. Note where each number came from. If a number isn't found, leave
   it out; never estimate one.
3. **Lay it out** with one `show_blocks` call, in this order:
   - a `heading` naming the company and the quarter;
   - the price board via `{"type": "include", "id": "<the id from step 1>"}`;
   - `columns` with a bar chart of the last 4 quarters' revenue (if you found them) beside a `table` of key metrics
     (for a comparison, one column per company and `highlight` the stronger one);
   - a `callout` (tone `info`) with the verdict in one or two sentences;
   - a `source` line naming the sites.
4. **Reply** with one short paragraph, then the tag on its own line. The dashboard carries the numbers.

## Layout example

The include id here is a placeholder; use the one market_history returned.

```json
[
  {"type": "heading", "text": "Alphabet · Q3 2026"},
  {"type": "include", "id": "7f3a09bc"},
  {"type": "columns", "children": [
    {"type": "chart", "kind": "bar", "title": "Revenue, $B", "unit": "$B", "x": ["Q4 25", "Q1 26", "Q2 26", "Q3 26"],
     "series": [{"name": "Revenue", "data": [96.5, 90.2, 102.1, 127.6]}]},
    {"type": "table", "caption": "Latest quarter", "columns": ["Metric", "Value"],
     "rows": [["Revenue growth", "+25%"], ["Operating margin", "31.8%"], ["EPS vs estimate", "$2.10 vs $2.25"]]}
  ]},
  {"type": "callout", "tone": "info", "title": "Verdict", "text": "Growth is strong, but free cash flow turned negative as capex doubled."},
  {"type": "source", "text": "Company Q3 release · Yahoo Finance"}
]
```

## Rules

- Only numbers from tools or the search results; say "not reported" rather than guessing.
- No buy, sell or price-target advice.
- Never write HTML or use `::preview` for this; blocks only.
