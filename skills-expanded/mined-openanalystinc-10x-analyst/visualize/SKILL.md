---
name: visualize
description: "Generate charts and plots from data — line, bar, pie, heatmap, scatter, histogram"
argument-hint: "[dataset-name] [chart-type or description]"
risk: "safe"
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Write, Bash, Glob, Grep
model: claude-haiku-4-5-20251001
context: fork
agent: general-purpose
---

# 10x Analyst — Visualizer

Generate publication-ready charts from any data file.

## Overview

Creates matplotlib/seaborn visualizations with the 10x.in style. Reads from `input/<dataset>/`, saves charts to `output/<dataset>/charts/`. Specify a chart type or describe what you want to see.

## When to Use

- User asks for a chart: "plot revenue over time", "show me a bar chart of top products"
- User wants to visualize a specific column or relationship
- User needs charts for a presentation or report

## Path Resolution

Parse `$ARGUMENTS`:
- First word: dataset name → reads from `input/<dataset-name>/`
- Remaining text: chart type or description
- Charts saved to: `output/<dataset-name>/charts/`

## Instructions

1. Parse `$ARGUMENTS`:
   - First word = dataset name
   - Rest = chart type or description (e.g., "line chart of revenue by month")
   - Input: `input/<dataset>/`
   - Output: `output/<dataset>/charts/`
2. Load the data file(s) from `input/<dataset>/`
3. Clean column names: lowercase, underscore-separated
4. Determine chart type from user's request:

| User Says | Chart Type |
|-----------|-----------|
| "trend", "over time", "line" | Line chart |
| "top", "ranking", "bar" | Bar chart (horizontal for >5 categories) |
| "breakdown", "proportion", "pie" | Donut chart |
| "correlation", "heatmap", "relationship" | Heatmap |
| "distribution", "histogram" | Histogram |
| "scatter", "compare two" | Scatter plot |
| "box", "spread" | Box plot |

5. Create output directory: `mkdir -p output/<dataset>/charts`
6. Write and execute a Python script:

```python
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# 10x style
COLORS = ['#FF6B35', '#004E89', '#00A878', '#FFD166', '#EF476F', '#118AB2', '#073B4C']
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette(COLORS)
plt.rcParams.update({'figure.figsize': (12, 6), 'figure.dpi': 150, 'font.size': 11})

# Load data from input/<dataset>/
df = pd.read_csv('input/<dataset>/file.csv')

# Generate chart
fig, ax = plt.subplots()
# ... chart-specific code ...
ax.set_title('Chart Title — Key Takeaway', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('output/<dataset>/charts/chart_name.png', bbox_inches='tight')
plt.close()
print("Chart saved to output/<dataset>/charts/chart_name.png")
```

7. Show the user the file path to the saved chart

## Examples

```bash
# Specific chart type
/10x-analyst:visualize shopify-data "line chart of revenue by month"

# Auto-detect best chart
/10x-analyst:visualize shopify-data "show me the top 10 products"

# Multiple charts
/10x-analyst:visualize shopify-data "revenue trend and customer segments"
```

## Limitations

- Static PNG output only — for interactive charts use `:dashboard`
- Max 15 categories per chart (remainder grouped as "Other")
- Requires matplotlib and seaborn installed

---
*Developed by [10x.in](https://10x.in) | 10x-Analyst v1.0.0*
