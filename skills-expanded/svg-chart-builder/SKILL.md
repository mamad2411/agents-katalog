---
name: svg-chart-builder
description: Generate clean, consistently styled SVG bar and line charts from CSV data using python3 stdlib only — no matplotlib, no dependencies — saved as .svg files. Use when the user says "chart this", "visualize this CSV", "make a bar/line chart", "graph this data", or wants a visual for a report or deck. Don't use for computing the stats and findings themselves — that's csv-data-analyst; run it first and chart its output.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Research & Analysis, Charts, Visualization, SVG]
    related_skills: [csv-data-analyst, survey-response-synthesizer]
---

# SVG Chart Builder

Produces publication-ready bar and line charts as standalone .svg files from a two-column CSV (label, value), using only python3's stdlib. One house style — clean axis, readable labels, one accent color — so every chart from this skill looks like it belongs to the same report. The standard: the chart plots exactly the numbers in the CSV (verified against a recomputed max/min), axes never lie (bars start at zero), and the file opens in any browser.

## When to Use

- User has numbers (CSV or a table from `csv-data-analyst` / `survey-response-synthesizer`) and wants a visual.
- Charts for HTML reports, decks, or landing pages where a dependency-free .svg is ideal.
- **Not for:** the analysis itself — `csv-data-analyst` finds the story; this skill draws it. Not for interactive dashboards (that's an app build, outside this track).

## Quick Reference

| Action | Command / Call |
|---|---|
| Precheck | `command -v python3`; CSV must be `label,value` with a header row |
| Bar chart | `python3 chart.py data.csv out.svg bar "Title"` (script in step 3) |
| Line chart | `python3 chart.py data.csv out.svg line "Title"` |
| Verify output | `python3 -c "print(open('out.svg').read(120))"` — starts with `<svg` |
| View | open the .svg in any browser; embeds directly in HTML via `<img>` or inline |

## Procedure

1. **Precheck** — `command -v python3`. Confirm the CSV is two columns (`label,value`) with a header; if it has more columns, ask which value column to plot and reshape first. Bar for categories, line for ordered sequences (time) — confirm the choice matches the data.
2. **Sanity-scan the data** — check for: non-numeric values, negative numbers (bars handle them; note it), >16 categories for bars (aggregate the tail into "Other" first, with the user's OK), unsorted time labels for lines (sort chronologically, tell the user).
3. **Write the generator once per session** — save as `/tmp/chart.py`:
   ```python
   import csv, sys, html
   src, out, kind, title = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
   rows = list(csv.reader(open(src, newline='', encoding='utf-8-sig')))[1:]
   labels = [r[0] for r in rows]; vals = [float(r[1]) for r in rows]
   W, H, L, R, T, B = 720, 400, 64, 24, 56, 64          # canvas + margins
   pw, ph = W - L - R, H - T - B
   top = max(max(vals), 0) or 1; bot = min(min(vals), 0)
   y = lambda v: T + ph * (top - v) / (top - bot)
   ACCENT, INK, GRID, FONT = "#4F46E5", "#1F2937", "#E5E7EB", "font-family='Helvetica,Arial,sans-serif'"
   s = [f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {W} {H}' {FONT}>",
        f"<text x='{L}' y='28' font-size='18' font-weight='bold' fill='{INK}'>{html.escape(title)}</text>"]
   for i in range(5):                                    # gridlines + y labels
       gv = bot + (top - bot) * i / 4
       s.append(f"<line x1='{L}' y1='{y(gv):.1f}' x2='{W-R}' y2='{y(gv):.1f}' stroke='{GRID}'/>")
       s.append(f"<text x='{L-8}' y='{y(gv)+4:.1f}' font-size='11' text-anchor='end' fill='{INK}'>{gv:,.6g}</text>")
   step = pw / len(vals)
   if kind == "bar":
       bw = step * 0.62
       for i, v in enumerate(vals):
           x = L + i * step + (step - bw) / 2
           s.append(f"<rect x='{x:.1f}' y='{min(y(v),y(0)):.1f}' width='{bw:.1f}' "
                    f"height='{abs(y(v)-y(0)):.1f}' fill='{ACCENT}' rx='2'/>")
   else:
       pts = " ".join(f"{L + (i+0.5)*step:.1f},{y(v):.1f}" for i, v in enumerate(vals))
       s.append(f"<polyline points='{pts}' fill='none' stroke='{ACCENT}' stroke-width='2.5'/>")
       s += [f"<circle cx='{p.split(',')[0]}' cy='{p.split(',')[1]}' r='3.5' fill='{ACCENT}'/>" for p in pts.split()]
   for i, lab in enumerate(labels):                      # x labels, thinned if crowded
       if len(labels) <= 12 or i % (len(labels) // 12 + 1) == 0:
           s.append(f"<text x='{L + (i+0.5)*step:.1f}' y='{H-B+18}' font-size='11' "
                    f"text-anchor='middle' fill='{INK}'>{html.escape(lab[:14])}</text>")
   s.append("</svg>")
   open(out, "w").write("\n".join(s)); print(f"wrote {out}: {kind}, {len(vals)} points")
   ```
4. **Generate** — `python3 /tmp/chart.py data.csv revenue_by_month.svg line "Revenue by month"`. Expected output: `wrote ... line, N points`. Name files descriptively (what_by_what.svg), never chart1.svg.
5. **Verify visually and numerically** — confirm the file starts with `<svg`, then check the tallest bar / highest point corresponds to the CSV's max value (`python3 -c` one-liner over the CSV). Offer the user the file and, if the destination is an HTML report, the inline-embed option.

## Output Template

```
Chart saved: <absolute path>.svg
Type: bar|line | Points: N | Source: <csv path>, column <name>
Max plotted: <label> = <value> (matches CSV max: yes)
Style: house (720x400, indigo #4F46E5 accent, zero-based value axis)
Caveats: <tail aggregated into "Other" / labels thinned / negative values present / none>
```

## Pitfalls

- **Truncated value axis exaggerating differences** — starting bars at 90 makes a 3% gap look like 3x. Recovery: the script pins the axis to zero for bars by design (`max(...,0)`/`min(...,0)`); if the user asks for a zoomed axis on a line chart, add a visible axis-break note in the title, never silently.
- **Too many categories** — 40 bars render as unreadable slivers. Recovery: cap bars at 16; aggregate the smallest into "Other" (disclosed in caveats) or switch to a sorted top-N chart with the user's OK.
- **Currency/percent strings crash float()** — `"$1,200"` in the value column throws. Recovery: strip `$ € £ , %` in a pre-pass (or via `csv-data-analyst`'s cleaning), and report how many values were cleaned.
- **Unescaped labels break the XML** — a label containing `&` or `<` produces an .svg that won't open. Recovery: the script routes every label and title through `html.escape`; if a chart won't render, check for raw ampersands first.
- **Chart contradicts the analysis** — plotting a different column or stale file than the findings cite. Recovery: the numeric verification step (max value cross-check) is mandatory before delivering; state the source column in the output block.

## Verification

- [ ] File exists, starts with `<svg`, and opens in a browser
- [ ] Highest/lowest plotted point matches the CSV's actual max/min
- [ ] Bar charts have a zero-based value axis (or a disclosed break)
- [ ] All labels readable (thinned/truncated per the script, noted if so)
- [ ] Filename is descriptive; source CSV and column stated in the delivery note
