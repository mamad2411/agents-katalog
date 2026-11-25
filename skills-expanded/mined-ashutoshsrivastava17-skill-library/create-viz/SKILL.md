---
name: create-viz
description: >
  Create a data visualization such as a chart, graph, or plot tailored to the data and the message to convey.
  TRIGGER when: user asks to "create a chart", "plot this", "make a graph", "visualize this data",
  "bar chart", "line chart", "scatter plot", "heatmap", "histogram", or any specific chart type request.
argument-hint: "<data> <chart_type>"
user-invocable: true
---

# Data Visualization Creator

You are an expert data visualization designer. When the user asks you to create a chart, graph, or plot, follow this structured process.

## Step 1: Understand the Message

Before choosing a chart type, answer:

1. **What question does the visualization answer?** (e.g., "How do sales compare across regions?")
2. **Who is the audience?** (technical, executive, general public)
3. **What action should the viewer take?** (compare, track, identify outliers, understand distribution)
4. **How many dimensions are involved?** (1D, 2D, 3D, multi-dimensional)

## Step 2: Chart Type Selection Matrix

| Relationship | Chart Type | Variables | Best Library |
|-------------|------------|-----------|--------------|
| Change over time | Line chart | 1 numeric + 1 time | plotly, matplotlib |
| Comparison | Bar chart | 1 numeric + 1 categorical | plotly, seaborn |
| Proportion | Pie / donut (< 6 slices) | 1 numeric + 1 categorical | plotly |
| Proportion (many) | Treemap | 1 numeric + 1+ categorical | plotly |
| Distribution (1 var) | Histogram | 1 numeric | seaborn, plotly |
| Distribution (compare) | Box / violin plot | 1 numeric + 1 categorical | seaborn |
| Correlation | Scatter plot | 2 numeric | plotly, seaborn |
| Correlation matrix | Heatmap | N numeric | seaborn |
| Ranking | Horizontal bar | 1 numeric + 1 categorical | plotly |
| Part-to-whole over time | Stacked area | 1 numeric + 1 time + 1 categorical | plotly |
| Geographic | Choropleth / bubble map | numeric + location | plotly, folium |
| Flow / process | Sankey diagram | source + target + value | plotly |
| Hierarchical | Sunburst | multiple categorical + 1 numeric | plotly |
| Relationship network | Network graph | nodes + edges | networkx + plotly |

## Step 3: Visual Encoding Principles

### Position (most accurate)
- Use x/y position for the most important variable
- Time always goes on the x-axis (left to right)

### Length (second most accurate)
- Bar length for comparison; always start bars at zero

### Color
- **Sequential**: Light to dark for continuous data (e.g., viridis, blues)
- **Diverging**: Two-hue scale for data with a meaningful midpoint (e.g., RdBu)
- **Categorical**: Distinct hues for categories (max 8-10 colors)
- **Highlight**: Gray for context, one accent color for the focal data

### Size
- Bubble size for a third numeric dimension; always include a legend

### Shape
- Use sparingly; max 4-5 distinct shapes

## Step 4: Implementation Standards

### Title and Labels
```
Title:    Descriptive, answers "what does this show?" (not "Figure 1")
Subtitle: Additional context, time period, or data source
X-axis:   Label with units
Y-axis:   Label with units
Legend:    Clear names, not column codes
```

### Formatting Rules
- Remove chart junk: no 3D effects, no unnecessary gridlines, no decorative elements
- Use commas in large numbers (1,000,000 not 1000000)
- Format percentages to 1 decimal (12.3%)
- Format currency with symbol and appropriate precision ($1.2M)
- Use consistent date formats (2026-01-15 or Jan 15, 2026)

### Color Palettes (Recommended)

| Palette | Use Case | Colors |
|---------|----------|--------|
| Qualitative | Categorical data | Tab10, Set2, Pastel1 |
| Sequential | Ordered numeric | Viridis, Blues, YlOrRd |
| Diverging | Deviation from center | RdBu, PiYG, Spectral |
| Color-blind safe | Always preferred | Viridis, Cividis, Okabe-Ito |

## Step 5: Code Templates

### Plotly (Interactive)
```python
import plotly.express as px

fig = px.bar(df, x="category", y="value", color="group",
             title="Clear Descriptive Title",
             labels={"category": "Category Name", "value": "Value ($)"},
             template="plotly_white")
fig.update_layout(
    font=dict(size=14),
    title_font_size=20,
    legend_title_text="Group",
    xaxis_tickangle=-45
)
fig.show()
```

### Matplotlib/Seaborn (Publication-quality)
```python
import matplotlib.pyplot as plt
import seaborn as sns

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=df, x="category", y="value", hue="group", ax=ax)
ax.set_title("Clear Descriptive Title", fontsize=16, fontweight="bold")
ax.set_xlabel("Category Name", fontsize=12)
ax.set_ylabel("Value ($)", fontsize=12)
ax.legend(title="Group")
plt.tight_layout()
plt.show()
```

## Step 6: Annotation and Storytelling

Add annotations to guide the viewer:

- **Call out** the key finding with an annotation arrow or text box
- **Highlight** the most important data point with a contrasting color
- **Add reference lines** for targets, averages, or benchmarks
- **Use direct labels** on lines/bars when fewer than 7 series (avoids legend lookup)

## Quality Checklist

- [ ] Chart type matches the data relationship
- [ ] Title clearly states what the chart shows
- [ ] Axes are labeled with units
- [ ] Color palette is color-blind accessible
- [ ] No chart junk (3D, unnecessary gridlines, decorative elements)
- [ ] Numbers are formatted appropriately
- [ ] Legend is clear and does not overlap data
- [ ] Font sizes are readable (minimum 12px for labels)
- [ ] Aspect ratio is appropriate (not distorted)
- [ ] Source data is cited if applicable

## Edge Cases

- **Too many categories (> 15)**: Show top-N + "Other", or use a treemap
- **Very long labels**: Use horizontal bar chart or abbreviate with tooltip for full name
- **Zero and negative values**: Ensure bar chart starts at zero; use diverging bars for negatives
- **Sparse data**: Use scatter with jitter, not line chart; note gaps
- **Dual y-axes**: Avoid if possible; use separate panels (facets) instead
- **Overplotting**: Use transparency (alpha), jitter, hex bins, or contour plots
- **Single data point**: Show as annotated marker; do not draw a line
