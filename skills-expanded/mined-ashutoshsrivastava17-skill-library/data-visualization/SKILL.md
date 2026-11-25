---
name: data-visualization
description: >
  Comprehensive data visualization guidance covering best practices, chart selection, design principles, and accessibility.
  TRIGGER when: user asks for "visualization best practices", "which chart should I use", "data viz guidelines",
  "chart design principles", "how to present data", "visualization strategy", or "make my charts better".
argument-hint: "[topic_or_question]"
user-invocable: true
---

# Data Visualization Best Practices

You are an expert in data visualization design, perception science, and visual communication. Provide comprehensive guidance on creating effective, truthful, and accessible visualizations.

## Core Principles

### 1. Truthfulness
- Never distort data to support a narrative
- Start bar charts at zero
- Use consistent scales across compared panels
- Avoid dual y-axes unless absolutely necessary (prefer faceting)
- Label truncated axes clearly
- Show uncertainty when it exists (confidence intervals, error bars)

### 2. Clarity
- One chart, one message
- Remove every element that does not convey information (chart junk)
- Use direct labels over legends when feasible (fewer than 7 series)
- Sort data meaningfully (by value, time, or logical order -- not alphabetically unless that IS logical)
- Use whitespace to separate visual groups

### 3. Efficiency
- Maximize the data-ink ratio (Tufte's principle)
- Choose encodings that leverage human perceptual strengths (position > length > angle > area > color saturation)
- Use small multiples instead of overloaded single charts

## Chart Selection Decision Tree

```
What are you showing?
|
+-- Change over time?
|   +-- Few series (1-5) --> Line chart
|   +-- Many series --> Small multiples OR highlight + gray
|   +-- Part-of-whole over time --> Stacked area
|   +-- Single period change --> Slope chart
|
+-- Comparison?
|   +-- Few categories --> Vertical bar
|   +-- Many categories (>7) --> Horizontal bar (sorted)
|   +-- Two time points --> Dumbbell chart
|
+-- Distribution?
|   +-- One variable --> Histogram or density plot
|   +-- Compare groups --> Box plot, violin, ridge plot
|   +-- Two variables --> 2D density or hex bin
|
+-- Relationship?
|   +-- Two variables --> Scatter plot
|   +-- Three variables --> Bubble chart (size = 3rd var)
|   +-- Many variables --> Pair plot or correlation heatmap
|
+-- Composition?
|   +-- Static, few parts (<6) --> Pie/donut (use sparingly)
|   +-- Static, many parts --> Treemap
|   +-- Over time --> Stacked bar or stacked area
|
+-- Spatial?
|   +-- Regions --> Choropleth map
|   +-- Points --> Bubble map or dot map
|
+-- Flow/Process?
    +-- Stage-to-stage --> Sankey diagram
    +-- Funnel --> Funnel chart
```

## Color Guidelines

### Palette Selection

| Data Type | Palette Type | Examples |
|-----------|-------------|----------|
| Categorical (unordered) | Qualitative | Okabe-Ito, Set2, Tab10 |
| Ordered numeric | Sequential | Viridis, Blues, YlOrRd |
| Diverging from center | Diverging | RdBu, PiYG, Coolwarm |
| Binary / highlight | Accent | Gray + one saturated color |

### Color-Blind Accessibility

- 8% of males and 0.5% of females have color vision deficiency
- Avoid red-green as the only differentiator
- Preferred safe palettes: Viridis, Cividis, Okabe-Ito
- Test with a color-blindness simulator (e.g., Coblis)
- Supplement color with shape, pattern, or direct labels

### Color Rules
- Maximum 8-10 distinct categorical colors (after that, use grouping)
- Use color consistently across a dashboard (same category = same color everywhere)
- Reserve red for negative/alert, green for positive/success (but not as only encoding)
- Gray is your best friend: use it for context, reference, and de-emphasis

## Typography in Visualizations

| Element | Recommended Size | Weight |
|---------|-----------------|--------|
| Chart title | 16-20px | Bold |
| Subtitle / annotation | 12-14px | Regular |
| Axis labels | 12-14px | Medium |
| Tick labels | 10-12px | Regular |
| Data labels | 10-12px | Regular |
| Source / footnote | 9-10px | Light |

- Use a single sans-serif font family (Inter, Roboto, Helvetica)
- Left-align text, right-align numbers
- Use tabular (monospaced) numerals for aligned columns

## Accessibility Standards (WCAG)

- **Contrast ratio**: Minimum 4.5:1 for text, 3:1 for graphical elements
- **Text alternatives**: Provide alt text or data tables for screen readers
- **Patterns**: Use texture/pattern fills in addition to color
- **Keyboard navigation**: Interactive charts must be keyboard-accessible
- **Focus indicators**: Visible focus ring on interactive elements

## Common Anti-Patterns to Avoid

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Pie chart with 10+ slices | Unreadable | Use horizontal bar chart |
| 3D charts | Distorts perception | Use 2D always |
| Truncated y-axis on bar chart | Exaggerates differences | Start at zero |
| Rainbow color map | Not perceptually uniform | Use viridis or similar |
| Dual y-axes | Misleading correlation | Use two separate panels |
| Spaghetti lines (>7 series) | Unreadable | Highlight + gray, or small multiples |
| Overuse of animation | Distracting | Animate only to show change/transition |
| Missing axis labels | Ambiguous | Always label with units |

## Responsive and Multi-Format Design

| Output | Considerations |
|--------|---------------|
| Web (desktop) | Interactive tooltips, hover states, 1200px+ width |
| Web (mobile) | Simplify, larger touch targets, vertical layout |
| Print / PDF | High DPI (300+), no interactivity, explicit legends |
| Presentation | Large fonts (18px+), minimal text, high contrast |
| Email | Static image, alt text, keep under 600px wide |

## Annotation Best Practices

- Annotate the insight, not just the data point
- Use leader lines to connect annotation to data without overlap
- Place annotations in whitespace, not over data
- Keep annotation text brief (1-2 sentences max)
- Use consistent annotation styling throughout a report

## Quality Checklist

- [ ] Chart type is appropriate for the data relationship
- [ ] Title answers "what does this show?"
- [ ] All axes have labels with units
- [ ] Color palette is color-blind safe
- [ ] No chart junk (3D, unnecessary gridlines, decorative elements)
- [ ] Data-ink ratio is high
- [ ] Numbers are formatted with appropriate precision
- [ ] Annotations highlight the key insight
- [ ] Source is credited
- [ ] Accessibility standards are met (contrast, alt text)
- [ ] Chart works at intended output size and format

## Edge Cases

- If input data is incomplete, state assumptions explicitly and flag gaps
- For time-sensitive situations, prioritize speed over comprehensiveness
- If multiple stakeholders have conflicting needs, document the tradeoffs
- For first-time use, start with a simplified version and iterate
- Adapt the depth and detail to the audience's expertise level
