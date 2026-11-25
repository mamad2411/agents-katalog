---
name: data-create-viz
version: 1.0.0
description: Produce a publication-quality static visualization in Python with a deliberately chosen chart type and a message-first title.
author: matrixx0070
tags: [visualization, python, matplotlib, charts, reporting, chart-choice]
capabilities: []
---

# data-create-viz

## When to use

Use this when you need one polished static chart — for a report, slide, or export — where clarity and correct chart-type choice matter more than interactivity.

**Not for:** an explorable multi-chart tool with filters (use data-build-dashboard), deciding whether a difference is significant (use data-statistical-analysis), or answering the underlying question (use data-analyze).

## Method

1. **Name the message.** Every chart makes one point. Write it as a sentence; the title should state that point, not just label axes.
2. **Choose the chart type by data relationship:**
   - Trend over time → line.
   - Comparison across categories → horizontal bar, sorted by value.
   - Part-to-whole → stacked bar, or (rarely, ≤4 slices) donut — never a pie for many slices.
   - Distribution → histogram or box/violin.
   - Correlation → scatter, with trend line only if a relationship is claimed.
   - Composition over time → stacked area.
   Decision point: if two encodings both fit, pick the one that puts the message on a position axis (bar/line) over area/angle.
3. **Build in Python** (matplotlib/seaborn). Sort bars, start value axes at zero for bars, label directly instead of relying on legends.
4. **Design for legibility:** high contrast, minimal gridlines, no chartjunk, colorblind-safe palette, readable fonts at final scale.
5. **Annotate** the key point (peak, inflection, outlier) so the message is unmissable.
6. **Export** at high resolution (PNG 2x, plus SVG when scalable output helps).

## Example

Message: "Region West drives 40% of revenue." A pie of 8 regions hides it; a sorted horizontal bar makes West's dominance instant.

```python
import matplotlib.pyplot as plt
d = df.sort_values("revenue")
plt.barh(d.region, d.revenue)
plt.title("West drives 40% of revenue")  # title = the point
plt.xlim(0, None)                          # bars start at zero
plt.tight_layout(); plt.savefig("rev_by_region@2x.png", dpi=200)
```

## Pitfalls

- Titling with the metric ("Revenue by region") instead of the takeaway.
- Truncating a bar's value axis so a small difference looks huge.
- Pie/donut with many slices, forcing readers to compare angles.
- Encoding series in a red/green palette that colorblind viewers cannot separate.

## Output format

```
Script:  runnable Python
Image:   exported file(s), descriptive filename (e.g. rev_by_region@2x.png)
Caption: one line stating the single takeaway
Source:  data source, filters, time window
```

Verify axes, units, and totals before exporting. If the chosen type would mislead, fix it and say why.
