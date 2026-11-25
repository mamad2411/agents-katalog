---
name: g2-charts
description: "Declarative, grammar-based charting using AntV G2 for complex medical visualizations. Use when creating forest plots, Kaplan-Meier curves, funnel plots, waterfall charts, or any statistical/clinical chart that requires grammar-of-graphics composition with medical-journal-grade styling and accessibility-validated color palettes."
---

# G2 Grammar-Based Charts

**Purpose:** Declarative, grammar-based charting using AntV G2 for complex medical visualizations.

**Status:** ✅ Production Ready

---

## Tool Selection

```
Does Plotly have a built-in chart type that works?
├─ YES → Use Plotly (faster, simpler)
└─ NO → Do you need custom composition?
    ├─ YES → Use G2 (grammar-based)
    └─ NO → Use drawsvg (pure Python SVG)
```

**Use G2 for:** complex multi-layer compositions, custom chart types, multi-panel figures, template-driven workflows, publication figures requiring precise control.

**Use Plotly for:** standard charts, interactive dashboards, quick prototyping.

---

## Quick Start

```python
from g2_charts.medical_grammars import forest_plot_grammar
from g2_charts.grammar_renderer import G2Chart

# Create grammar specification
grammar = forest_plot_grammar(
    studies=['DAPA-HF', 'EMPEROR-Reduced'],
    estimates=[0.74, 0.75],
    lower_ci=[0.65, 0.65],
    upper_ci=[0.85, 0.86],
    title="SGLT2i Trials"
)

# Render chart
chart = G2Chart(width=800, height=600)
chart.grammar = grammar
chart.render('forest.png')

# Validate output
import os
assert os.path.exists('forest.png'), "Render failed: output file not created"
```

For all other grammar types (Kaplan-Meier, grouped bars, multi-panel, scatter/regression, heatmap) with full parameter references, see [GRAMMARS.md](GRAMMARS.md).

---

## Rendering Workflow with Validation

```python
from grammar_renderer import G2Chart
import os

chart = G2Chart(width=800, height=600)
chart.grammar = grammar

# 1. Validate grammar spec before rendering
required_keys = ['data', 'marks']
for key in required_keys:
    assert key in grammar, f"Grammar missing required key: '{key}'"

# 2. Render
output_path = 'output.png'
chart.render(output_path)

# 3. Verify output exists and has valid dimensions
assert os.path.exists(output_path), "Render failed: output file not created"
assert os.path.getsize(output_path) > 1000, "Render may have failed: output file suspiciously small"
```

---

## CLI Usage

```bash
# List available templates
python g2_cli.py list-templates

# Generate forest plot
python g2_cli.py forest \
  --studies "DAPA-HF,EMPEROR-Reduced,VICTORIA" \
  --estimates "0.74,0.75,0.90" \
  --lower "0.65,0.65,0.82" \
  --upper "0.85,0.86,0.98" \
  -o forest.png

# Generate Kaplan-Meier from data file
python g2_cli.py kaplan --data survival.json -o km.svg --format svg

# Generate grouped bars from data
python g2_cli.py grouped --data trial_results.json -o bars.png

# Generate all demo charts
python g2_cli.py demo --all
```

### Data File Formats

**Kaplan-Meier (survival.json):**
```json
{
  "groups": ["Treatment", "Control"],
  "time": [
    [0, 6, 12, 18, 24],
    [0, 6, 12, 18, 24]
  ],
  "survival": [
    [1.0, 0.90, 0.82, 0.78, 0.75],
    [1.0, 0.85, 0.72, 0.65, 0.58]
  ]
}
```

**Grouped Bars (trial_results.json):**
```json
{
  "categories": ["Primary", "Secondary", "Safety"],
  "groups": ["Treatment", "Placebo"],
  "values": [
    [12.3, 8.5, 3.2],
    [18.7, 14.2, 2.8]
  ]
}
```

---

## Custom Grammars

```python
from grammar_renderer import G2Chart

chart = G2Chart(width=800, height=600)

# Set data
chart.data([
    {'category': 'A', 'value': 23},
    {'category': 'B', 'value': 45},
    {'category': 'C', 'value': 31}
])

# Add interval mark (bars)
chart.add_mark(
    'interval',
    encode={'x': 'category', 'y': 'value'},
    style={'fill': '#1e3a5f', 'radius': 2}
)

# Configure scales, axes
chart.scale('y', {'nice': True})
chart.axis('x', title='Category')
chart.axis('y', title='Value', grid=True)

# Render with validation
output_path = 'custom.png'
chart.render(output_path)
assert os.path.exists(output_path), "Render failed"
```

For a full reference of grammar components (`data`, `marks`, `scales`, `coordinate`, `axes`, `legend`) and all supported mark types (`point`, `line`, `interval`, `area`, `cell`, `text`, `rect`), see [GRAMMARS.md](GRAMMARS.md).

---

## Output Formats

```python
chart.render('output.png', format='png')  # Publication quality, 800×600px default
chart.render('output.svg', format='svg')  # Vector; editable in Illustrator/Inkscape
```

---

## Further Reading

- [GRAMMARS.md](GRAMMARS.md) — Full parameter reference for all six medical grammar types, grammar components, and mark types
- [COOKBOOK.md](COOKBOOK.md) — Recipes: annotations, custom colors, confidence bands
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) — Node.js, npm, canvas, and Python import fixes
- [AntV G2 Documentation](https://g2.antv.antgroup.com/en)
- [Grammar of Graphics (Wilkinson)](https://www.springer.com/gp/book/9780387245447)
- [Design Tokens](../tokens/)
- [Plotly Charts](../../cardiology-visual-system/scripts/plotly_charts.py)
