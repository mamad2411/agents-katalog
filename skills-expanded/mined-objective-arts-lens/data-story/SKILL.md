---
name: data-story
description: "Data storytelling"
---

<essential_principles>
## The Six Lessons of Storytelling with Data

These principles transform data from noise into narrative. Apply them in order.

### 1. Understand the Context

Before touching any tool, answer three questions:

**WHO** is your audience?
- What do they know? What do they need to know?
- What biases or preconceptions do they have?
- What will make them care?

**WHAT** do you want them to do?
- Be specific: "approve the budget" not "understand the situation"
- If you can't articulate the action, you're not ready to visualize

**HOW** will you communicate?
- Live presentation? Written report? Dashboard?
- This determines level of detail and annotation needed

<context_checklist>
Before creating any visualization:
- [ ] I can state my audience in one sentence
- [ ] I can state the desired action in one sentence
- [ ] I know the communication mechanism
- [ ] I have identified the "So What?" - why should they care?
</context_checklist>

### 2. Choose an Effective Visual

**The right chart for the job:**

| Data Relationship | Best Chart Type | Avoid |
|-------------------|-----------------|-------|
| Comparison (few categories) | Horizontal bar | Pie, 3D |
| Comparison (many categories) | Horizontal bar, sorted | Vertical bar |
| Time series | Line chart | Area (unless stacked) |
| Part-to-whole | 100% stacked bar, treemap | Pie (>3 slices) |
| Correlation | Scatterplot | Dual-axis line |
| Distribution | Histogram, box plot | Bar chart |

**Default choices:**
- When in doubt: **simple bar chart or line chart**
- Tables: Use when audience needs exact values
- Text: Use when you have 1-2 numbers to communicate

<chart_selection_rules>
ALWAYS avoid:
- Pie charts (except 2-3 slices max)
- 3D effects (distorts perception)
- Dual y-axes (confuses correlation with causation)
- Donut charts (harder to compare than pie)
- Radar/spider charts (difficult to read)

PREFER:
- Horizontal bars over vertical (labels read naturally)
- Line charts for time (even with few points)
- Direct labels over legends
</chart_selection_rules>

### 3. Eliminate Clutter

**Clutter is your enemy.** Every element should earn its place.

Remove ruthlessly:
- Chart borders and backgrounds
- Gridlines (or lighten to near-invisible)
- Data markers on lines (unless highlighting specific points)
- Legends (use direct labels instead)
- Axis lines (data speaks for itself)
- Bold/italic formatting (unless strategic)

**The Declutter Checklist:**
```
For each element ask: "Would removing this change the meaning?"
If NO → Remove it
If YES → Keep it (but consider if it can be lighter/smaller)
```

<clutter_identification>
Visual clutter includes:
- Borders, boxes, shading that don't encode data
- Heavy gridlines
- Unnecessary axis labels or tick marks
- Legends (when direct labels would work)
- Data markers on every point
- Gradient fills
- 3D effects
- Rotated text
- Unnecessary precision (3.14159 → 3.1)
</clutter_identification>

### 4. Focus Attention

**Use preattentive attributes strategically.**

Preattentive attributes (processed in <500ms):
- **Color** - Most powerful. Use sparingly for emphasis.
- **Size** - Larger = more important
- **Position** - Top-left gets seen first (in Western reading)
- **Enclosure** - Boxes draw attention
- **Bold** - For headlines and key numbers only

<attention_strategy>
The hierarchy of emphasis:
1. ONE thing should be boldest/brightest (your main point)
2. Supporting elements in medium gray
3. Everything else in light gray or removed

COLOR RULES:
- Gray is your friend (use for de-emphasis)
- ONE accent color for emphasis
- Never use red/green alone (colorblindness)
- Brand colors are fine, but don't let them drive design
</attention_strategy>

### 5. Think Like a Designer

**Affordances:** Make it obvious how to read your visual
- Clear title that states the insight (not just the topic)
- Axis labels that don't require rotation
- Annotations that explain, not just label

**Accessibility:**
- Sufficient contrast (4.5:1 minimum)
- Don't rely on color alone
- Alt text for screen readers

**Alignment:**
- Left-align text (easier to scan)
- Align data to make comparisons easy
- Use consistent spacing

<design_checklist>
- [ ] Title states the insight ("Sales grew 15%" not "Sales Data")
- [ ] No rotated text
- [ ] Direct labels instead of legend where possible
- [ ] Consistent color meaning across visuals
- [ ] White space used intentionally
- [ ] Mobile-friendly if needed
</design_checklist>

### 6. Tell a Story

**Structure your narrative:**

**Beginning:** Set up the context
- What's the current situation?
- Why does this matter now?

**Middle:** Build the tension
- What's the problem or opportunity?
- What are the stakes?

**End:** Resolve with action
- What should the audience do?
- What happens if they don't?

<story_framework>
The "So What?" test:
After every insight, ask "So what?" until you reach the action.

Example:
- "Sales are down 10%" → So what?
- "We're missing Q3 targets" → So what?
- "We need to approve the new marketing campaign by Friday"
← THIS is your story's conclusion
</story_framework>
</essential_principles>

<intake>
What would you like to do?

1. **Review** a visualization (get improvement suggestions)
2. **Choose** a chart type for my data
3. **Declutter** an existing visualization
4. **Focus** attention on key insights
5. **Structure** a data story/presentation

Share your visualization, data, or context and I'll apply the SWD framework.
</intake>

<review_process>
## SWD Review Framework

When reviewing any visualization, evaluate in this order:

**1. Context Check**
- Is the audience clear?
- Is the action explicit?
- Is the "So What?" obvious?

**2. Chart Type Audit**
- Is this the right chart for the data relationship?
- Would a simpler chart work?
- Are there SWD-forbidden elements (pie charts, 3D, dual axes)?

**3. Clutter Scan**
- Borders, gridlines, backgrounds → Remove or lighten?
- Legend → Can it be direct labels?
- Axis elements → Minimum necessary?
- Precision → Appropriate decimal places?

**4. Attention Assessment**
- What's the ONE thing that should stand out?
- Is color used sparingly and strategically?
- Is gray used for de-emphasis?

**5. Story Structure**
- Does the title state the insight?
- Is there clear narrative arc?
- Does it end with a call to action?

<scoring>
SWD Compliance Score (0-100):

| Category | Weight | Criteria |
|----------|--------|----------|
| Context | 15 | Clear audience, action, mechanism |
| Chart Choice | 20 | Appropriate type, no forbidden charts |
| Clutter | 25 | Minimal non-data ink |
| Focus | 25 | Strategic use of preattentive attributes |
| Story | 15 | Insight title, clear narrative |
</scoring>
</review_process>

<quick_fixes>
## Common Problems → Quick Fixes

| Problem | SWD Fix |
|---------|---------|
| "I don't know what to look at" | Add ONE accent color, gray everything else |
| "It's too busy" | Remove gridlines, borders, legend → direct labels |
| "The title is generic" | Change "Sales Data" to "Sales grew 15% in Q3" |
| "Too many categories" | Group into "Top 5 + Other" or use horizontal bars |
| "Pie chart with 8 slices" | Convert to horizontal bar, sorted by value |
| "Can't read axis labels" | Rotate chart (vertical → horizontal bars) |
| "Dual y-axes" | Split into two charts or use indexed values |
| "3D chart" | Flatten immediately |
</quick_fixes>

<code_patterns>
## Implementation Patterns

### D3.js - SWD-Compliant Defaults
```javascript
// Minimal, clean styling
const swd = {
  colors: {
    emphasis: '#2563eb',    // Blue for focus
    neutral: '#6b7280',     // Gray for context
    background: '#ffffff',
    light: '#e5e7eb'        // Very light gray for subtle gridlines
  },
  axis: {
    tickSize: 0,            // No tick marks
    strokeWidth: 0          // No axis lines
  },
  grid: {
    stroke: '#f3f4f6',      // Nearly invisible
    strokeDasharray: '2,2'  // Dotted if needed
  }
};

// Direct labels over legends
bars.append('text')
  .attr('x', d => x(d.value) + 5)
  .attr('y', d => y(d.category) + y.bandwidth() / 2)
  .attr('dy', '0.35em')
  .text(d => d.value);
```

### Tailwind CSS - SWD Palette
```css
/* De-emphasis (most elements) */
.swd-muted { @apply text-gray-400; }

/* Normal context */
.swd-neutral { @apply text-gray-600; }

/* Emphasis (ONE thing) */
.swd-emphasis { @apply text-blue-600 font-semibold; }

/* Remove chart chrome */
.swd-clean-chart {
  @apply border-0 bg-transparent;
}
```
</code_patterns>

<success_criteria>
A visualization passes the SWD test when:
- [ ] A stranger can identify the main point in 5 seconds
- [ ] The title states an insight, not a topic
- [ ] Color is used for ONE purpose only
- [ ] No legends (direct labels used)
- [ ] No 3D, pie charts (>3 slices), or dual axes
- [ ] Gridlines are invisible or nearly so
- [ ] The audience knows what to do next
</success_criteria>
