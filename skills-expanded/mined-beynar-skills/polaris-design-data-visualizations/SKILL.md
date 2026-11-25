---
name: polaris-design-data-visualizations
description: Create effective data visualizations for Shopify analytics. Master chart types, accuracy, intuitiveness, axes, labeling, color coding, and accessibility for merchant insights.
---

# Data Visualizations

Visualizations surface patterns in data and provide immediate answers to a single, specific question.

## Visualization Process

Always begins with:
1. A set of data
2. A specific question
3. Analysis to find the answer

**Core principle:** Each visualization focuses on answering one specific question. Example: "What are my sales over time?"

## Guidelines

### Solving a Problem

Have a clear question that needs answering.

**Do:**
- Define the single question you're answering
- Focus on one specific insight
- Avoid over-complication

**Don't:**
- Try to answer multiple questions in one chart
- Create over-complicated visualizations

### Testing with Real Data

Test effectiveness with actual data patterns.

**Do:**
- Test with real data
- Test edge cases (1-2 data points, 100+ data points)
- Verify scaling works

**Don't:**
- Use only perfect datasets
- Skip edge case testing

### Scaling by Data Points

Consider visualization behavior at different scales.

**Considerations:**
- Sparse data (mostly zero values)
- Spiky data (some values much larger)
- Few vs. many data points
- Performance with large datasets

## Five Core Traits

An effective visualization balances these traits intentionally:

### Accuracy
How faithfully the visualization matches the original dataset. High accuracy not always needed to convey trends.

### Intuitiveness
Ease of interpreting the visualization. Will merchants immediately understand, or need instructions?

### Engagement
How much attention the visualization attracts at a glance. Sometimes best visualizations are supportive, not prominent.

### Focus
How merchant attention is directed. Highly focused visualizations decrease cognitive overload but may restrict message breadth.

### Data Granularity
Level of detail presented. More granular = more data points and processing. Depends on question and audience.

## Axes and Labeling

**Standard chart conventions:**
- All quantitative charts have 2 labeled axes
- Label outside and separate from data area
- Clear, accurate labels
- Simple and short language
- Don't confuse label with data
- Never slant labels to fit

**Abbreviations:**
- 12-hour format for time (12am, 6pm)
- First 3 letters for days (Sun, Mon)
- First 3 letters for months (Feb, Mar)
- Day + month format (10 Apr, 11 Apr)
- Month + year format (Apr 2011, May 2017)

**Y-axis monetary abbreviations:**
- 'k' for thousand
- 'b' for billion
- Maximum 3 numeric characters + 1 decimal + 1 letter

## Chart Types

### Horizontal Bar Charts

**Best for:** Discrete category comparisons (products vs. sales)

**Don't use when:** Data points exceed 6 (use table instead)

**Guidelines:**
- Label each bar with value
- Include label on top showing category
- Use one color for all bars
- Give negative bars 60% opacity
- Bar width roughly twice the space between bars

**Don't:**
- Use multiple colors
- Make bars too skinny
- Exceed 6 categories

### Vertical Column Charts

**Best for:**
- Change over time
- Trends and individual data points
- Fewer than 30 data points

**Don't use when:** Data points exceed 31 (use line chart)

**Guidelines:**
- All bars same color
- Bar width roughly twice the space
- Include tooltips for hover interaction
- Follow axis labeling conventions

**Don't:**
- Use multiple colors
- Make bars too skinny
- Use for sparse time data

### Line Charts

**Best for:**
- Continuous data over time
- Change, comparisons, trends
- 30+ data points
- Larger time granularities (yearly, quarterly)

**Multi-line guidelines:**
- Use contrasting colors
- Include legend
- Maximum 4 lines per chart

**Don't:**
- Use too many lines (> 4)
- Overcrowd the visualization

### Display Metrics

Single quantifiable measures showing status.

**Guidelines:**
- Pair with base unit in close proximity
- Use concise language
- Include time dimension scope
- Consider comparison indicator (previous period, average)
- Green for positive movement
- Red for negative movement

### Tables

Large amounts of information with many variables.

**Best for:**
- Large discrete datasets
- Multiple variables and categories
- Filtering and ordering
- Accurate value lookup

**Guidelines:**
- Left align non-numeric values
- Right align numeric values
- Don't center column headers
- Use light lines for row separation
- Don't highlight alternating rows
- Place totals as first row beneath headers, bold text

## Color Palettes

Color in data visualization has specific meaning.

**Single data series:** Use single unified color

**Single comparison to past:** Current = purple, Previous = grey

**Multiseries data:** Specific palette for multiple datasets

**Biased:** Show positive/negative relative to reference value

## Accessibility

### Provide Options

Multiple formats for data visualizations.

**Do:**
- Let merchants access data in multiple formats
- Offer data in table format
- Make alternative formats discoverable

**Don't:**
- Provide data in only one format

### Use of Color

**Do:**
- Ensure sufficient contrast
- Use colors distinguishable for colorblindness
- Test with colorblind users

**Don't:**
- Require color perception to understand data
- Use color alone for differentiation

### SVG Accessibility

**Do:**
- Hide SVG elements from screen readers (aria-hidden="true")
- Provide separate text equivalent
- Create consistent experience

**Don't:**
- Leave SVG content inaccessible
- Assume assistive technology compatibility
