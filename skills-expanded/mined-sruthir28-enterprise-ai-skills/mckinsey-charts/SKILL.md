---
name: mckinsey-charts
description: Generate McKinsey-style consulting charts as native python-pptx objects (editable inside PowerPoint). Three workhorse types — bar+callout for TAM/single-number stories, stacked column over time for revenue/usage mix, and waterfall for drivers/bridge analysis. Use when you need a chart that looks like it came from an EM-reviewed deck, not from Excel defaults.
---

# McKinsey Charts

Drop-in chart builders for python-pptx. Charts are inserted as **native PowerPoint chart objects** — your audience can edit the data, change the colors, copy the chart to their own deck. No images, no screenshots.

## The Three Charts

| Type | When to use | Example |
|------|-------------|---------|
| `bar_callout` | One number is the story. TAM, market size, headcount, anything where you want to anchor on a single highlighted bar with a big callout. | "RTD coffee TAM will hit **$42.5B** by 2028" |
| `stacked_bar_over_time` | Composition over time. Revenue by segment, usage by feature, headcount by function. Shows both total growth and mix shift. | "Revenue grew 3x, but enterprise segment grew 7x" |
| `waterfall` | Bridging two numbers. Revenue walk, cost walk, headcount changes, any "start → adds → subtracts → end" story. | "FY24 → FY25 revenue bridge: $80M → $112M" |

## Design choices (intentional, not configurable)

- **Title is a claim, not a label.** "RTD market will hit $42.5B by 2028" beats "Market Size."
- **One highlight color, everything else grey.** McKinsey decks don't rainbow. The chart points at one thing.
- **No gridlines, no chart border, no legend unless multi-series.** Less ink → more signal.
- **Source line at the bottom in light grey italic.** Always include it.
- **Single font (Inter) at consistent sizes.** Title 20pt, axis 10pt, source 9pt.

## How to use

```python
from pptx import Presentation
from pptx.util import Inches
from charts import add_bar_callout, add_stacked_bar_over_time, add_waterfall, new_deck

prs = new_deck()  # 16:9 with title slide layout
slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank

add_bar_callout(
    slide,
    title="RTD coffee TAM will hit $42.5B by 2028",
    categories=["2023", "2024", "2025", "2026", "2027", "2028"],
    values=[28.1, 30.8, 33.6, 36.5, 39.4, 42.5],
    highlight_index=5,        # which bar to highlight (last one here)
    callout="$42.5B\n2028 TAM",
    y_label="USD, billions",
    source="Euromonitor 2025; Mintel; team analysis",
)

prs.save("output.pptx")
```

Same pattern for the other two:

```python
add_stacked_bar_over_time(
    slide,
    title="Enterprise segment now drives 62% of revenue, up from 18% in 2021",
    categories=["2021", "2022", "2023", "2024", "2025"],
    series=[
        ("SMB",        [12, 14, 15, 16, 18]),
        ("Mid-market", [8,  12, 16, 22, 28]),
        ("Enterprise", [4,  10, 22, 38, 74]),
    ],
    highlight_series="Enterprise",
    y_label="Revenue, $M",
    source="Internal financials; FY21–FY25",
)

add_waterfall(
    slide,
    title="FY24 → FY25 revenue bridge: $80M → $112M, with new logos doing the heavy lifting",
    labels=["FY24",  "New logos", "Expansion", "Churn",  "Price",  "FY25"],
    values=[80.0,    24.0,        12.0,        -8.0,     4.0,      112.0],
    kinds=["start",  "pos",       "pos",       "neg",    "pos",    "total"],
    y_label="Revenue, $M",
    source="Internal financials; FY24–FY25",
)
```

## Test it

```
python3 test_charts.py
open test_output.pptx
```

The test script generates one slide per chart type with realistic sample data. Open it in PowerPoint or Keynote and right-click any chart → "Edit Data" to confirm it's a native chart, not an image.

## When NOT to use this skill

- You need a **distribution** (use a histogram or box plot — not a McKinsey staple).
- You need a **scatter / quadrant** (the 2x2 / portfolio map is a different skill).
- You're showing **>5 series** stacked (split into small multiples instead — one chart can't carry that load).
